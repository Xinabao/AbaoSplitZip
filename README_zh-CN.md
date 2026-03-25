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

# AbaoZip (原 AbaoSplitZip)

将大文件夹按指定大小分卷打包，**每个分卷都是独立的 ZIP 文件**，可单独解压，无需合并。

**搜索关键词**：分卷压缩 独立解压、大文件 分割 单独解压、ZIP 分卷 每卷独立、文件分割打包工具、分卷压缩包 不用合并 直接解压

### 功能特性

- 📦 **分卷独立解压** — 每个分卷都是完整的 ZIP，无需合并即可独立解压
- 📂 **目录优先模式** — 智能保持子文件夹结构完整
- 🔗 **一键合并解压** — 选择任意分卷即可自动识别并解压全部关联分卷
- 🔐 **双加密模式** — ZipCrypto（兼容 Windows 资源管理器）或 AES-256（更安全）
- ⚡ **多线程并行压缩** — 利用多核 CPU 加速打包
- 🖱️ **拖拽支持** — 支持文件/文件夹拖拽输入
- 📂 **多格式解压** — 支持解压 ZIP、7z、RAR
- 🌍 **9 种语言** — 自动检测系统语言

### 使用方法

从 [Releases](https://github.com/Xinabao/AbaoZip/releases) 或 [官方网站](https://www.aboutdisk.com/AbaoSoftware/abaosplitzip) 下载，或从源码运行：

```bash
git clone https://github.com/Xinabao/AbaoZip.git
cd AbaoZip
pip install -r requirements.txt
python main.py
```

> ⚠️ Windows SmartScreen 可能拦截未签名的 exe，请参考压缩包内「使用说明.txt」解除拦截。

### 打包操作

1. 选择源文件夹 → 选择输出目录 → 设置分卷大小（MB）
2. 选择模式（体积均衡 / 目录优先）
3. 可选：设置密码 + 选择加密方式
4. 开始打包

### 合并解压

1. 切换到“合并解压”标签页
2. 拖入任意一个分卷文件 (.zip)
3. 点击“开始合并解压”，软件会自动寻找同目录下的其他分卷并解压

### 命名格式

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_一键全部解压.bat
```


---

## 🔧 Build / 构建

### Windows
双击 `build.bat`，或执行：
```cmd
build.bat
```

### macOS / Linux
执行 shell 脚本：
```bash
chmod +x build.sh
./build.sh
```

### Manual Build
```bash
pip install -r requirements.txt
python -m PyInstaller build.spec --clean --noconfirm
```

输出：`dist/AbaoZip`（Windows 下为 `AbaoZip.exe`）

### 测试

```bash
python -m unittest discover -s tests -v
```

### 项目文档

- `CHANGELOG.md` — 更新记录与维护说明
- `CONTRIBUTING.md` — 本地开发、测试、发布流程

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
