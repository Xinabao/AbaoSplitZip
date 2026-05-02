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

> 最終 GPL 開源版。v1.4.0 發布後，本倉庫計劃歸檔；後續商業開發將另行進行。

將大資料夾按指定大小分卷打包，**每個分卷都是獨立的 ZIP 檔案**，可單獨解壓，無需合併。

**搜尋關鍵詞**：分卷壓縮 獨立解壓、大檔案 分割 單獨解壓、ZIP 分卷 每卷獨立、檔案分割打包工具、分卷壓縮包 不用合併 直接解壓

### 功能特性

- 📦 **分卷獨立解壓** — 每個分卷都是完整的 ZIP，無需合併即可獨立解壓
- 📂 **目錄優先模式** — 智能保持子資料夾結構完整
- 🔗 **一鍵合併解壓** — 選擇任意分卷即可自動識別並解壓全部關聯分卷
- 🔐 **雙加密模式** — ZipCrypto（相容 Windows 檔案總管）或 AES-256（更安全）
- ⚡ **多執行緒並行壓縮** — 利用多核 CPU 加速打包
- 🖱️ **拖曳支援** — 支援檔案/資料夾拖曳輸入
- 📂 **多格式解壓** — 支援解壓 ZIP、7z、RAR
- 🌍 **9 種語言** — 自動偵測系統語言

### 使用方法

從 [Releases](https://github.com/Xinabao/AbaoSplitZip/releases) 或 [官方網站](https://www.abaodisk.com/Abaozip) 下載，或從源碼執行：

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen 可能攔截未簽署的 exe，請參考壓縮包內「使用說明.txt」解除攔截。

### 打包操作

1. 選擇源資料夾 → 選擇輸出目錄 → 設定分卷大小（MB）
2. 選擇模式（體積均衡 / 目錄優先）
3. 可選：設定密碼 + 選擇加密方式
4. 開始打包

### 合併解壓

1. 切換到「合併解壓」標籤頁
2. 拖入任意一個分卷檔案 (.zip)
3. 點擊「開始合併解壓」，軟體會自動尋找同目錄下的其他分卷並解壓

### 命名格式

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_一鍵全部解壓.bat
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
