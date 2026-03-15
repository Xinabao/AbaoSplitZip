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

# AbaoZip (구 AbaoSplitZip)

큰 폴더를 지정된 크기로 분할 압축합니다. **각 분할 볼륨은 독립적인 ZIP 파일**이며 병합 없이 개별 추출 가능합니다.

**검색 키워드**: 분할 압축, 독립 해제, 대용량 파일 분할, 개별 해제, ZIP 분할 볼륨, 파일 청킹 도구, 분할 보관함, 병합 불필요

### 기능

- 📦 **독립적 볼륨 추출** — 각 볼륨은 완전한 ZIP이며 병합 없이 독립적으로 추출 가능
- 📂 **디렉터리 우선 모드** — 하위 폴더 구조 자동 유지
- 🔗 **원클릭 병합 해제** — 임의의 볼륨을 선택하면 관련된 모든 볼륨 자동 감지 및 해제
- 🔐 **이중 암호화 모드** — ZipCrypto(Windows 탐색기 호환) 또는 AES-256(더 안전)
- ⚡ **멀티스레드 압축** — 멀티코어 CPU를 활용한 압축 가속
- 🖱️ **드래그 & 드롭 지원** — 파일/폴더 드래그 & 드롭 입력 지원
- 📂 **다중 형식 해제** — ZIP, 7z, RAR 해제 지원
- 🌍 **9 언어** — 시스템 언어 자동 감지

### 사용 방법

[Releases](https://github.com/Xinabao/AbaoZip/releases) 또는 [공식 웹사이트](https://www.aboutdisk.com/AbaoSoftware/abaosplitzip)에서 다운로드하거나 소스에서 실행합니다:

```bash
git clone https://github.com/Xinabao/AbaoZip.git
cd AbaoZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen이 서명되지 않은 exe를 차단할 수 있습니다. 패키지 내 "사용설명.txt"를 참조하여 보호를 해제하세요.

### 압축 작업

1. 원본 폴더 선택 → 출력 디렉터리 선택 → 분할 볼륨 크기 설정(MB)
2. 모드 선택(균형잡힌 크기 / 디렉터리 우선)
3. 선택사항: 비밀번호 설정 + 암호화 방식 선택
4. 압축 시작

### 병합 해제

1. "병합 해제" 탭으로 전환
2. 임의의 분할 파일(.zip) 드래그
3. "병합 해제 시작" 클릭하면 소프트웨어가 같은 디렉터리의 다른 볼륨을 자동 검색하여 해제

### 명명 형식

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_일괄해제.bat
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
