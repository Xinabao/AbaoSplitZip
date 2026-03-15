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

# AbaoZip (ehemals AbaoSplitZip)

Teilen Sie große Ordner nach einer bestimmten Größe in mehrere Volumen auf. **Jedes Volumen ist eine eigenständige ZIP-Datei** und kann separat ohne Zusammenführung extrahiert werden.

**Suchbegriffe**: Zip-Aufteilung, unabhängige Extraktion, große Dateien teilen, separate Entpackung, ZIP-Volumenaufteilung, Datei-Chunking-Tool, geteilte Archive, Zusammenführung nicht erforderlich

### Funktionen

- 📦 **Unabhängige Volumenextraktion** — Jedes Volumen ist eine vollständige ZIP, die unabhängig ohne Zusammenführung extrahiert werden kann
- 📂 **Verzeichnis-Prioritätsmodus** — Intelligente Beibehaltung der Unterordnerstruktur
- 🔗 **Ein-Klick-Zusammenführung und Extraktion** — Wählen Sie ein beliebiges Volumen und erkennen Sie automatisch alle zugehörigen Volumen und extrahieren Sie diese
- 🔐 **Duale Verschlüsselungsmodi** — ZipCrypto (kompatibel mit Windows Explorer) oder AES-256 (sicherer)
- ⚡ **Multithreading-Komprimierung** — Nutzen Sie Multi-Core-CPUs zur Beschleunigung des Packens
- 🖱️ **Drag-and-Drop-Unterstützung** — Unterstützt Datei- und Ordner-Drag-and-Drop-Eingabe
- 📂 **Mehrformat-Extraktion** — Unterstützt das Extrahieren von ZIP, 7z, RAR
- 🌍 **9 Sprachen** — Automatische Erkennung der Systemsprache

### Verwendung

Download von [Releases](https://github.com/Xinabao/AbaoZip/releases) oder der [offiziellen Website](https://www.aboutdisk.com/AbaoSoftware/abaosplitzip) oder Ausführung aus dem Quellcode:

```bash
git clone https://github.com/Xinabao/AbaoZip.git
cd AbaoZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen kann unsignierte exe-Dateien blockieren. Lesen Sie bitte "使用说明.txt" im Paket, um den Schutz zu deaktivieren.

### Packbetrieb

1. Quellordner auswählen → Ausgabeverzeichnis auswählen → Volumengröße festlegen (MB)
2. Modus auswählen (ausgeglichene Größe / Verzeichnis-Priorität)
3. Optional: Kennwort festlegen + Verschlüsselungsmethode auswählen
4. Packen starten

### Zusammenführung und Extraktion

1. Zur Registerkarte "Zusammenführung und Extraktion" wechseln
2. Eine beliebige Volumendatei (.zip) ziehen
3. Klicken Sie auf "Zusammenführung und Extraktion starten". Die Software findet automatisch andere Volumen im selben Verzeichnis und extrahiert diese

### Namensformat

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

Output: `dist/AbaoZip` (or `AbaoZip.exe`)

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
