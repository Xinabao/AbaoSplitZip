import os
import sys

from core.version import APP_NAME

python_dir = os.path.dirname(sys.executable)
python_dll = os.path.join(python_dir, f'python{sys.version_info.major}{sys.version_info.minor}.dll')

extra_binaries = []
if os.path.exists(python_dll):
    extra_binaries.append((python_dll, '.'))

# Icon only on Windows
icon_file = 'resources/icon.ico' if sys.platform == 'win32' and os.path.exists('resources/icon.ico') else None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=extra_binaries,
    datas=[],
    hiddenimports=['py7zr', 'rarfile'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Version info only on Windows
version_file = 'version_info.txt' if sys.platform == 'win32' else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_file,
    version=version_file,
)
