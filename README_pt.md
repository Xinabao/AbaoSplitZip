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

Divida pastas grandes em volumes comprimidos pelo tamanho especificado. **Cada volume é um arquivo ZIP independente** que pode ser extraído separadamente sem mesclagem.

**Palavras-chave de busca**: compressão dividida, extração independente, divisão de arquivo grande, extração separada, divisão de volume ZIP, ferramenta de fragmentação de arquivo, arquivos divididos, sem necessidade de mesclagem

### Recursos

- 📦 **Extração de Volume Independente** — Cada volume é um ZIP completo que pode ser extraído independentemente sem mesclagem
- 📂 **Modo Diretório Prioritário** — Preserva inteligentemente a estrutura de subpastas
- 🔗 **Mesclar e Extrair em Um Clique** — Selecione qualquer volume para identificar e extrair automaticamente todos os volumes associados
- 🔐 **Modos de Criptografia Dupla** — ZipCrypto (compatível com Explorador do Windows) ou AES-256 (mais seguro)
- ⚡ **Compressão Multi-thread** — Acelere o empacotamento usando CPUs multi-núcleo
- 🖱️ **Suporte de Arrastar e Soltar** — Suporta entrada de arquivo/pasta por arrastar e soltar
- 📂 **Extração Multi-formato** — Suporta extração de ZIP, 7z, RAR
- 🌍 **9 Idiomas** — Detecção automática do idioma do sistema

### Uso

Baixe em [Releases](https://github.com/Xinabao/AbaoSplitZip/releases) ou no [site oficial](https://www.abaodisk.com/Abaozip), ou execute a partir do código-fonte:

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen pode bloquear arquivos exe não assinados. Consulte "使用说明.txt" no pacote para desabilitar esta proteção.

### Operação de Empacotamento

1. Selecione a pasta de origem → Selecione o diretório de saída → Defina o tamanho do volume (MB)
2. Escolha o modo (tamanho balanceado / diretório prioritário)
3. Opcional: Defina a senha + Escolha o método de criptografia
4. Iniciar empacotamento

### Mesclar e Extrair

1. Alterne para a aba "Mesclar e Extrair"
2. Arraste qualquer arquivo de volume (.zip)
3. Clique em "Iniciar Mesclar e Extrair", o software localizará automaticamente outros volumes no mesmo diretório e os extrairá

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
