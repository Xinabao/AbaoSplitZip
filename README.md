# AbaoZip - 分卷独立解压打包工具

<p align="center">
  <strong>将大文件夹按指定大小分卷打包，每卷可独立解压</strong>
</p>

## ✨ 特性

- 📦 **分卷独立解压** — 每个分卷都是完整的 ZIP 文件，无需合并即可独立解压
- 🔐 **双加密模式** — ZipCrypto（兼容 Windows 10/11 资源管理器直接解压）或 AES-256（更安全，需 7-Zip/WinRAR 等第三方工具解压）
- ⚙️ **可调压缩级别** — 从仅存储到最大压缩，按需选择
- 📊 **智能分组** — 自动将文件按大小分配到各分卷，接近指定大小
- 🖥️ **图形界面** — 简洁易用的 GUI，支持进度显示和日志输出
- 💻 **Windows 原生** — 可打包为独立 .exe 文件运行

## 📋 使用场景

- 需要将大型项目/资源按大小分割，但又希望每部分可以独立使用
- 通过有文件大小限制的平台传输大量文件
- 备份大文件夹到有容量限制的存储介质

## 🚀 快速开始

### 从源码运行

```bash
# 克隆项目
git clone https://github.com/your-username/AbaoZip.git
cd AbaoZip

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

### 使用 .exe

从 [Releases](https://github.com/your-username/AbaoZip/releases) 下载最新版本，双击运行即可。

## 🔧 构建 .exe

```bash
pip install pyinstaller
python -m PyInstaller build.spec
```

构建产物在 `dist/AbaoZip/` 目录下。

## 📖 使用说明

1. **选择源文件夹** — 点击"浏览"选择要打包的文件夹
2. **选择输出目录** — 选择分卷压缩包的保存位置
3. **设置分卷大小** — 输入每卷的目标大小（MB）
4. **设置密码**（可选） — 输入密码启用 AES-256 加密
5. **选择压缩级别** — 从存储到最大压缩
6. **开始打包** — 点击"开始打包"，等待完成

### 命名格式

```
MyFolder_part001.zip
MyFolder_part002.zip
MyFolder_part003.zip
...
```

## ⚠️ 注意事项

- 分卷大小为近似值，因为要保证每个文件的完整性（不会切割单个文件）
- 如果单个文件大于指定分卷大小，该文件会单独放入一卷中
- AES-256 加密的 ZIP 需要支持该标准的解压工具（如 7-Zip、WinRAR 等），Windows 资源管理器无法直接打开
- ZipCrypto 加密可被 Windows 10/11 资源管理器直接解压，但安全性较弱，不适合高敏感数据

## 🛠️ 技术栈

- **Python 3.8+**
- **PyQt5** — GUI 框架
- **pyzipper** — AES-256 加密 ZIP 支持
- **PyInstaller** — 打包为 Windows 可执行文件

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。
