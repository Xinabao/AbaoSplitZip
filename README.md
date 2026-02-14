# AbaoSplitZip

<p align="center">
  <strong>Split large folders into volume-sized ZIPs — each volume extracts independently</strong><br>
  大文件夹分卷打包，每卷可独立解压 | 大きなフォルダを分割、各巻独立解凍 | 대용량 폴더 분할 압축, 각 볼륨 독립 해제
</p>

<p align="center">
  <a href="#-english">English</a> •
  <a href="#-简体中文">简体中文</a> •
  <a href="#-繁體中文">繁體中文</a> •
  <a href="#-日本語">日本語</a> •
  <a href="#-한국어">한국어</a> •
  <a href="#-deutsch">Deutsch</a> •
  <a href="#-français">Français</a> •
  <a href="#-español">Español</a> •
  <a href="#-português">Português</a>
</p>

---

<!-- GitHub Topics (recommended):
  split-zip, volume-packer, independent-extract, zip-splitter,
  file-splitter, archive-tool, multi-volume-zip, pyqt5,
  zip-encryption, aes256, compression-tool
-->

## 🌍 English

**AbaoSplitZip** — Pack large folders into multiple volume-sized ZIP files where **each volume can be extracted independently** without needing other parts.

**Keywords**: split zip independently extractable, split archive each part standalone, volume zip extract separately, large folder splitter, zip split tool with independent extraction

### Features

- 📦 **Independent Volume Extraction** — Each volume is a complete ZIP, no merging required
- 🔐 **Dual Encryption** — ZipCrypto (Windows Explorer compatible) or AES-256 (requires 7-Zip/WinRAR)
- ⚡ **Multi-threaded Packing** — Parallel compression with 64MB buffered I/O
- 📂 **Multi-format Extraction** — Extract ZIP, 7z, and RAR archives
- 🌍 **9 Languages** — Auto-detects system language
- 💻 **Cross-platform** — Windows / macOS / Linux

### Quick Start

Download from [Releases](https://github.com/Xinabao/AbaoSplitZip/releases), or run from source:

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

---

## 🇨🇳 简体中文

**AbaoSplitZip** — 将大文件夹按指定大小分卷打包，**每个分卷都是独立的 ZIP 文件**，可单独解压，无需合并。

**搜索关键词**：分卷压缩 独立解压、大文件 分割 单独解压、ZIP 分卷 每卷独立、文件分割打包工具、分卷压缩包 不用合并 直接解压

### 功能特性

- 📦 **分卷独立解压** — 每个分卷都是完整的 ZIP，无需合并即可独立解压
- 🔐 **双加密模式** — ZipCrypto（兼容 Windows 10/11 资源管理器直接解压）或 AES-256（更安全）
- ⚡ **多线程并行压缩** — 64MB 缓冲写盘，减少磁盘碎片
- 📂 **多格式解压** — 支持解压 ZIP、7z、RAR
- 🌍 **9 种语言** — 自动检测系统语言
- 💻 **跨平台** — Windows / macOS / Linux

### 使用方法

从 [Releases](https://github.com/Xinabao/AbaoSplitZip/releases) 下载，或从源码运行：

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen 可能拦截未签名的 exe，请参考压缩包内「使用说明.txt」解除拦截。

### 打包操作

1. 选择源文件夹 → 选择输出目录 → 设置分卷大小（MB）
2. 可选：设置密码 + 选择加密方式（ZipCrypto / AES-256）
3. 选择压缩级别 → 开始打包
4. 完成后自动生成「一键全部解压.bat」脚本

### 命名格式

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_一键全部解压.bat
```

---

## 🇹🇼 繁體中文

**AbaoSplitZip** — 將大資料夾按指定大小分卷打包，**每個分卷都是獨立的 ZIP 檔案**，可單獨解壓，無需合併。

**搜尋關鍵字**：分卷壓縮 獨立解壓、大檔案 分割 單獨解壓、ZIP 分卷 每卷獨立、檔案分割打包工具

### 功能特性

- 📦 **分卷獨立解壓** — 每個分卷都是完整的 ZIP，無需合併即可獨立解壓
- 🔐 **雙加密模式** — ZipCrypto（相容 Windows 檔案總管）或 AES-256（更安全）
- ⚡ **多執行緒並行壓縮** — 64MB 緩衝寫入，減少磁碟碎片
- 📂 **多格式解壓** — 支援 ZIP、7z、RAR
- 🌍 **9 種語言** — 自動偵測系統語言

---

## 🇯🇵 日本語

**AbaoSplitZip** — 大きなフォルダを指定サイズで分割パック。**各ボリュームは独立したZIPファイル**で、他のパーツなしで個別に解凍可能。

**検索キーワード**：分割圧縮 個別解凍、大容量フォルダ 分割 独立解凍、ZIP分割 各巻独立、ファイル分割ツール

### 機能

- 📦 **分割独立解凍** — 各ボリュームは完全なZIP、結合不要で個別解凍可能
- 🔐 **二重暗号化** — ZipCrypto（Windowsエクスプローラー対応）/ AES-256
- ⚡ **マルチスレッド圧縮** — 64MBバッファI/O
- 📂 **複数形式対応** — ZIP / 7z / RAR の解凍をサポート
- 🌍 **9言語対応** — システム言語自動検出

---

## 🇰🇷 한국어

**AbaoSplitZip** — 대용량 폴더를 지정 크기로 분할 압축. **각 볼륨은 독립적인 ZIP 파일**로, 다른 파트 없이 개별 압축 해제 가능.

**검색 키워드**: 분할 압축 독립 해제, 대용량 파일 분할 개별 압축해제, ZIP 분할 각 파트 독립, 파일 분할 도구

### 기능

- 📦 **분할 독립 해제** — 각 볼륨은 완전한 ZIP, 합치지 않고 개별 해제 가능
- 🔐 **이중 암호화** — ZipCrypto (Windows 탐색기 호환) / AES-256
- ⚡ **멀티스레드 압축** — 64MB 버퍼 I/O
- 📂 **다형식 지원** — ZIP / 7z / RAR 압축 해제 지원
- 🌍 **9개 언어** — 시스템 언어 자동 감지

---

## 🇩🇪 Deutsch

**AbaoSplitZip** — Große Ordner in Volumen-ZIPs aufteilen. **Jedes Volumen ist ein eigenständiges ZIP** und kann unabhängig entpackt werden.

**Suchbegriffe**: ZIP aufteilen unabhängig extrahieren, Ordner aufteilen einzeln entpacken, Volumen-ZIP unabhängige Extraktion

### Funktionen

- 📦 **Unabhängige Volumen-Extraktion** — Jedes Volumen ist ein vollständiges ZIP
- 🔐 **Doppelte Verschlüsselung** — ZipCrypto / AES-256
- ⚡ **Multi-Thread-Komprimierung** — 64MB gepufferte I/O
- 📂 **Multi-Format-Entpackung** — ZIP / 7z / RAR
- 🌍 **9 Sprachen** — Automatische Spracherkennung

---

## 🇫🇷 Français

**AbaoSplitZip** — Diviser de grands dossiers en ZIP par volumes. **Chaque volume est un ZIP indépendant** extractible séparément.

**Mots-clés**: diviser ZIP extraction indépendante, séparer dossier extraire individuellement, archive multi-volumes indépendante

### Fonctionnalités

- 📦 **Extraction indépendante par volume** — Chaque volume est un ZIP complet
- 🔐 **Double chiffrement** — ZipCrypto / AES-256
- ⚡ **Compression multi-thread** — I/O tamponnée 64Mo
- 📂 **Extraction multi-format** — ZIP / 7z / RAR
- 🌍 **9 langues** — Détection automatique de la langue

---

## 🇪🇸 Español

**AbaoSplitZip** — Dividir carpetas grandes en ZIPs por volúmenes. **Cada volumen es un ZIP independiente** que se puede extraer por separado.

**Palabras clave**: dividir ZIP extracción independiente, separar carpeta extraer individualmente, archivo multi-volumen independiente

### Características

- 📦 **Extracción independiente por volumen** — Cada volumen es un ZIP completo
- 🔐 **Doble cifrado** — ZipCrypto / AES-256
- ⚡ **Compresión multi-hilo** — I/O con búfer de 64MB
- 📂 **Extracción multi-formato** — ZIP / 7z / RAR
- 🌍 **9 idiomas** — Detección automática del idioma

---

## 🇧🇷 Português

**AbaoSplitZip** — Dividir pastas grandes em ZIPs por volumes. **Cada volume é um ZIP independente** que pode ser extraído separadamente.

**Palavras-chave**: dividir ZIP extração independente, separar pasta extrair individualmente, arquivo multi-volume independente

### Recursos

- 📦 **Extração independente por volume** — Cada volume é um ZIP completo
- 🔐 **Dupla criptografia** — ZipCrypto / AES-256
- ⚡ **Compressão multi-thread** — I/O com buffer de 64MB
- 📂 **Extração multi-formato** — ZIP / 7z / RAR
- 🌍 **9 idiomas** — Detecção automática do idioma

---

## 🔧 Build / 构建

```bash
# Build exe (Windows)
build.bat

# Or manually on any platform
pip install -r requirements.txt
python -m PyInstaller build.spec --clean --noconfirm
```

Output: `dist/AbaoSplitZip` (~40 MB)

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

## 🏷️ Recommended GitHub Topics

```
split-zip, volume-packer, independent-extract, zip-splitter,
file-splitter, archive-tool, multi-volume-zip, pyqt5,
zip-encryption, aes256, compression-tool, cross-platform
```
