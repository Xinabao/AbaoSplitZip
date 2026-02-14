# AbaoZip - 分卷独立解压打包工具

<p align="center">
  <strong>将大文件夹按指定大小分卷打包，每卷可独立解压</strong>
</p>

## ✨ 特性

- 📦 **分卷独立解压** — 每个分卷都是完整的 ZIP 文件，无需合并即可独立解压
- 🔐 **双加密模式** — ZipCrypto（兼容 Windows 10/11 资源管理器直接解压）或 AES-256（更安全，需 7-Zip/WinRAR 等第三方工具解压）
- ⚙️ **可调压缩级别** — 从仅存储到最大压缩，按需选择
- 📊 **智能分组** — 自动将文件按大小分配到各分卷，接近指定大小
- ⚡ **多线程并行** — 多个分卷同时压缩，充分利用多核 CPU
- 💾 **智能缓冲写盘** — 64MB 分块缓冲 + 写盘锁，减少磁盘碎片和 I/O 争抢
- 📂 **内置解压** — 选择任意一个分卷即可自动识别并解压同组所有分卷
- 📝 **一键解压脚本** — 打包完成后自动生成 bat 脚本，双击即可解压全部分卷
- 🖥️ **图形界面** — 简洁易用的 GUI，支持进度显示和日志输出
- 💻 **Windows 原生** — 单文件 .exe，无需安装，双击即用

## 📋 使用场景

- 需要将大型项目/资源按大小分割，但又希望每部分可以独立使用
- 通过有文件大小限制的平台传输大量文件
- 备份大文件夹到有容量限制的存储介质

## 🚀 快速开始

### 直接使用

从 [Releases](https://github.com/Xinabao/AbaoZip/releases) 下载最新版本的 ZIP 包，解压后双击 `AbaoZip.exe` 即可运行。

> ⚠️ 如果 Windows SmartScreen 拦截，请参考压缩包内的「使用说明.txt」解除拦截。

### 从源码运行

```bash
git clone https://github.com/Xinabao/AbaoZip.git
cd AbaoZip
pip install -r requirements.txt
python main.py
```

## 🔧 构建 .exe

```bash
pip install -r requirements.txt
python -m PyInstaller build.spec --clean --noconfirm
```

构建产物：`dist/AbaoZip.exe`（单文件，约 40 MB）

## 📖 使用说明

### 打包

1. **选择源文件夹** — 点击"浏览"选择要打包的文件夹
2. **选择输出目录** — 选择分卷压缩包的保存位置
3. **设置分卷大小** — 输入每卷的目标大小（MB）
4. **设置密码**（可选） — 输入密码并选择加密方式
5. **选择压缩级别** — 从存储到最大压缩
6. **开始打包** — 点击"开始打包"，等待完成

### 解压

1. **选择分卷文件** — 点击"浏览"选择任意一个分卷 ZIP（如 `XXX_part001.zip`）
2. **选择解压目录** — 选择解压目标位置
3. **输入密码**（如有） — 填写打包时设置的密码
4. **开始解压** — 自动识别并解压同组所有分卷

也可以直接双击输出目录中的 `XXX_一键全部解压.bat` 一次性解压所有分卷。

### 命名格式

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
MyFolder_一键全部解压.bat
```

## ⚠️ 注意事项

- 分卷大小为近似值，因为要保证每个文件的完整性（不会切割单个文件）
- 如果单个文件大于指定分卷大小，该文件会单独放入一卷中
- AES-256 加密的 ZIP 需要 7-Zip、WinRAR 等工具解压，Windows 资源管理器无法直接打开
- ZipCrypto 加密可被 Windows 10/11 资源管理器直接解压，但安全性较弱，不适合高敏感数据

## 🛠️ 技术栈

- **Python 3.8+**
- **PyQt5** — GUI 框架
- **pyzipper** — ZIP 加密支持（ZipCrypto / AES-256）
- **PyInstaller** — 打包为 Windows 可执行文件

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。
