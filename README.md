<p align="center">
  [English](README.md) •
  [简体中文](README_zh-CN.md) •
  [繁體中文](README_zh-TW.md) •
  [日本語](README_ja.md) •
  [한국어](README_ko.md) •
  [Deutsch](README_de.md) •
  [Français](README_fr.md) •
  [Español](README_es.md) •
  [Português](README_pt.md)
</p>

---

# AbaoSplitZip

> Final GPL open-source release. This repository is intended to be archived after v1.4.0; future commercial development will happen separately.

## Commercial Successor

This repository preserves the final GPL open-source release of AbaoSplitZip v1.4.0. Source code, release downloads, and GPL v3 rights remain available.

Future commercial development continues separately under the AbaoZip product line, with a different license and feature roadmap:

https://www.abaodisk.com/Abaozip

Split large folders into independently extractable ZIP volumes by specified size. **Each volume is a standalone ZIP file** that can be extracted separately without merging.

**Search Keywords**: split zip archive, independent volume extraction, large file splitting, separate extraction, ZIP volume splitting, file chunking tool, split archive without merging, direct extraction

### Features

- 📦 **Independent Volume Extraction** — Each volume is a complete ZIP that can be extracted independently without merging
- 📂 **Directory-First Mode** — Intelligently preserves complete subfolder structures
- 🔗 **One-Click Merge & Extract** — Select any volume and automatically identify and extract all associated volumes
- 🔐 **Dual Encryption Modes** — ZipCrypto (compatible with Windows Explorer) or AES-256 (more secure)
- ⚡ **Multi-threaded Compression** — Accelerate packing using multi-core CPU
- 🖱️ **Drag & Drop Support** — Supports file/folder drag and drop input
- 📂 **Multi-format Extraction** — Supports extracting ZIP, 7z, RAR
- 🌍 **9 Languages** — Automatic system language detection

### Usage

Download the final GPL release from [Releases](https://github.com/Xinabao/AbaoSplitZip/releases), visit the [commercial successor page](https://www.abaodisk.com/Abaozip), or run from source:

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen may block unsigned executables. Please refer to "使用说明.txt" in the package to disable this protection.

### Packing Operation

1. Select source folder → Select output directory → Set volume size (MB)
2. Choose mode (Balanced Size / Directory-First)
3. Optional: Set password + Choose encryption method
4. Start packing

### Merge & Extract

1. Switch to the "Merge & Extract" tab
2. Drag in any volume file (.zip)
3. Click "Start Merge & Extract", the software will automatically find other volumes in the same directory and extract them

### Naming Format

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_一键全部解压.bat
```

---

## 🔧 Build / 构建

### Windows
Double-click `build.bat` or run:
```cmd
build.bat
```

### macOS / Linux
Run the shell script:
```bash
chmod +x build.sh
./build.sh
```

### Manual Build
```bash
pip install -r requirements.txt
python -m PyInstaller build.spec --clean --noconfirm
```

Output: `dist/AbaoSplitZip` (or `AbaoSplitZip.exe`)

### Tests

```bash
python -m unittest discover -s tests -v
```

### Project Docs

- `CHANGELOG.md` — maintenance and release notes
- `CONTRIBUTING.md` — setup, test, and release workflow for contributors
- `ARCHIVE_NOTICE.md` — final open-source archive notice
- `RELEASE_NOTES_1.4.0.md` — GitHub release notes for the final GPL version
- `RELEASE_CHECKLIST_1.4.0.md` — final release and archive checklist
- `THIRD_PARTY_NOTICES.md` — third-party dependency license notes

## ⚠️ Notes / 注意事项

- Volume sizes are approximate — single files are never split across volumes
- AES-256 encrypted ZIPs require 7-Zip/WinRAR to extract (Windows Explorer does not support AES)
- RAR extraction requires UnRAR runtime (auto-detected on system)
- macOS/Linux builds via [GitHub Actions](.github/workflows/build.yml)

## 🛠️ Tech Stack

- **Python 3.8+** / **PyQt5** (GUI) / **pyzipper** (ZIP + encryption)
- **py7zr** (7z extraction) / **rarfile** (RAR extraction)
- **PyInstaller** (standalone executable)

## 📄 License

[GPL v3](LICENSE)
