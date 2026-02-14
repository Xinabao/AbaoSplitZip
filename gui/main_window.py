"""
AbaoZip GUI 主窗口 (i18n)
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
from core.unpacker import VolumeUnpacker, get_file_filter, SUPPORTED_EXTENSIONS
from core.i18n import t, set_language, get_language, detect_system_language, LANGUAGES

# Mapping from i18n key to the original Chinese key used in COMPRESSION_LEVELS
_COMP_KEYS = [
    ("compression_store", "仅存储 (最快)"),
    ("compression_fast", "快速压缩"),
    ("compression_normal", "标准压缩"),
    ("compression_max", "最大压缩 (最慢)"),
]


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
        self._comp_keys = _COMP_KEYS

        # Auto-detect system language
        detected = detect_system_language()
        set_language(detected)

        self.setMinimumWidth(620)
        self.setMinimumHeight(700)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(t("app_title"))

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        # ── 顶部标题栏（标题 + 语言选择器） ──
        header_row = QHBoxLayout()
        title = QLabel(t("header_title"))
        title.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header_row.addStretch()
        header_row.addWidget(title)
        header_row.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.setFixedWidth(120)
        lang_names = list(LANGUAGES.keys())
        self.lang_combo.addItems(lang_names)
        # Pre-select the current language
        current_code = get_language()
        for name, code in LANGUAGES.items():
            if code == current_code:
                self.lang_combo.setCurrentText(name)
                break
        self.lang_combo.currentTextChanged.connect(self._on_language_changed)
        header_row.addWidget(self.lang_combo)
        layout.addLayout(header_row)

        desc = QLabel(t("header_desc") + '<br>'
                      '<b style="color: red;">' + t("header_bat_hint") + '</b>')
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 6px;")
        layout.addWidget(desc)

        # ── 标签页 ──
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_pack_tab(), t("tab_pack"))
        self.tabs.addTab(self._create_unpack_tab(), t("tab_unpack"))
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
        self.log_text.setPlaceholderText(t("log_placeholder"))
        layout.addWidget(self.log_text)

    # ── 打包标签页 ──

    def _create_pack_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 路径设置
        path_group = QGroupBox(t("group_paths"))
        path_layout = QVBoxLayout(path_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(t("label_source")))
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText(t("hint_source"))
        row1.addWidget(self.source_edit)
        btn_src = QPushButton(t("browse"))
        btn_src.setFixedWidth(105)
        btn_src.clicked.connect(self._browse_source)
        row1.addWidget(btn_src)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(t("label_output")))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText(t("hint_output"))
        row2.addWidget(self.output_edit)
        btn_out = QPushButton(t("browse"))
        btn_out.setFixedWidth(105)
        btn_out.clicked.connect(self._browse_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 打包设置
        settings_group = QGroupBox(t("group_settings"))
        settings_layout = QVBoxLayout(settings_group)

        size_row = QHBoxLayout()
        size_row.addWidget(QLabel(t("label_volume_size")))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 999999)
        self.size_spin.setValue(700)
        self.size_spin.setSuffix(" MB")
        self.size_spin.setFixedWidth(120)
        size_row.addWidget(self.size_spin)
        size_hint = QLabel(t("hint_volume_size"))
        size_hint.setStyleSheet("color: #888; font-size: 15px;")
        size_row.addWidget(size_hint)
        size_row.addStretch()
        settings_layout.addLayout(size_row)

        comp_row = QHBoxLayout()
        comp_row.addWidget(QLabel(t("label_compression")))
        self.comp_combo = QComboBox()
        for i18n_key, _orig_key in self._comp_keys:
            self.comp_combo.addItem(t(i18n_key))
        self.comp_combo.setCurrentIndex(2)  # "标准压缩" / Normal compression
        self.comp_combo.setFixedWidth(220)
        comp_row.addWidget(self.comp_combo)
        comp_row.addStretch()
        settings_layout.addLayout(comp_row)

        layout.addWidget(settings_group)

        # 密码与加密
        pwd_group = QGroupBox(t("group_password"))
        pwd_layout = QVBoxLayout(pwd_group)

        pwd_row = QHBoxLayout()
        pwd_row.addWidget(QLabel(t("label_password")))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setPlaceholderText(t("hint_password"))
        pwd_row.addWidget(self.pwd_edit)
        pwd_layout.addLayout(pwd_row)

        self.radio_zipcrypto = QRadioButton("ZipCrypto")
        self.radio_zipcrypto.setChecked(True)
        zipcrypto_hint = QLabel(t("enc_zipcrypto"))
        zipcrypto_hint.setStyleSheet("color: #888; font-size: 15px;")

        self.radio_aes = QRadioButton("AES-256")
        aes_hint = QLabel(t("enc_aes"))
        aes_hint.setStyleSheet("color: #888; font-size: 15px;")

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
        self.btn_start = QPushButton(t("btn_start_pack"))
        self.btn_start.setFixedHeight(36)
        self.btn_start.setStyleSheet(
            "QPushButton { background-color: #0078d4; color: white; font-size: 13px; "
            "font-weight: bold; border-radius: 4px; }"
            "QPushButton:hover { background-color: #006abc; }"
            "QPushButton:disabled { background-color: #ccc; }"
        )
        self.btn_start.clicked.connect(self._start_pack)
        btn_row.addWidget(self.btn_start)

        self.btn_cancel = QPushButton(t("btn_cancel"))
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

        desc = QLabel(t("unpack_desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; font-size: 15px; margin-bottom: 8px;")
        layout.addWidget(desc)

        # 支持格式提示
        fmt_parts = ["ZIP"]
        if ".7z" in SUPPORTED_EXTENSIONS:
            fmt_parts.append("7z")
        if ".rar" in SUPPORTED_EXTENSIONS:
            fmt_parts.append("RAR")
        fmt_label = QLabel(t("unpack_formats") + " " + " / ".join(fmt_parts))
        fmt_label.setStyleSheet("color: #0078d4; font-size: 15px; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(fmt_label)

        # 路径设置
        path_group = QGroupBox(t("group_paths"))
        path_layout = QVBoxLayout(path_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(t("label_select_zip")))
        self.unpack_zip_edit = QLineEdit()
        self.unpack_zip_edit.setPlaceholderText(t("hint_select_zip"))
        row1.addWidget(self.unpack_zip_edit)
        btn_zip = QPushButton(t("browse"))
        btn_zip.setFixedWidth(105)
        btn_zip.clicked.connect(self._browse_zip)
        row1.addWidget(btn_zip)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(t("label_extract_to")))
        self.unpack_output_edit = QLineEdit()
        self.unpack_output_edit.setPlaceholderText(t("hint_extract_to"))
        row2.addWidget(self.unpack_output_edit)
        btn_out = QPushButton(t("browse"))
        btn_out.setFixedWidth(105)
        btn_out.clicked.connect(self._browse_unpack_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 密码
        pwd_group = QGroupBox(t("group_unpack_password"))
        pwd_layout = QHBoxLayout(pwd_group)
        pwd_layout.addWidget(QLabel(t("label_password")))
        self.unpack_pwd_edit = QLineEdit()
        self.unpack_pwd_edit.setEchoMode(QLineEdit.Password)
        self.unpack_pwd_edit.setPlaceholderText(t("hint_unpack_password"))
        pwd_layout.addWidget(self.unpack_pwd_edit)
        layout.addWidget(pwd_group)

        # 操作按钮
        btn_row = QHBoxLayout()
        self.btn_unpack = QPushButton(t("btn_start_unpack"))
        self.btn_unpack.setFixedHeight(36)
        self.btn_unpack.setStyleSheet(
            "QPushButton { background-color: #107c10; color: white; font-size: 13px; "
            "font-weight: bold; border-radius: 4px; }"
            "QPushButton:hover { background-color: #0b5e0b; }"
            "QPushButton:disabled { background-color: #ccc; }"
        )
        self.btn_unpack.clicked.connect(self._start_unpack)
        btn_row.addWidget(self.btn_unpack)

        self.btn_unpack_cancel = QPushButton(t("btn_cancel"))
        self.btn_unpack_cancel.setFixedHeight(36)
        self.btn_unpack_cancel.setFixedWidth(80)
        self.btn_unpack_cancel.setEnabled(False)
        self.btn_unpack_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_unpack_cancel)
        layout.addLayout(btn_row)

        layout.addStretch()
        return tab

    # ── 语言切换 ──

    def _on_language_changed(self, lang_name: str):
        code = LANGUAGES.get(lang_name)
        if code and code != get_language():
            set_language(code)
            self._rebuild_ui()

    def _rebuild_ui(self):
        """Save state, rebuild all UI, restore state."""
        # Save current state
        source = self.source_edit.text()
        output = self.output_edit.text()
        password = self.pwd_edit.text()
        volume_size = self.size_spin.value()
        comp_index = self.comp_combo.currentIndex()
        aes_checked = self.radio_aes.isChecked()
        tab_index = self.tabs.currentIndex()
        unpack_zip = self.unpack_zip_edit.text()
        unpack_output = self.unpack_output_edit.text()
        unpack_pwd = self.unpack_pwd_edit.text()
        log_content = self.log_text.toHtml()
        progress_val = self.progress_bar.value()

        # Rebuild
        self._init_ui()

        # Restore state
        self.source_edit.setText(source)
        self.output_edit.setText(output)
        self.pwd_edit.setText(password)
        self.size_spin.setValue(volume_size)
        self.comp_combo.setCurrentIndex(comp_index)
        if aes_checked:
            self.radio_aes.setChecked(True)
        else:
            self.radio_zipcrypto.setChecked(True)
        self.tabs.setCurrentIndex(tab_index)
        self.unpack_zip_edit.setText(unpack_zip)
        self.unpack_output_edit.setText(unpack_output)
        self.unpack_pwd_edit.setText(unpack_pwd)
        self.log_text.setHtml(log_content)
        self.progress_bar.setValue(progress_val)

    # ── 槽函数 ──

    def _browse_source(self):
        path = QFileDialog.getExistingDirectory(self, t("dialog_select_source"))
        if path:
            self.source_edit.setText(path)

    def _browse_output(self):
        path = QFileDialog.getExistingDirectory(self, t("dialog_select_output"))
        if path:
            self.output_edit.setText(path)

    def _browse_zip(self):
        path, _ = QFileDialog.getOpenFileName(
            self, t("dialog_select_zip"), "", get_file_filter())
        if path:
            self.unpack_zip_edit.setText(path)

    def _browse_unpack_output(self):
        path = QFileDialog.getExistingDirectory(self, t("dialog_select_extract"))
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
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_source"))
            return
        if not output:
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_output"))
            return

        password = self.pwd_edit.text() or None
        encryption = "aes256" if self.radio_aes.isChecked() else "zipcrypto"

        # Map localized combo index back to original Chinese key for VolumePacker
        comp_index = self.comp_combo.currentIndex()
        compression_name = self._comp_keys[comp_index][1]

        packer = VolumePacker(
            source_dir=source,
            output_dir=output,
            volume_size_mb=self.size_spin.value(),
            password=password,
            compression_name=compression_name,
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
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_archive"))
            return
        if not output:
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_output"))
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
            QMessageBox.information(self, t("msg_done"), msg)
        else:
            QMessageBox.warning(self, t("msg_hint"), t("msg_incomplete") + msg)
        self.worker = None
