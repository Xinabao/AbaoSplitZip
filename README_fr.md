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

Divisez les grands dossiers en volumes compressés par taille spécifiée. **Chaque volume est un fichier ZIP indépendant** qui peut être extrait séparément sans fusion.

**Mots-clés de recherche**: compression divisée, extraction indépendante, fractionnement de fichiers volumineux, extraction séparée, division de volumes ZIP, outil de segmentation de fichiers, archives divisées, fusion non requise

### Caractéristiques

- 📦 **Extraction de Volume Indépendante** — Chaque volume est un ZIP complet qui peut être extrait indépendamment sans fusion
- 📂 **Mode Répertoire Prioritaire** — Préserve intelligemment la structure des sous-dossiers
- 🔗 **Fusion et Extraction en Un Clic** — Sélectionnez n'importe quel volume pour identifier et extraire automatiquement tous les volumes associés
- 🔐 **Modes de Chiffrement Dual** — ZipCrypto (compatible avec l'Explorateur Windows) ou AES-256 (plus sécurisé)
- ⚡ **Compression Multithread** — Accélérez l'empaquetage en utilisant les CPU multi-cœurs
- 🖱️ **Support du Glisser-Déposer** — Prend en charge l'entrée par glisser-déposer de fichiers/dossiers
- 📂 **Extraction Multi-formats** — Prend en charge l'extraction de ZIP, 7z, RAR
- 🌍 **9 Langues** — Détection automatique de la langue du système

### Utilisation

Téléchargez depuis [Releases](https://github.com/Xinabao/AbaoSplitZip/releases) ou le [site officiel](https://www.abaodisk.com/Abaozip), ou exécutez depuis le code source :

```bash
git clone https://github.com/Xinabao/AbaoSplitZip.git
cd AbaoSplitZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen peut bloquer les fichiers exe non signés. Veuillez consulter « 使用说明.txt » dans le package pour désactiver cette protection.

### Opération d'Empaquetage

1. Sélectionnez le dossier source → Sélectionnez le répertoire de sortie → Définissez la taille du volume (MB)
2. Choisissez le mode (taille équilibrée / répertoire prioritaire)
3. Optionnel : Définir le mot de passe + Choisir la méthode de chiffrement
4. Démarrer l'empaquetage

### Fusion et Extraction

1. Accédez à l'onglet "Fusion et Extraction"
2. Déposez n'importe quel fichier de volume (.zip)
3. Cliquez sur "Démarrer la Fusion et l'Extraction", le logiciel trouvera automatiquement les autres volumes du même répertoire et les extraira

### Format de Dénomination

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
