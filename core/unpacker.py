"""
AbaoZip 解压逻辑
识别并解压同一组分卷压缩包
"""

import os
import re
import zipfile
from dataclasses import dataclass, field
from typing import Optional

import pyzipper


@dataclass
class UnpackResult:
    """解压结果"""
    total_files: int = 0
    volumes: int = 0
    output_dir: str = ""


class VolumeUnpacker:
    """分卷解压器"""

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
        self.password = password.encode("utf-8") if password else None
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

    def find_volumes(self) -> list:
        """根据第一个 zip 找到同组的所有分卷，按序号排列"""
        zip_dir = os.path.dirname(self.first_zip)
        zip_name = os.path.basename(self.first_zip)

        # 匹配命名格式: XXX_part001.zip
        match = re.match(r"^(.+)_part(\d+)\.zip$", zip_name, re.IGNORECASE)
        if not match:
            # 不是分卷格式，当作单个 zip 处理
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

    def _extract_zip(self, zip_path: str):
        """解压单个 zip，自动检测是否加密"""
        try:
            # 先尝试用 pyzipper（支持加密格式）
            with pyzipper.ZipFile(zip_path, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)
                zf.extractall(self.output_dir)
                return len(zf.namelist())
        except Exception:
            # 回退到标准 zipfile
            with zipfile.ZipFile(zip_path, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)
                zf.extractall(self.output_dir)
                return len(zf.namelist())

    def unpack(self) -> UnpackResult:
        """执行解压"""
        result = UnpackResult()
        result.output_dir = self.output_dir

        self._log("正在查找分卷文件...")
        volumes = self.find_volumes()
        result.volumes = len(volumes)

        if not volumes:
            self._log("错误：未找到匹配的分卷文件。")
            return result

        self._log(f"共找到 {result.volumes} 个分卷")
        os.makedirs(self.output_dir, exist_ok=True)

        for i, vol_path in enumerate(volumes, 1):
            if self._is_cancelled():
                self._log("用户取消了解压操作。")
                return result

            vol_name = os.path.basename(vol_path)
            self._log(f"正在解压第 {i}/{result.volumes} 卷: {vol_name}")

            try:
                count = self._extract_zip(vol_path)
                result.total_files += count
                self._log(f"  完成 — {count} 个文件")
            except RuntimeError as e:
                if "password" in str(e).lower() or "Bad password" in str(e):
                    self._log(f"  错误：密码不正确或缺少密码")
                    return result
                raise
            except Exception as e:
                self._log(f"  错误：{e}")
                return result

            progress = int(i / result.volumes * 100)
            self._progress(progress)

        self._log(f"\n解压完成！共解压 {result.total_files} 个文件到:\n{self.output_dir}")
        return result
