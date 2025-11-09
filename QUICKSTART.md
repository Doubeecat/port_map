# 快速使用指南

## 第一次使用

1. **打包程序**（首次需要）
   - 以管理员身份运行PowerShell
   - 切换到程序目录：`cd e:\MaVis\port_map`
   - 运行：`.\build.bat`
   - 等待打包完成，生成的exe在 `dist\port_map.exe`

2. **运行程序**
   - 右键点击 `port_map.exe`
   - 选择"以管理员身份运行"

3. **创建端口映射**
   - 输入远程IP地址（例如：192.168.1.100）
   - 输入远程端口（例如：2222）
   - 点击"映射"按钮

## 直接运行Python脚本（无需打包）

如果你已经安装了Python，可以直接运行：

```powershell
# 以管理员身份运行PowerShell
cd e:\MaVis\port_map
python port_map.py
```

## 验证映射是否成功

在管理员PowerShell中运行：
```powershell
netsh interface portproxy show all
```

应该能看到类似输出：
```
侦听 ipv4:                 连接到 ipv4:

地址            端口        地址            端口
--------------- ----------  --------------- ----------
0.0.0.0         22          192.168.1.100   2222
```

## 测试连接

映射成功后，可以使用SSH客户端连接到本地22端口：
```powershell
ssh user@localhost -p 22
```

这将自动转发到远程服务器的指定端口。
