"""
AbaoZip GUI 主窗口 (i18n)
"""

import os
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QIcon, QDesktopServices
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QRadioButton, QSpinBox, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)

from core.packer import COMPRESSION_LEVELS, VolumePacker
from core.unpacker import VolumeUnpacker, get_file_filter, SUPPORTED_EXTENSIONS
from core.i18n import t, set_language, get_language, detect_system_language, LANGUAGES
from gui.styles import MODERN_STYLE

# Mapping from i18n key to the original Chinese key used in COMPRESSION_LEVELS
_COMP_KEYS = [
    ("compression_store", "仅存储 (最快)"),
    ("compression_fast", "快速压缩"),
    ("compression_normal", "标准压缩"),
    ("compression_max", "最大压缩 (最慢)"),
]

class DragDropLineEdit(QLineEdit):
    """支持拖拽文件/文件夹的输入框"""
    def __init__(self, parent=None, is_folder=True):
        super().__init__(parent)
        self.is_folder = is_folder
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if self.is_folder and os.path.isdir(path):
                self.setText(path)
            elif not self.is_folder and os.path.isfile(path):
                self.setText(path)
            elif self.is_folder and os.path.isfile(path):
                # If expecting folder but got file, use parent dir
                self.setText(os.path.dirname(path))

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
        
        # Apply Style
        if QApplication.instance():
            QApplication.instance().setStyleSheet(MODERN_STYLE)

        # Auto-detect system language
        detected = detect_system_language()
        set_language(detected)

        self.setMinimumWidth(680)
        self.setMinimumHeight(760)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(t("app_title"))

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # ── 顶部标题栏（标题 + 语言选择器） ──
        header_row = QHBoxLayout()
        title = QLabel(t("header_title"))
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #333;")
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

        # About / Help Button
        self.btn_about = QPushButton("?")
        self.btn_about.setFixedWidth(30)
        self.btn_about.setToolTip(t("btn_about"))
        self.btn_about.clicked.connect(self._show_about)
        header_row.addWidget(self.btn_about)

        layout.addLayout(header_row)

        desc = QLabel(t("header_desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 6px; font-size: 13px;")
        layout.addWidget(desc)

        # ── 标签页 ──
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_pack_tab(), t("tab_pack"))
        self.tabs.addTab(self._create_unpack_tab(), t("tab_unpack"))
        self.tabs.addTab(self._create_merge_tab(), t("tab_merge"))  # New tab
        layout.addWidget(self.tabs)

        # ── 进度条 ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # ── 日志 ──
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setFixedHeight(120)
        self.log_text.setPlaceholderText(t("log_placeholder"))
        layout.addWidget(self.log_text)

    # ── 打包标签页 ──

    def _create_pack_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # 路径设置
        path_group = QGroupBox(t("group_paths"))
        path_layout = QVBoxLayout(path_group)
        path_layout.setSpacing(10)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(t("label_source")))
        self.source_edit = DragDropLineEdit(is_folder=True)
        self.source_edit.setPlaceholderText(t("hint_source"))
        row1.addWidget(self.source_edit)
        btn_src = QPushButton(t("browse"))
        btn_src.clicked.connect(self._browse_source)
        row1.addWidget(btn_src)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(t("label_output")))
        self.output_edit = DragDropLineEdit(is_folder=True)
        self.output_edit.setPlaceholderText(t("hint_output"))
        row2.addWidget(self.output_edit)
        btn_out = QPushButton(t("browse"))
        btn_out.clicked.connect(self._browse_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 打包设置
        settings_group = QGroupBox(t("group_settings"))
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(10)

        # Row: Size & Mode
        size_mode_row = QHBoxLayout()
        
        # Volume Size
        size_mode_row.addWidget(QLabel(t("label_volume_size")))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 999999)
        self.size_spin.setValue(700)
        self.size_spin.setSuffix(" MB")
        self.size_spin.setFixedWidth(100)
        size_mode_row.addWidget(self.size_spin)
        
        size_mode_row.addSpacing(20)

        # Mode
        size_mode_row.addWidget(QLabel(t("label_mode")))
        self.mode_combo = QComboBox()
        self.mode_combo.addItem(t("mode_size"), "size_balanced")
        self.mode_combo.addItem(t("mode_dir"), "directory_priority")
        self.mode_combo.setCurrentIndex(1) # Default to Directory Priority for better user experience
        size_mode_row.addWidget(self.mode_combo)
        
        size_mode_row.addStretch()
        settings_layout.addLayout(size_mode_row)

        # Row: Compression & Exclude
        comp_excl_row = QHBoxLayout()
        
        # Compression
        comp_excl_row.addWidget(QLabel(t("label_compression")))
        self.comp_combo = QComboBox()
        for i18n_key, _orig_key in self._comp_keys:
            self.comp_combo.addItem(t(i18n_key))
        self.comp_combo.setCurrentIndex(2)  # "标准压缩"
        self.comp_combo.setFixedWidth(150)
        comp_excl_row.addWidget(self.comp_combo)

        comp_excl_row.addSpacing(20)

        # Exclude
        comp_excl_row.addWidget(QLabel(t("label_exclude")))
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText(t("hint_exclude"))
        comp_excl_row.addWidget(self.exclude_edit)

        settings_layout.addLayout(comp_excl_row)

        layout.addWidget(settings_group)

        # 密码与加密
        pwd_group = QGroupBox(t("group_password"))
        pwd_layout = QHBoxLayout(pwd_group)
        
        pwd_layout.addWidget(QLabel(t("label_password")))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setPlaceholderText(t("hint_password"))
        self.pwd_edit.setFixedWidth(200)
        pwd_layout.addWidget(self.pwd_edit)

        pwd_layout.addSpacing(20)

        self.radio_zipcrypto = QRadioButton("ZipCrypto")
        self.radio_zipcrypto.setChecked(True)
        self.radio_aes = QRadioButton("AES-256")
        
        pwd_layout.addWidget(self.radio_zipcrypto)
        pwd_layout.addWidget(self.radio_aes)
        pwd_layout.addStretch()

        layout.addWidget(pwd_group)

        # 操作按钮
        btn_row = QHBoxLayout()
        self.btn_start = QPushButton(t("btn_start_pack"))
        self.btn_start.setObjectName("primary")
        self.btn_start.setFixedHeight(40)
        self.btn_start.clicked.connect(self._start_pack)
        btn_row.addWidget(self.btn_start)

        self.btn_cancel = QPushButton(t("btn_cancel"))
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setFixedWidth(100)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_cancel)
        
        self.btn_open = QPushButton(t("btn_open_folder"))
        self.btn_open.setFixedHeight(40)
        self.btn_open.setFixedWidth(140)
        self.btn_open.setEnabled(False)
        self.btn_open.clicked.connect(self._open_output_folder)
        btn_row.addWidget(self.btn_open)

        layout.addLayout(btn_row)

        return tab

    # ── 解压标签页 ──

    def _create_unpack_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        desc = QLabel(t("unpack_desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(desc)

        # 支持格式提示
        fmt_parts = ["ZIP"]
        if ".7z" in SUPPORTED_EXTENSIONS:
            fmt_parts.append("7z")
        if ".rar" in SUPPORTED_EXTENSIONS:
            fmt_parts.append("RAR")
        fmt_label = QLabel(t("unpack_formats") + " " + " / ".join(fmt_parts))
        fmt_label.setStyleSheet("color: #0078d4; font-weight: bold;")
        layout.addWidget(fmt_label)

        # 路径设置
        path_group = QGroupBox(t("group_paths"))
        path_layout = QVBoxLayout(path_group)
        path_layout.setSpacing(10)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(t("label_select_zip")))
        self.unpack_zip_edit = DragDropLineEdit(is_folder=False)
        self.unpack_zip_edit.setPlaceholderText(t("hint_select_zip"))
        row1.addWidget(self.unpack_zip_edit)
        btn_zip = QPushButton(t("browse"))
        btn_zip.clicked.connect(self._browse_zip)
        row1.addWidget(btn_zip)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(t("label_extract_to")))
        self.unpack_output_edit = DragDropLineEdit(is_folder=True)
        self.unpack_output_edit.setPlaceholderText(t("hint_extract_to"))
        row2.addWidget(self.unpack_output_edit)
        btn_out = QPushButton(t("browse"))
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
        self.btn_unpack.setObjectName("success")
        self.btn_unpack.setFixedHeight(40)
        self.btn_unpack.clicked.connect(self._start_unpack)
        btn_row.addWidget(self.btn_unpack)

        self.btn_unpack_cancel = QPushButton(t("btn_cancel"))
        self.btn_unpack_cancel.setFixedHeight(40)
        self.btn_unpack_cancel.setFixedWidth(100)
        self.btn_unpack_cancel.setEnabled(False)
        self.btn_unpack_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_unpack_cancel)
        layout.addLayout(btn_row)

        layout.addStretch()
        return tab

    # ── 合并解压标签页 ──

    def _create_merge_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        desc = QLabel(t("merge_desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(desc)

        # 路径设置
        path_group = QGroupBox(t("group_paths"))
        path_layout = QVBoxLayout(path_group)
        path_layout.setSpacing(10)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(t("label_select_part")))
        self.merge_zip_edit = DragDropLineEdit(is_folder=False)
        self.merge_zip_edit.setPlaceholderText(t("hint_select_part"))
        row1.addWidget(self.merge_zip_edit)
        btn_zip = QPushButton(t("browse"))
        btn_zip.clicked.connect(self._browse_merge_zip)
        row1.addWidget(btn_zip)
        path_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(t("label_extract_to")))
        self.merge_output_edit = DragDropLineEdit(is_folder=True)
        self.merge_output_edit.setPlaceholderText(t("hint_extract_to"))
        row2.addWidget(self.merge_output_edit)
        btn_out = QPushButton(t("browse"))
        btn_out.clicked.connect(self._browse_merge_output)
        row2.addWidget(btn_out)
        path_layout.addLayout(row2)

        layout.addWidget(path_group)

        # 密码
        pwd_group = QGroupBox(t("group_unpack_password"))
        pwd_layout = QHBoxLayout(pwd_group)
        pwd_layout.addWidget(QLabel(t("label_password")))
        self.merge_pwd_edit = QLineEdit()
        self.merge_pwd_edit.setEchoMode(QLineEdit.Password)
        self.merge_pwd_edit.setPlaceholderText(t("hint_unpack_password"))
        pwd_layout.addWidget(self.merge_pwd_edit)
        layout.addWidget(pwd_group)

        # 操作按钮
        btn_row = QHBoxLayout()
        self.btn_merge = QPushButton(t("btn_start_merge"))
        self.btn_merge.setObjectName("success")
        self.btn_merge.setFixedHeight(40)
        self.btn_merge.clicked.connect(self._start_merge)
        btn_row.addWidget(self.btn_merge)

        self.btn_merge_cancel = QPushButton(t("btn_cancel"))
        self.btn_merge_cancel.setFixedHeight(40)
        self.btn_merge_cancel.setFixedWidth(100)
        self.btn_merge_cancel.setEnabled(False)
        self.btn_merge_cancel.clicked.connect(self._cancel)
        btn_row.addWidget(self.btn_merge_cancel)
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
        
        # New states
        mode_idx = self.mode_combo.currentIndex()
        exclude = self.exclude_edit.text()
        
        merge_zip = self.merge_zip_edit.text()
        merge_out = self.merge_output_edit.text()
        merge_pwd = self.merge_pwd_edit.text()

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
        
        self.mode_combo.setCurrentIndex(mode_idx)
        self.exclude_edit.setText(exclude)
        
        self.merge_zip_edit.setText(merge_zip)
        self.merge_output_edit.setText(merge_out)
        self.merge_pwd_edit.setText(merge_pwd)

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
            
    def _browse_merge_zip(self):
        path, _ = QFileDialog.getOpenFileName(
            self, t("dialog_select_zip"), "", get_file_filter())
        if path:
            self.merge_zip_edit.setText(path)
            
    def _browse_merge_output(self):
        path = QFileDialog.getExistingDirectory(self, t("dialog_select_extract"))
        if path:
            self.merge_output_edit.setText(path)

    def _set_buttons_enabled(self, enabled: bool):
        self.btn_start.setEnabled(enabled)
        self.btn_unpack.setEnabled(enabled)
        self.btn_merge.setEnabled(enabled)
        self.btn_cancel.setEnabled(not enabled)
        self.btn_unpack_cancel.setEnabled(not enabled)
        self.btn_merge_cancel.setEnabled(not enabled)
        
        # Enable open folder only if finished and not running
        if enabled and (self.output_edit.text() or self.merge_output_edit.text()):
             self.btn_open.setEnabled(True)
        else:
             self.btn_open.setEnabled(False)

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
        
        mode = self.mode_combo.itemData(self.mode_combo.currentIndex())
        
        exclude_str = self.exclude_edit.text().strip()
        exclude_patterns = [p.strip() for p in exclude_str.split(",") if p.strip()]

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
            mode=mode,
            exclude_patterns=exclude_patterns,
        )

        self.log_text.clear()
        self.progress_bar.setValue(0)
        self._set_buttons_enabled(False)
        self.btn_open.setEnabled(False)

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
        
    def _start_merge(self):
        zip_path = self.merge_zip_edit.text().strip()
        output = self.merge_output_edit.text().strip()

        if not zip_path or not os.path.isfile(zip_path):
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_archive"))
            return
        if not output:
            QMessageBox.warning(self, t("msg_hint"), t("msg_select_output"))
            return

        password = self.merge_pwd_edit.text() or None

        # Re-use VolumeUnpacker - it already handles finding volumes!
        unpacker = VolumeUnpacker(
            first_zip=zip_path,
            output_dir=output,
            password=password,
        )

        self.log_text.clear()
        self.progress_bar.setValue(0)
        self._set_buttons_enabled(False)
        self.btn_open.setEnabled(False)

        self.worker = UnpackWorker(unpacker)
        self.worker.log.connect(self._on_log)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _show_about(self):
        """Show About dialog with help and link"""
        msg = QMessageBox(self)
        msg.setWindowTitle(t("about_title"))
        msg.setTextFormat(Qt.RichText)
        msg.setText(t("about_content"))
        msg.exec_()

    def _cancel(self):
        if self.worker:
            self.worker.cancel()

    def _open_output_folder(self):
        path = self.output_edit.text().strip()
        if path and os.path.isdir(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _on_log(self, msg: str):
        self.log_text.append(msg)

    def _on_finished(self, success: bool, msg: str):
        self._set_buttons_enabled(True)
        if success:
            self.progress_bar.setValue(100)
            self.btn_open.setEnabled(True)
            QMessageBox.information(self, t("msg_done"), msg)
        else:
            QMessageBox.warning(self, t("msg_hint"), t("msg_incomplete") + msg)
        self.worker = None
