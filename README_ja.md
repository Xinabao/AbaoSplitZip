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

大きなフォルダを指定サイズでボリュームに分割してパッケージ化します。**各ボリュームは独立した ZIP ファイル**で、マージなしで個別に抽出できます。

**検索キーワード**：分割圧縮、独立抽出、大ファイル分割、個別解凍、ZIP ボリューム分割、ファイルチャンク化ツール、分割アーカイブ、マージ不要

### 機能

- 📦 **独立ボリューム抽出** — 各ボリュームは完全な ZIP で、マージなしで独立して抽出可能
- 📂 **ディレクトリ優先モード** — サブフォルダ構造を自動保持
- 🔗 **ワンクリック統合解凍** — 任意のボリュームを選択して、関連するすべてのボリュームを自動検出して抽出
- 🔐 **デュアル暗号化モード** — ZipCrypto（Windows エクスプローラ互換）または AES-256（より安全）
- ⚡ **マルチスレッド圧縮** — マルチコア CPU を活用して圧縮を高速化
- 🖱️ **ドラッグ & ドロップ対応** — ファイル/フォルダのドラッグ & ドロップ入力に対応
- 📂 **複数形式の抽出** — ZIP、7z、RAR の抽出に対応
- 🌍 **9 言語** — システム言語の自動検出

### 使用方法

[Releases](https://github.com/Xinabao/AbaoSplitZip/releases) または[公式ウェブサイト](https://www.abaodisk.com/Abaozip)からダウンロードするか、ソースから実行します：

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen が署名されていない exe をブロックする場合があります。パッケージ内の「使用説明.txt」を参照して、保護を無効にしてください。

### パッキング操作

1. ソースフォルダを選択 → 出力ディレクトリを選択 → ボリュームサイズを設定（MB）
2. モードを選択（バランス型 / ディレクトリ優先）
3. オプション：パスワードを設定 + 暗号化方式を選択
4. パッキング開始

### 統合解凍

1. 「統合解凍」タブに切り替え
2. 任意のボリュームファイル（.zip）をドラッグ
3. 「統合解凍開始」をクリックすると、ソフトウェアが同じディレクトリ内の他のボリュームを自動検出して抽出

### ネーミング形式

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
