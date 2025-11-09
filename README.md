# Port Mapper

Windows port mapping tool to forward remote port to local port.

[![GitHub release](https://img.shields.io/github/v/release/yourusername/port_map)](https://github.com/yourusername/port_map/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- 🖥️ Modern GUI with resizable window
- 🔄 One-click create/delete port mapping
- ✅ Auto-validate IP address and port format
- 📊 Real-time status display with scrollable log
- 🔍 Auto-detect existing mappings
- 💡 Customizable local port (default: 22)

## Mapping Direction

**Remote IP:Port → Local 127.0.0.1:Port**

Example: Map `192.168.1.100:2222` to local `127.0.0.1:22`, so accessing remote port 2222 will forward to your local port 22 (SSH).

## Download

### Option 1: Pre-built Binary (Recommended)

Download latest `port_map.exe` from [Releases](https://github.com/yourusername/port_map/releases/latest)

### Option 2: Run from Source

```bash
git clone https://github.com/yourusername/port_map.git
cd port_map
python port_map.py
```

## Requirements

- Windows 7/8/10/11
- Python 3.6+ (if running from source)
- Administrator privileges

## Usage

### Run Executable

1. Download `port_map.exe` from [Releases](https://github.com/yourusername/port_map/releases)
2. Right-click `port_map.exe`
3. Select "Run as administrator"
4. Enter remote IP address
5. Enter remote port
6. Enter local port (default: 22)
7. Click "Create Mapping"

### Run from Source

1. Ensure Python 3.6+ is installed
2. Right-click Command Prompt or PowerShell, select "Run as administrator"
3. Navigate to project directory:
   ```powershell
   cd e:\MaVis\port_map
   ```
4. Run:
   ```powershell
   python port_map.py
   ```

## Build Executable

1. Install PyInstaller:
   ```powershell
   pip install pyinstaller
   ```

2. Run build script:
   ```powershell
   .\build.bat
   ```

3. Find executable at `dist\port_map.exe`

## How It Works

Uses Windows built-in `netsh` command for port forwarding:

```
Remote IP:Port → Local 127.0.0.1:Port
```

Command executed:
```powershell
netsh interface portproxy add v4tov4 listenport=[RemotePort] listenaddress=[RemoteIP] connectport=[LocalPort] connectaddress=127.0.0.1
```

**Use Case Example**:
- You have a remote server (192.168.1.100)
- Server provides SSH on port 2222
- After mapping, accessing `192.168.1.100:2222` forwards to your local port 22

## Interface Guide

- **Remote IP Address**: Enter server IP (e.g., 192.168.1.100)
- **Remote Port**: Enter server port (e.g., 2222)
- **Local Port**: Enter local port (default: 22)
- **Create Mapping**: Create port mapping
- **Delete Mapping**: Remove current mapping
- **Refresh**: Check current mapping status
- **Log Messages**: Operation logs and error messages

## Important Notes

⚠️ **Required**:

1. **Admin Privileges**: Must run as administrator to create/delete mappings
2. **Firewall**: Check Windows Firewall if connection fails after mapping
3. **Port Conflicts**: Mapping may fail if local port is already in use
4. **Persistence**: Mappings persist after reboot unless manually deleted

## FAQ

### Q: "Permission Denied" error?
A: Right-click and select "Run as administrator"

### Q: How to view all port mappings?
A: Run in administrator PowerShell:
```powershell
netsh interface portproxy show all
```

### Q: How to manually delete mapping?
A: Run in administrator PowerShell:
```powershell
netsh interface portproxy delete v4tov4 listenport=[Port] listenaddress=[IP]
```

### Q: Mapping created but can't connect?
A: Check:
- Remote IP and port are correct
- Windows Firewall allows the port
- Remote server is reachable (ping test)
- Remote server port is open

## Version

- Version: 1.1
- Updated: 2025-11-09
- Language: Python 3
- GUI: tkinter

## License

MIT License - For learning and internal use.

## 📦 下载

### 方式一：下载预编译版本（推荐）

从 [Releases](https://github.com/你的用户名/port_map/releases/latest) 页面下载最新的 `port_map.exe`

### 方式二：从源码运行

```bash
git clone https://github.com/你的用户名/port_map.git
cd port_map
python port_map.py
```

## 💻 系统要求

- Windows 7/8/10/11
- Python 3.6+ (如果运行.py文件)
- 管理员权限

## 🚀 使用方法

### 方式一：直接运行exe文件（推荐）

1. 从 [Releases](https://github.com/你的用户名/port_map/releases) 下载最新版 `port_map.exe`
2. 右键点击 `port_map.exe`
3. 选择"以管理员身份运行"
4. 在"远程IP地址"框中输入服务器提供的IP地址
5. 在"远程端口"框中输入服务器提供的端口号
6. 点击"创建映射"按钮完成端口映射

### 方式二：运行Python脚本

1. 确保已安装Python 3.6+
2. 右键点击命令提示符或PowerShell，选择"以管理员身份运行"
3. 切换到程序目录：
   ```powershell
   cd e:\MaVis\port_map
   ```
4. 运行程序：
   ```powershell
   python port_map.py
   ```

## 打包成exe文件

1. 安装PyInstaller：
   ```powershell
   pip install pyinstaller
   ```

2. 运行打包脚本：
   ```powershell
   .\build.bat
   ```

3. 生成的exe文件位于 `dist\port_map.exe`

## 端口映射原理

本程序使用Windows系统自带的 `netsh` 命令实现端口转发：

```
远程IP:远程端口 → 本地127.0.0.1:22
```

实际执行的命令：
```powershell
netsh interface portproxy add v4tov4 listenport=[远程端口] listenaddress=[远程IP] connectport=22 connectaddress=127.0.0.1
```

**使用场景示例**：
- 你有一台远程服务器（192.168.1.100）
- 服务器提供的SSH端口是2222
- 创建映射后，访问 `192.168.1.100:2222` 会转发到你本地的22端口

## 界面说明

- **远程IP地址**：输入服务器提供的IP地址（例如：192.168.1.100）
- **远程端口**：输入服务器提供的端口号（例如：2222）
- **映射按钮**：创建端口映射
- **删除映射按钮**：删除当前的端口映射
- **刷新状态按钮**：刷新并检查当前映射状态
- **日志信息**：显示操作日志和错误信息

## 注意事项

⚠️ **重要提示**：

1. **管理员权限**：本程序必须以管理员身份运行才能创建/删除端口映射
2. **防火墙设置**：如果映射后无法连接，请检查Windows防火墙是否允许22端口
3. **端口冲突**：如果本地22端口已被占用，映射可能失败
4. **映射持久性**：创建的映射会在系统重启后保留，除非手动删除

## 常见问题

### Q: 提示"权限不足"怎么办？
A: 必须右键程序，选择"以管理员身份运行"

### Q: 如何查看当前所有端口映射？
A: 在管理员PowerShell中运行：
```powershell
netsh interface portproxy show all
```

### Q: 如何手动删除端口映射？
A: 在管理员PowerShell中运行：
```powershell
netsh interface portproxy delete v4tov4 listenport=22 listenaddress=0.0.0.0
```

### Q: 映射成功但无法连接？
A: 检查以下几点：
- 远程服务器IP和端口是否正确
- Windows防火墙是否允许22端口
- 远程服务器是否可达（ping测试）
- 远程服务器端口是否开放

## 技术支持

如遇问题，请检查日志信息框中的错误提示，或联系技术支持。

## 版本信息

- 版本：1.0
- 更新日期：2025-11-09
- 开发语言：Python 3
- GUI框架：tkinter

## 许可证

本工具仅供学习和内部使用。
