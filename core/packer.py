"""
AbaoSplitZip 核心打包逻辑
将文件夹按指定大小分卷打包为独立可解压的 ZIP 文件
"""

import io
import json
import os
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional

import pyzipper

from core.version import APP_NAME, APP_VERSION
from core.zipcrypto import ZIP_CRYPTO, ZipCryptoZipFile

MAX_PACK_WORKERS = 4
DEFAULT_FILE_CHUNK_SIZE = 1024 * 1024
DEFAULT_ZIP_BUFFER_SIZE = 16 * 1024 * 1024

# 压缩级别映射
COMPRESSION_LEVELS = {
    "store": (zipfile.ZIP_STORED, 0),
    "fast": (zipfile.ZIP_DEFLATED, 1),
    "normal": (zipfile.ZIP_DEFLATED, 6),
    "max": (zipfile.ZIP_DEFLATED, 9),
}


class BufferedFileWriter:
    """
    分块缓冲写入器，作为 ZipFile 的文件对象。
    在内存中积攒到 chunk_size 后加锁写盘，减少磁盘碎片和 I/O 争抢。
    """

    def __init__(self, path: str, write_lock: threading.Lock, chunk_size: int = 8 * 1024 * 1024):
        self._path = path
        self._lock = write_lock
        self._chunk_size = chunk_size
        self._buffer = io.BytesIO()
        self._file = open(path, "wb")
        self._pos = 0
        self._closed = False

    def write(self, data: bytes) -> int:
        self._buffer.write(data)
        self._pos += len(data)
        if self._buffer.tell() >= self._chunk_size:
            self._flush()
        return len(data)

    def _flush(self):
        chunk = self._buffer.getvalue()
        if chunk:
            with self._lock:
                self._file.write(chunk)
            self._buffer = io.BytesIO()

    def tell(self) -> int:
        return self._pos

    def seek(self, offset: int, whence: int = 0):
        # ZipFile 在写入结尾目录时需要 seek
        self._flush()
        with self._lock:
            self._file.seek(offset, whence)
        if whence == 0:
            self._pos = offset
        elif whence == 1:
            self._pos += offset
        elif whence == 2:
            self._pos = self._file.tell()

    def flush(self):
        self._flush()
        with self._lock:
            self._file.flush()

    def close(self):
        if self._closed:
            return
        self._flush()
        self._file.close()
        self._closed = True


@dataclass
class PackResult:
    """打包结果"""
    total_files: int = 0
    total_size: int = 0
    volumes: int = 0
    output_files: list = field(default_factory=list)
    manifest_file: str = ""


@dataclass
class PackPreview:
    """打包前预估结果"""
    total_files: int = 0
    total_size: int = 0
    volumes: int = 0
    max_file_size: int = 0
    has_oversized_file: bool = False


class VolumePacker:
    """分卷打包器"""

    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        volume_size_mb: float,
        password: Optional[str] = None,
        compression_key: str = "normal",
        encryption_method: str = "zipcrypto",
        mode: str = "size_balanced",
        exclude_patterns: list = None,
        progress_callback=None,
        log_callback=None,
        cancel_check=None,
    ):
        if volume_size_mb <= 0:
            raise ValueError("volume_size_mb must be greater than 0")
        if mode not in {"size_balanced", "directory_priority"}:
            raise ValueError(f"unsupported mode: {mode}")

        self.source_dir = os.path.normpath(source_dir)
        self.output_dir = os.path.normpath(output_dir)
        self.volume_size_bytes = int(volume_size_mb * 1024 * 1024)
        self.password = password.encode("utf-8") if password else None
        self.compression_key = compression_key
        self.encryption_method = encryption_method
        self.mode = mode
        self.exclude_patterns = exclude_patterns or []
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_check = cancel_check
        self.file_chunk_size = DEFAULT_FILE_CHUNK_SIZE
        self.zip_buffer_size = DEFAULT_ZIP_BUFFER_SIZE

        comp = COMPRESSION_LEVELS.get(compression_key, COMPRESSION_LEVELS["normal"])
        self.compression_type = comp[0]
        self.compression_level = comp[1]

        self.folder_name = os.path.basename(self.source_dir)
        # 写盘锁：多线程压缩完成后排队写入磁盘，避免 I/O 争抢和碎片
        self._write_lock = threading.Lock()
        self._progress_lock = threading.Lock()
        self._bytes_done = 0
        self._total_bytes = 0
        self._last_progress = -1

    def _validate_paths(self):
        source_abs = os.path.abspath(os.path.realpath(self.source_dir))
        output_abs = os.path.abspath(os.path.realpath(self.output_dir))

        if not os.path.isdir(source_abs):
            raise ValueError("Source folder does not exist.")

        try:
            output_inside_source = os.path.commonpath([source_abs, output_abs]) == source_abs
        except ValueError:
            output_inside_source = False

        if output_inside_source:
            raise ValueError("Output folder must not be inside the source folder.")

    def _log(self, msg: str):
        if self.log_callback:
            self.log_callback(msg)

    def _progress(self, value: int):
        if self.progress_callback:
            self.progress_callback(value)

    def _progress_bytes(self, byte_count: int):
        if self._total_bytes <= 0 or byte_count <= 0:
            return
        with self._progress_lock:
            self._bytes_done += byte_count
            progress = min(99, int(self._bytes_done / self._total_bytes * 100))
            if progress > self._last_progress:
                self._last_progress = progress
                self._progress(progress)

    def _is_cancelled(self) -> bool:
        if self.cancel_check:
            return self.cancel_check()
        return False

    def scan_files(self) -> tuple:
        """扫描源文件夹，返回 (相对路径, 文件大小) 列表"""
        import fnmatch
        file_list = []
        max_file_size = 0
        
        for root, _dirs, files in os.walk(self.source_dir):
            if self._is_cancelled():
                raise RuntimeError("Operation cancelled.")
            for fname in files:
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, self.source_dir)
                
                # Check exclude patterns
                if any(fnmatch.fnmatch(rel_path, pat) for pat in self.exclude_patterns):
                    continue
                    
                size = os.path.getsize(full_path)
                file_list.append((rel_path, size))
                if size > max_file_size:
                    max_file_size = size
        
        if self.mode == "size_balanced":
            # 按大小降序排列，大文件优先分配（贪心装箱 - FFD）
            # 优点：分卷数量最少
            # 缺点：打乱了目录结构
            file_list.sort(key=lambda x: x[1], reverse=True)
        else:
            # directory_priority
            # 按路径名字母顺序排列，保持目录结构
            # 优点：同一目录下的文件尽可能在同一卷
            # 缺点：可能产生更多分卷（尾部空间浪费）
            file_list.sort(key=lambda x: x[0])
            
        return file_list, max_file_size

    def assign_volumes(self, file_list: list) -> list:
        """
        将文件分配到各分卷
        返回: [ [rel_path, ...], ... ] 每卷包含的文件列表
        """
        if self.mode == "size_balanced":
            # First Fit Decreasing (FFD)
            volumes = []       # 每个元素: [当前大小, [文件列表]]
            for rel_path, size in file_list:
                placed = False
                for vol in volumes:
                    if vol[0] + size <= self.volume_size_bytes:
                        vol[0] += size
                        vol[1].append(rel_path)
                        placed = True
                        break
                if not placed:
                    volumes.append([size, [rel_path]])
            return [vol[1] for vol in volumes]
        else:
            # Next Fit (保持顺序)
            # 依次放入当前卷，放不下就开新卷
            volumes = []
            current_vol_files = []
            current_vol_size = 0
            
            for rel_path, size in file_list:
                # 如果单个文件超过卷大小，必须单独放一卷（或者报错，这里选择单独放）
                if size > self.volume_size_bytes:
                    # 如果当前卷有内容，先封卷
                    if current_vol_files:
                        volumes.append(current_vol_files)
                        current_vol_files = []
                        current_vol_size = 0
                    # 大文件单独一卷
                    volumes.append([rel_path])
                    continue
                
                if current_vol_size + size <= self.volume_size_bytes:
                    current_vol_files.append(rel_path)
                    current_vol_size += size
                else:
                    # 放不下，封卷
                    if current_vol_files:
                        volumes.append(current_vol_files)
                    # 开新卷
                    current_vol_files = [rel_path]
                    current_vol_size = size
            
            # 最后一卷
            if current_vol_files:
                volumes.append(current_vol_files)
                
            return volumes

    def preview(self) -> PackPreview:
        """扫描并预估本次打包结果，不写入任何文件。"""
        self._validate_paths()
        file_list, max_file_size = self.scan_files()
        if not file_list:
            raise ValueError("Source folder is empty.")
        volume_files = self.assign_volumes(file_list)
        total_size = sum(size for _, size in file_list)
        return PackPreview(
            total_files=len(file_list),
            total_size=total_size,
            volumes=len(volume_files),
            max_file_size=max_file_size,
            has_oversized_file=max_file_size > self.volume_size_bytes,
        )

    def _create_zip(self, output_path: str, file_paths: list):
        """创建 ZIP 分卷，使用分块缓冲写盘减少碎片"""
        buf = BufferedFileWriter(output_path, self._write_lock, chunk_size=self.zip_buffer_size)
        try:
            if self.password:
                zip_kwargs = {
                    "compression": self.compression_type,
                    "compresslevel": self.compression_level if self.compression_type == zipfile.ZIP_DEFLATED else None,
                }
                if self.encryption_method == "aes256":
                    with pyzipper.AESZipFile(buf, "w", encryption=pyzipper.WZ_AES, **zip_kwargs) as zf:
                        zf.setpassword(self.password)
                        zf.setencryption(pyzipper.WZ_AES, nbits=256)
                        self._write_files(zf, file_paths)
                elif self.encryption_method == "zipcrypto":
                    with ZipCryptoZipFile(buf, "w", **zip_kwargs) as zf:
                        zf.setpassword(self.password)
                        zf.setencryption(ZIP_CRYPTO)
                        self._write_files(zf, file_paths)
                else:
                    raise ValueError(f"unsupported encryption method: {self.encryption_method}")
            else:
                with zipfile.ZipFile(
                    buf, "w",
                    compression=self.compression_type,
                    compresslevel=self.compression_level if self.compression_type == zipfile.ZIP_DEFLATED else None,
                ) as zf:
                    self._write_files(zf, file_paths)
        finally:
            buf.close()

    def _write_files(self, zf, file_paths: list):
        for rel_path in file_paths:
            if self._is_cancelled():
                raise RuntimeError("Operation cancelled.")
            full_path = os.path.join(self.source_dir, rel_path)
            arcname = os.path.join(self.folder_name, rel_path)
            self._write_file_to_zip(zf, full_path, arcname)

    def _write_file_to_zip(self, zf, full_path: str, arcname: str):
        zip_info = self._zip_info_for_file(zf, full_path, arcname)
        with open(full_path, "rb") as source, zf.open(zip_info, "w", force_zip64=True) as target:
            while True:
                if self._is_cancelled():
                    raise RuntimeError("Operation cancelled.")
                chunk = source.read(self.file_chunk_size)
                if not chunk:
                    break
                target.write(chunk)
                self._progress_bytes(len(chunk))
                if self._is_cancelled():
                    raise RuntimeError("Operation cancelled.")

    def _zip_info_for_file(self, zf, full_path: str, arcname: str):
        st = os.stat(full_path)
        date_time = time.localtime(st.st_mtime)[:6]
        if date_time[0] < 1980:
            date_time = (1980, 1, 1, 0, 0, 0)
        zip_info_cls = getattr(zf, "zipinfo_cls", zipfile.ZipInfo)
        zip_info = zip_info_cls(arcname, date_time)
        zip_info.compress_type = self.compression_type
        zip_info._compresslevel = self.compression_level if self.compression_type == zipfile.ZIP_DEFLATED else None
        zip_info.file_size = st.st_size
        zip_info.external_attr = (st.st_mode & 0xFFFF) << 16
        return zip_info

    def _pack_one_volume(self, i: int, total: int, vol_files: list):
        """打包单个分卷（供线程池调用）"""
        part_name = f"{self.folder_name}_part{i:03d}.zip"
        output_path = os.path.join(self.output_dir, part_name)
        try:
            self._create_zip(output_path, vol_files)
        except Exception:
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            raise
        zip_size = os.path.getsize(output_path)
        return i, output_path, part_name, zip_size, len(vol_files)

    def pack(self) -> PackResult:
        """执行打包（多线程并行压缩各分卷）"""
        result = PackResult()

        self._validate_paths()

        self._log("正在扫描文件夹...")
        file_list, max_file_size = self.scan_files()
        
        # Check for large files
        if max_file_size > self.volume_size_bytes:
             self._log(f"警告：检测到文件大小 ({max_file_size / 1024 / 1024:.1f} MB) 超过分卷大小。该文件将不会被分割，所在分卷将超出预设大小。")

        if not file_list:
            self._log("错误：源文件夹为空，没有可打包的文件。")
            raise ValueError("Source folder is empty.")

        result.total_files = len(file_list)
        result.total_size = sum(size for _, size in file_list)
        self._log(f"共发现 {result.total_files} 个文件，"
                  f"总大小 {result.total_size / 1024 / 1024:.1f} MB")

        self._log("正在分配分卷...")
        volume_files = self.assign_volumes(file_list)
        result.volumes = len(volume_files)

        self._total_bytes = result.total_size
        self._bytes_done = 0
        self._last_progress = -1
        self._progress(0)

        max_workers = self._max_worker_count(result.volumes)
        self._log(f"将分为 {result.volumes} 卷打包（{max_workers} 线程并行）")

        os.makedirs(self.output_dir, exist_ok=True)
        completed = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for i, vol_files in enumerate(volume_files, 1):
                f = executor.submit(self._pack_one_volume, i, result.volumes, vol_files)
                futures[f] = i

            for future in as_completed(futures):
                if self._is_cancelled():
                    executor.shutdown(wait=False, cancel_futures=True)
                    self._log("用户取消了打包操作。")
                    raise RuntimeError("Operation cancelled.")

                vol_i, output_path, part_name, zip_size, file_count = future.result()
                result.output_files.append(output_path)
                completed += 1

                self._log(f"完成第 {vol_i}/{result.volumes} 卷: {part_name} "
                          f"({file_count} 个文件, {zip_size / 1024 / 1024:.1f} MB)")

        result.output_files.sort(key=self._volume_sort_key)
        self._progress(100)
        self._log(f"\n打包完成！共生成 {result.volumes} 个分卷。")

        result.manifest_file = self._generate_manifest(result)

        # 生成一键解压脚本
        self._generate_unpack_script(result)

        return result

    def _max_worker_count(self, volume_count: int) -> int:
        if volume_count <= 0:
            return 1
        return max(1, min(os.cpu_count() or 4, volume_count, MAX_PACK_WORKERS))

    def _volume_sort_key(self, path: str) -> int:
        import re
        match = re.search(r"_part(\d+)\.zip$", os.path.basename(path), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    def _generate_manifest(self, result: PackResult) -> str:
        manifest_path = os.path.join(self.output_dir, f"{self.folder_name}_manifest.json")
        payload = {
            "format_version": 1,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "base_name": self.folder_name,
            "volume_count": result.volumes,
            "volumes": [
                {
                    "name": os.path.basename(path),
                    "size": os.path.getsize(path),
                }
                for path in result.output_files
            ],
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        self._log(f"已生成分卷清单: {os.path.basename(manifest_path)}")
        return manifest_path

    def _generate_unpack_script(self, result: PackResult):
        """在输出目录生成一键全部解压的 bat 脚本"""
        if not result.output_files:
            return

        bat_path = os.path.join(self.output_dir, f"{self.folder_name}_一键全部解压.bat")
        folder_name = self._escape_batch_text(self.folder_name)
        lines = [
            "@echo off",
            "chcp 65001 >nul",
            'cd /d "%~dp0"',
            f'echo 正在解压 "{folder_name}" 的全部 {result.volumes} 个分卷...',
            f'set "OUT_DIR=%cd%\\{folder_name}"',
            'mkdir "%OUT_DIR%" 2>nul',
            "",
        ]

        for filepath in result.output_files:
            zip_name = os.path.basename(filepath)
            zip_name_for_batch = self._escape_batch_text(zip_name)
            zip_name_for_powershell = self._escape_batch_text(self._escape_powershell_single_quoted(zip_name))
            lines.append(f'echo 解压: "{zip_name_for_batch}"')
            lines.append(
                f'powershell -NoProfile -Command "'
                f"Expand-Archive -LiteralPath '.\\{zip_name_for_powershell}' "
                f'-DestinationPath $env:OUT_DIR -Force"'
            )

        lines.extend([
            "",
            "echo.",
            "echo 全部解压完成！",
            "pause",
        ])

        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        self._log(f"已生成一键解压脚本: {os.path.basename(bat_path)}")

    def _escape_batch_text(self, value: str) -> str:
        return value.replace("%", "%%")

    def _escape_powershell_single_quoted(self, value: str) -> str:
        return value.replace("'", "''")
