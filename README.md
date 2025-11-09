# 端口映射GUI工具 (Port Mapper)

Windows端口映射工具，用于将本地22端口映射到远程服务器的指定IP和端口。

## 功能特点

- 🖥️ 简洁的图形用户界面
- 🔄 一键创建/删除端口映射
- ✅ 自动验证IP地址和端口格式
- 📊 实时状态显示和日志记录
- 🔍 自动检测现有映射
- 💡 本地端口默认使用22 (SSH)

## 系统要求

- Windows 7/8/10/11
- Python 3.6+ (如果运行.py文件)
- 管理员权限

## 使用方法

### 方式一：直接运行exe文件（推荐）

1. 右键点击 `port_map.exe`
2. 选择"以管理员身份运行"
3. 在"远程IP地址"框中输入服务器提供的IP地址
4. 在"远程端口"框中输入服务器提供的端口号
5. 点击"映射"按钮完成端口映射

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
本地22端口 → 远程IP:远程端口
```

实际执行的命令：
```powershell
netsh interface portproxy add v4tov4 listenport=22 listenaddress=0.0.0.0 connectport=[远程端口] connectaddress=[远程IP]
```

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
