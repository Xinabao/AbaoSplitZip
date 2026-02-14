"""
AbaoZip GUI 主窗口
"""

import os
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QRadioButton, QSpinBox, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)

from core.packer import COMPRESSION_LEVELS, VolumePacker
from core.unpacker import VolumeUnpacker


class PackWorker(QThread):
    """后台打包线程"""
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, packer: VolumePacker):
        super().__init__()
        self.packer = packer
        self._cancelled = False

    def run(self):
        self.packer.log_callback = self.log.emit
        self.packer.progress_callback = self.progress.emit
        self.packer.cancel_check = lambda: self._cancelled
        try:
            result = self.packer.pack()
            if self._cancelled:
                self.finished.emit(False, "已取消")
            else:
                self.finished.emit(True, f"完成，共 {result.volumes} 卷")
        except Exception as e:
            self.finished.emit(False, str(e))

    def cancel(self):
        self._cancelled = True


class UnpackWorker(QThread):
    """后台解压线程"""
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, unpacker: VolumeUnpacker):
        super().__init__()
        self.unpacker = unpacker
        self._cancelled = False

    def run(self):
        self.unpacker.log_callback = self.log.emit
        self.unpacker.progress_callback = self.progress.emit
        self.unpacker.cancel_check = lambda: self._cancelled
        try:
            result = self.unpacker.unpack()
            if self._cancelled:
                self.finished.emit(False, "已取消")
            else:
                self.finished.emit(True, f"完成，共解压 {result.total_files} 个文件")
        except Exception as e:
            self.finished.emit(False, str(e))

    def cancel(self):
        self._cancelled = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setWindowTitle("AbaoZip — 分卷独立解压打包工具")
        self.setMinimumWidth(620)
        self.setMinimumHeight(700)
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        # ── 顶部标题 ──
        title = QLabel("AbaoZip 分卷打包工具")
        title.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("将大文件夹按指定大小分卷打包，每个分卷都是独立的 ZIP，可单独解压。\n"
                      "打包完成后会同时生成「一键全部解压.bat」脚本，如需一次性解压所有分卷请运行该脚本。")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 6px;")
        layout.addWidget(desc)

        # ── 标签页 ──
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_pack_tab(), "📦 打包")
        self.tabs.addTab(self._create_unpack_tab(), "📂 解压")
        layout.addWidget(self.tabs)

        # ── 进度条 ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # ── 日志 ──
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setFixedHeight(160)
        self.log_text.setPlaceholderText("日志将显示在这里...")
        layout.addWidget(self.log_text)

    # ── 打包标签页 ──

    def _create_pack_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 路径设置
        path_group = QGroupBox("路径设置")
        path_layout = QVBoxLayout(path_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("源文件夹:"))
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("选择要打包的文件夹")
        row1.addWidget(self.source_edit)
        btn_src = QPushButton("浏览...")
        btn_src.setFixedWidth(70)
        btn_src.clicked.connect(self._browse_source)
        row1.addWidget(btn_src)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("输出目录:"))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("选择分卷压缩包的保存位置")
        row2.addWidget(self.output_edit)
        btn_out = QPushButton("浏览...")
        btn_out.setFixedWidth(70)
        btn_out.clicked.connect(self._browse_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 打包设置
        settings_group = QGroupBox("打包设置")
        settings_layout = QVBoxLayout(settings_group)

        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("分卷大小:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 999999)
        self.size_spin.setValue(700)
        self.size_spin.setSuffix(" MB")
        self.size_spin.setFixedWidth(120)
        size_row.addWidget(self.size_spin)
        size_hint = QLabel("每卷的目标大小（实际会略有偏差以保证文件完整）")
        size_hint.setStyleSheet("color: #888; font-size: 11px;")
        size_row.addWidget(size_hint)
        size_row.addStretch()
        settings_layout.addLayout(size_row)

        comp_row = QHBoxLayout()
        comp_row.addWidget(QLabel("压缩级别:"))
        self.comp_combo = QComboBox()
        self.comp_combo.addItems(COMPRESSION_LEVELS.keys())
        self.comp_combo.setCurrentText("标准压缩")
        self.comp_combo.setFixedWidth(180)
        comp_row.addWidget(self.comp_combo)
        comp_row.addStretch()
        settings_layout.addLayout(comp_row)

        layout.addWidget(settings_group)

        # 密码与加密
        pwd_group = QGroupBox("密码与加密（可选）")
        pwd_layout = QVBoxLayout(pwd_group)

        pwd_row = QHBoxLayout()
        pwd_row.addWidget(QLabel("密码:"))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setPlaceholderText("留空则不加密")
        pwd_row.addWidget(self.pwd_edit)
        pwd_layout.addLayout(pwd_row)

        self.radio_zipcrypto = QRadioButton("ZipCrypto")
        self.radio_zipcrypto.setChecked(True)
        zipcrypto_hint = QLabel("  ✅ Windows 10/11 资源管理器可直接解压，安全性一般")
        zipcrypto_hint.setStyleSheet("color: #888; font-size: 11px;")

        self.radio_aes = QRadioButton("AES-256")
        aes_hint = QLabel("  🔒 安全性高，需用 7-Zip / WinRAR 等工具解压")
        aes_hint.setStyleSheet("color: #888; font-size: 11px;")

        enc_row1 = QHBoxLayout()
        enc_row1.addWidget(self.radio_zipcrypto)
        enc_row1.addWidget(zipcrypto_hint)
        enc_row1.addStretch()
        pwd_layout.addLayout(enc_row1)

        enc_row2 = QHBoxLayout()
        enc_row2.addWidget(self.radio_aes)
        enc_row2.addWidget(aes_hint)
        enc_row2.addStretch()
        pwd_layout.addLayout(enc_row2)

        layout.addWidget(pwd_group)

        # 操作按钮
        btn_row = QHBoxLayout()
        self.btn_start = QPushButton("▶ 开始打包")
        self.btn_start.setFixedHeight(36)
        self.btn_start.setStyleSheet(
            "QPushButton { background-color: #0078d4; color: white; font-size: 13px; "
            "font-weight: bold; border-radius: 4px; }"
            "QPushButton:hover { background-color: #006abc; }"
            "QPushButton:disabled { background-color: #ccc; }"
        )
        self.btn_start.clicked.connect(self._start_pack)
        btn_row.addWidget(self.btn_start)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setFixedHeight(36)
        self.btn_cancel.setFixedWidth(80)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_cancel)
        layout.addLayout(btn_row)

        return tab

    # ── 解压标签页 ──

    def _create_unpack_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        desc = QLabel("选择任意一个分卷文件（如 XXX_part001.zip），将自动识别并解压同组的所有分卷。\n"
                      "也可以解压单个普通 ZIP 文件。")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 8px;")
        layout.addWidget(desc)

        # 路径设置
        path_group = QGroupBox("路径设置")
        path_layout = QVBoxLayout(path_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("选择分卷:"))
        self.unpack_zip_edit = QLineEdit()
        self.unpack_zip_edit.setPlaceholderText("选择任意一个分卷 ZIP 文件")
        row1.addWidget(self.unpack_zip_edit)
        btn_zip = QPushButton("浏览...")
        btn_zip.setFixedWidth(70)
        btn_zip.clicked.connect(self._browse_zip)
        row1.addWidget(btn_zip)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("解压到:"))
        self.unpack_output_edit = QLineEdit()
        self.unpack_output_edit.setPlaceholderText("选择解压目标目录")
        row2.addWidget(self.unpack_output_edit)
        btn_out = QPushButton("浏览...")
        btn_out.setFixedWidth(70)
        btn_out.clicked.connect(self._browse_unpack_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 密码
        pwd_group = QGroupBox("密码（如果压缩包有密码）")
        pwd_layout = QHBoxLayout(pwd_group)
        pwd_layout.addWidget(QLabel("密码:"))
        self.unpack_pwd_edit = QLineEdit()
        self.unpack_pwd_edit.setEchoMode(QLineEdit.Password)
        self.unpack_pwd_edit.setPlaceholderText("留空则不使用密码")
        pwd_layout.addWidget(self.unpack_pwd_edit)
        layout.addWidget(pwd_group)

        # 操作按钮
        btn_row = QHBoxLayout()
        self.btn_unpack = QPushButton("▶ 开始解压")
        self.btn_unpack.setFixedHeight(36)
        self.btn_unpack.setStyleSheet(
            "QPushButton { background-color: #107c10; color: white; font-size: 13px; "
            "font-weight: bold; border-radius: 4px; }"
            "QPushButton:hover { background-color: #0b5e0b; }"
            "QPushButton:disabled { background-color: #ccc; }"
        )
        self.btn_unpack.clicked.connect(self._start_unpack)
        btn_row.addWidget(self.btn_unpack)

        self.btn_unpack_cancel = QPushButton("取消")
        self.btn_unpack_cancel.setFixedHeight(36)
        self.btn_unpack_cancel.setFixedWidth(80)
        self.btn_unpack_cancel.setEnabled(False)
        self.btn_unpack_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_unpack_cancel)
        layout.addLayout(btn_row)

        layout.addStretch()
        return tab

    # ── 槽函数 ──

    def _browse_source(self):
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if path:
            self.source_edit.setText(path)

    def _browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_edit.setText(path)

    def _browse_zip(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择分卷 ZIP 文件", "", "ZIP 文件 (*.zip)")
        if path:
            self.unpack_zip_edit.setText(path)

    def _browse_unpack_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择解压目标目录")
        if path:
            self.unpack_output_edit.setText(path)

    def _set_buttons_enabled(self, enabled: bool):
        self.btn_start.setEnabled(enabled)
        self.btn_unpack.setEnabled(enabled)
        self.btn_cancel.setEnabled(not enabled)
        self.btn_unpack_cancel.setEnabled(not enabled)

    def _start_pack(self):
        source = self.source_edit.text().strip()
        output = self.output_edit.text().strip()

        if not source or not os.path.isdir(source):
            QMessageBox.warning(self, "提示", "请选择有效的源文件夹。")
            return
        if not output:
            QMessageBox.warning(self, "提示", "请选择输出目录。")
            return

        password = self.pwd_edit.text() or None
        encryption = "aes256" if self.radio_aes.isChecked() else "zipcrypto"

        packer = VolumePacker(
            source_dir=source,
            output_dir=output,
            volume_size_mb=self.size_spin.value(),
            password=password,
            compression_name=self.comp_combo.currentText(),
            encryption_method=encryption,
        )

        self.log_text.clear()
        self.progress_bar.setValue(0)
        self._set_buttons_enabled(False)

        self.worker = PackWorker(packer)
        self.worker.log.connect(self._on_log)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _start_unpack(self):
        zip_path = self.unpack_zip_edit.text().strip()
        output = self.unpack_output_edit.text().strip()

        if not zip_path or not os.path.isfile(zip_path):
            QMessageBox.warning(self, "提示", "请选择有效的 ZIP 文件。")
            return
        if not output:
            QMessageBox.warning(self, "提示", "请选择解压目标目录。")
            return

        password = self.unpack_pwd_edit.text() or None

        unpacker = VolumeUnpacker(
            first_zip=zip_path,
            output_dir=output,
            password=password,
        )

        self.log_text.clear()
        self.progress_bar.setValue(0)
        self._set_buttons_enabled(False)

        self.worker = UnpackWorker(unpacker)
        self.worker.log.connect(self._on_log)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _cancel(self):
        if self.worker:
            self.worker.cancel()

    def _on_log(self, msg: str):
        self.log_text.append(msg)

    def _on_finished(self, success: bool, msg: str):
        self._set_buttons_enabled(True)
        if success:
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "完成", msg)
        else:
            QMessageBox.warning(self, "提示", f"操作未完成：{msg}")
        self.worker = None
