"""
AbaoZip 核心打包逻辑
将文件夹按指定大小分卷打包为独立可解压的 ZIP 文件
"""

import os
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional

import pyzipper

# 压缩级别映射
COMPRESSION_LEVELS = {
    "仅存储 (最快)": (zipfile.ZIP_STORED, 0),
    "快速压缩": (zipfile.ZIP_DEFLATED, 1),
    "标准压缩": (zipfile.ZIP_DEFLATED, 6),
    "最大压缩 (最慢)": (zipfile.ZIP_DEFLATED, 9),
}

# 加密方式映射
ENCRYPTION_METHODS = {
    "ZipCrypto (兼容 Windows 资源管理器)": "zipcrypto",
    "AES-256 (更安全，需第三方解压工具)": "aes256",
}


@dataclass
class PackResult:
    """打包结果"""
    total_files: int = 0
    total_size: int = 0
    volumes: int = 0
    output_files: list = field(default_factory=list)


class VolumePacker:
    """分卷打包器"""

    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        volume_size_mb: float,
        password: Optional[str] = None,
        compression_name: str = "标准压缩",
        encryption_method: str = "zipcrypto",
        progress_callback=None,
        log_callback=None,
        cancel_check=None,
    ):
        self.source_dir = os.path.normpath(source_dir)
        self.output_dir = os.path.normpath(output_dir)
        self.volume_size_bytes = int(volume_size_mb * 1024 * 1024)
        self.password = password.encode("utf-8") if password else None
        self.compression_name = compression_name
        self.encryption_method = encryption_method
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_check = cancel_check

        comp = COMPRESSION_LEVELS.get(compression_name, COMPRESSION_LEVELS["标准压缩"])
        self.compression_type = comp[0]
        self.compression_level = comp[1]

        self.folder_name = os.path.basename(self.source_dir)

    def _log(self, msg: str):
        if self.log_callback:
            self.log_callback(msg)

    def _progress(self, value: int):
        if self.progress_callback:
            self.progress_callback(value)

    def _is_cancelled(self) -> bool:
        if self.cancel_check:
            return self.cancel_check()
        return False

    def scan_files(self) -> list:
        """扫描源文件夹，返回 (相对路径, 文件大小) 列表"""
        file_list = []
        for root, _dirs, files in os.walk(self.source_dir):
            for fname in files:
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, self.source_dir)
                size = os.path.getsize(full_path)
                file_list.append((rel_path, size))
        # 按大小降序排列，大文件优先分配（贪心装箱）
        file_list.sort(key=lambda x: x[1], reverse=True)
        return file_list

    def assign_volumes(self, file_list: list) -> list:
        """
        将文件分配到各分卷（首次适配递减算法）
        返回: [ [rel_path, ...], ... ] 每卷包含的文件列表
        """
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

    def _create_zip(self, output_path: str, file_paths: list):
        """创建单个 ZIP 分卷"""
        if self.password:
            if self.encryption_method == "aes256":
                encryption = pyzipper.WZ_AES
            else:
                encryption = pyzipper.ZIP_CRYPTO
            with pyzipper.ZipFile(
                output_path, "w",
                compression=self.compression_type,
                encryption=encryption,
            ) as zf:
                zf.setpassword(self.password)
                if self.compression_type == zipfile.ZIP_DEFLATED:
                    zf.compresslevel = self.compression_level
                for rel_path in file_paths:
                    full_path = os.path.join(self.source_dir, rel_path)
                    arcname = os.path.join(self.folder_name, rel_path)
                    zf.write(full_path, arcname)
        else:
            # 无密码，使用标准 zipfile
            with zipfile.ZipFile(
                output_path, "w",
                compression=self.compression_type,
                compresslevel=self.compression_level if self.compression_type == zipfile.ZIP_DEFLATED else None,
            ) as zf:
                for rel_path in file_paths:
                    full_path = os.path.join(self.source_dir, rel_path)
                    arcname = os.path.join(self.folder_name, rel_path)
                    zf.write(full_path, arcname)

    def _pack_one_volume(self, i: int, total: int, vol_files: list):
        """打包单个分卷（供线程池调用）"""
        part_name = f"{self.folder_name}_part{i:03d}.zip"
        output_path = os.path.join(self.output_dir, part_name)
        self._create_zip(output_path, vol_files)
        zip_size = os.path.getsize(output_path)
        return i, output_path, part_name, zip_size, len(vol_files)

    def pack(self) -> PackResult:
        """执行打包（多线程并行压缩各分卷）"""
        result = PackResult()

        self._log("正在扫描文件夹...")
        file_list = self.scan_files()
        if not file_list:
            self._log("错误：源文件夹为空，没有可打包的文件。")
            return result

        result.total_files = len(file_list)
        result.total_size = sum(size for _, size in file_list)
        self._log(f"共发现 {result.total_files} 个文件，"
                  f"总大小 {result.total_size / 1024 / 1024:.1f} MB")

        self._log("正在分配分卷...")
        volume_files = self.assign_volumes(file_list)
        result.volumes = len(volume_files)

        max_workers = min(os.cpu_count() or 4, result.volumes)
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
                    return result

                vol_i, output_path, part_name, zip_size, file_count = future.result()
                result.output_files.append(output_path)
                completed += 1

                progress = int(completed / result.volumes * 100)
                self._progress(progress)
                self._log(f"完成第 {vol_i}/{result.volumes} 卷: {part_name} "
                          f"({file_count} 个文件, {zip_size / 1024 / 1024:.1f} MB)")

        result.output_files.sort()
        self._log(f"\n打包完成！共生成 {result.volumes} 个分卷。")

        # 生成一键解压脚本
        self._generate_unpack_script(result)

        return result

    def _generate_unpack_script(self, result: PackResult):
        """在输出目录生成一键全部解压的 bat 脚本"""
        if not result.output_files:
            return

        bat_path = os.path.join(self.output_dir, f"{self.folder_name}_一键全部解压.bat")
        lines = [
            "@echo off",
            "chcp 65001 >nul",
            'cd /d "%~dp0"',
            f'echo 正在解压 {self.folder_name} 的全部 {result.volumes} 个分卷...',
            f'set "OUT_DIR=%cd%\\{self.folder_name}"',
            'mkdir "%OUT_DIR%" 2>nul',
            "",
        ]

        for filepath in result.output_files:
            zip_name = os.path.basename(filepath)
            lines.append(f'echo 解压: {zip_name}')
            lines.append(f'powershell -Command "Expand-Archive -Path \'.\\{zip_name}\' -DestinationPath \'%OUT_DIR%\' -Force"')

        lines.extend([
            "",
            "echo.",
            "echo 全部解压完成！",
            "pause",
        ])

        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        self._log(f"已生成一键解压脚本: {os.path.basename(bat_path)}")
