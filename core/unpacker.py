"""
AbaoZip 解压逻辑
支持 ZIP（含加密）、7z、RAR 格式
识别并解压同一组分卷压缩包
"""

import os
import re
import zipfile
from dataclasses import dataclass
from typing import Optional

import pyzipper

# 可选依赖
try:
    import py7zr
    HAS_7Z = True
except ImportError:
    HAS_7Z = False

try:
    import rarfile
    HAS_RAR = True
except ImportError:
    HAS_RAR = False


# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".zip"}
if HAS_7Z:
    SUPPORTED_EXTENSIONS.add(".7z")
if HAS_RAR:
    SUPPORTED_EXTENSIONS.add(".rar")


def get_file_filter() -> str:
    """返回文件对话框的过滤器字符串"""
    parts = ["ZIP (*.zip)"]
    all_exts = ["*.zip"]
    if HAS_7Z:
        parts.append("7-Zip (*.7z)")
        all_exts.append("*.7z")
    if HAS_RAR:
        parts.append("RAR (*.rar)")
        all_exts.append("*.rar")
    all_str = " ".join(all_exts)
    return f"All Supported ({all_str});;" + ";;".join(parts)


@dataclass
class UnpackResult:
    """解压结果"""
    total_files: int = 0
    volumes: int = 0
    output_dir: str = ""


class VolumeUnpacker:
    """多格式解压器，支持 ZIP 分卷自动识别、7z、RAR"""

    def __init__(
        self,
        first_zip: str,
        output_dir: str,
        password: Optional[str] = None,
        progress_callback=None,
        log_callback=None,
        cancel_check=None,
    ):
        self.first_zip = os.path.normpath(first_zip)
        self.output_dir = os.path.normpath(output_dir)
        self.password = password
        self.password_bytes = password.encode("utf-8") if password else None
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_check = cancel_check

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

    def _detect_format(self) -> str:
        """检测文件格式"""
        ext = os.path.splitext(self.first_zip)[1].lower()
        if ext == ".7z":
            return "7z"
        elif ext == ".rar":
            return "rar"
        return "zip"

    def find_volumes(self) -> list:
        """根据第一个 zip 找到同组的所有分卷，按序号排列"""
        zip_dir = os.path.dirname(self.first_zip)
        zip_name = os.path.basename(self.first_zip)

        # 匹配命名格式: XXX_part001.zip
        match = re.match(r"^(.+)_part(\d+)\.zip$", zip_name, re.IGNORECASE)
        if not match:
            return [self.first_zip]

        base_name = match.group(1)
        pattern = re.compile(
            rf"^{re.escape(base_name)}_part(\d+)\.zip$", re.IGNORECASE
        )

        volumes = []
        for f in os.listdir(zip_dir):
            m = pattern.match(f)
            if m:
                seq = int(m.group(1))
                volumes.append((seq, os.path.join(zip_dir, f)))

        volumes.sort(key=lambda x: x[0])
        return [path for _, path in volumes]

    def _extract_zip(self, zip_path: str) -> int:
        """解压单个 zip，自动检测是否加密"""
        try:
            with pyzipper.ZipFile(zip_path, "r") as zf:
                if self.password_bytes:
                    zf.setpassword(self.password_bytes)
                zf.extractall(self.output_dir)
                return len(zf.namelist())
        except Exception:
            with zipfile.ZipFile(zip_path, "r") as zf:
                if self.password_bytes:
                    zf.setpassword(self.password_bytes)
                zf.extractall(self.output_dir)
                return len(zf.namelist())

    def _extract_7z(self, path: str) -> int:
        """解压 7z 文件"""
        if not HAS_7Z:
            raise RuntimeError("py7zr not installed — cannot extract .7z files")
        with py7zr.SevenZipFile(path, mode="r", password=self.password or None) as sz:
            sz.extractall(path=self.output_dir)
            return len(sz.getnames())

    def _extract_rar(self, path: str) -> int:
        """解压 RAR 文件"""
        if not HAS_RAR:
            raise RuntimeError("rarfile not installed — cannot extract .rar files")
        with rarfile.RarFile(path, "r") as rf:
            if self.password:
                rf.setpassword(self.password)
            rf.extractall(self.output_dir)
            return len(rf.namelist())

    def unpack(self) -> UnpackResult:
        """执行解压"""
        result = UnpackResult()
        result.output_dir = self.output_dir

        fmt = self._detect_format()

        if fmt == "7z":
            self._log(f"7z: {os.path.basename(self.first_zip)}")
            os.makedirs(self.output_dir, exist_ok=True)
            try:
                count = self._extract_7z(self.first_zip)
                result.total_files = count
                result.volumes = 1
                self._progress(100)
                self._log(f"OK — {count} files")
            except Exception as e:
                self._log(f"Error: {e}")
            return result

        if fmt == "rar":
            self._log(f"RAR: {os.path.basename(self.first_zip)}")
            os.makedirs(self.output_dir, exist_ok=True)
            try:
                count = self._extract_rar(self.first_zip)
                result.total_files = count
                result.volumes = 1
                self._progress(100)
                self._log(f"OK — {count} files")
            except Exception as e:
                self._log(f"Error: {e}")
            return result

        # ZIP (with volume detection)
        self._log("Scanning volumes...")
        volumes = self.find_volumes()
        result.volumes = len(volumes)

        if not volumes:
            self._log("Error: no matching volumes found.")
            return result

        self._log(f"Found {result.volumes} volume(s)")
        os.makedirs(self.output_dir, exist_ok=True)

        for i, vol_path in enumerate(volumes, 1):
            if self._is_cancelled():
                self._log("Cancelled.")
                return result

            vol_name = os.path.basename(vol_path)
            self._log(f"Extracting {i}/{result.volumes}: {vol_name}")

            try:
                count = self._extract_zip(vol_path)
                result.total_files += count
                self._log(f"  OK — {count} files")
            except RuntimeError as e:
                if "password" in str(e).lower() or "Bad password" in str(e):
                    self._log(f"  Error: wrong password")
                    return result
                raise
            except Exception as e:
                self._log(f"  Error: {e}")
                return result

            progress = int(i / result.volumes * 100)
            self._progress(progress)

        self._log(f"\nDone! {result.total_files} files extracted to:\n{self.output_dir}")
        return result
