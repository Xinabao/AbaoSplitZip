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

# AbaoZip (anteriormente AbaoSplitZip)

Divida carpetas grandes en volúmenes comprimidos según el tamaño especificado. **Cada volumen es un archivo ZIP independiente** que puede extraerse por separado sin fusionarse.

**Palabras clave de búsqueda**: compresión dividida, extracción independiente, división de archivos grandes, extracción separada, división de volúmenes ZIP, herramienta de fragmentación de archivos, archivos divididos, sin necesidad de fusión

### Características

- 📦 **Extracción de Volumen Independiente** — Cada volumen es un ZIP completo que puede extraerse independientemente sin fusión
- 📂 **Modo Directorios Prioritarios** — Preserva inteligentemente la estructura de subcarpetas
- 🔗 **Fusión y Extracción en Un Clic** — Seleccione cualquier volumen para identificar y extraer automáticamente todos los volúmenes asociados
- 🔐 **Modos de Cifrado Dual** — ZipCrypto (compatible con Explorador de Windows) o AES-256 (más seguro)
- ⚡ **Compresión Multihilo** — Acelere el empaque utilizando CPU multicódigo
- 🖱️ **Soporte de Arrastrar y Soltar** — Soporta entrada de archivos/carpetas por arrastrar y soltar
- 📂 **Extracción Multi-formato** — Soporta extracción de ZIP, 7z, RAR
- 🌍 **9 Idiomas** — Detección automática del idioma del sistema

### Uso

Descargue desde [Releases](https://github.com/Xinabao/AbaoZip/releases) o el [sitio oficial](https://www.aboutdisk.com/AbaoSoftware/abaosplitzip), o ejecute desde el código fuente:

```bash
git clone https://github.com/Xinabao/AbaoZip.git
cd AbaoZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen puede bloquear archivos exe sin firmar. Consulte « 使用说明.txt » en el paquete para desactivar esta protección.

### Operación de Empaque

1. Seleccione la carpeta de origen → Seleccione el directorio de salida → Establezca el tamaño del volumen (MB)
2. Elija el modo (tamaño equilibrado / directorios prioritarios)
3. Opcional: Establezca la contraseña + Elija el método de cifrado
4. Iniciar empaque

### Fusión y Extracción

1. Cambie a la pestaña "Fusión y Extracción"
2. Arrastre cualquier archivo de volumen (.zip)
3. Haga clic en "Iniciar Fusión y Extracción", el software encontrará automáticamente otros volúmenes en el mismo directorio y los extraerá

### Formato de Nomenclatura

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
