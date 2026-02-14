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
    QRadioButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)

from core.packer import COMPRESSION_LEVELS, VolumePacker


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setWindowTitle("AbaoZip — 分卷独立解压打包工具")
        self.setMinimumWidth(620)
        self.setMinimumHeight(680)
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

        desc = QLabel("将大文件夹按指定大小分卷打包，每个分卷都是独立的 ZIP，可单独解压。")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 6px;")
        layout.addWidget(desc)

        # ── 路径选择 ──
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

        # ── 打包设置 ──
        settings_group = QGroupBox("打包设置")
        settings_layout = QVBoxLayout(settings_group)

        # 分卷大小
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

        # 压缩级别
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

        # ── 密码与加密 ──
        pwd_group = QGroupBox("密码与加密（可选）")
        pwd_layout = QVBoxLayout(pwd_group)

        pwd_row = QHBoxLayout()
        pwd_row.addWidget(QLabel("密码:"))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setPlaceholderText("留空则不加密")
        pwd_row.addWidget(self.pwd_edit)
        pwd_layout.addLayout(pwd_row)

        # 加密方式单选 + 内嵌说明
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

        # ── 操作按钮 ──
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
        self.btn_cancel.clicked.connect(self._cancel_pack)
        btn_row.addWidget(self.btn_cancel)
        layout.addLayout(btn_row)

        # ── 进度条 ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # ── 日志 ──
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setFixedHeight(160)
        self.log_text.setPlaceholderText("打包日志将显示在这里...")
        layout.addWidget(self.log_text)

    # ── 槽函数 ──

    def _browse_source(self):
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if path:
            self.source_edit.setText(path)

    def _browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_edit.setText(path)

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
        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)

        self.worker = PackWorker(packer)
        self.worker.log.connect(self._on_log)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _cancel_pack(self):
        if self.worker:
            self.worker.cancel()

    def _on_log(self, msg: str):
        self.log_text.append(msg)

    def _on_finished(self, success: bool, msg: str):
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        if success:
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "完成", f"打包完成！{msg}")
        else:
            QMessageBox.warning(self, "提示", f"打包未完成：{msg}")
        self.worker = None
