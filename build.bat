@echo off
REM 端口映射工具打包脚本
REM 使用PyInstaller将Python程序打包成单个exe文件

echo =====================================
echo 端口映射工具 - 打包脚本
echo =====================================
echo.

REM 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未检测到PyInstaller
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo [信息] 开始打包程序...
echo.

REM 清理之前的打包文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist port_map.spec del /q port_map.spec

REM 使用PyInstaller打包
REM --onefile: 打包成单个exe文件
REM --windowed: 不显示控制台窗口（GUI程序）
REM --name: 指定输出文件名
REM --icon: 指定图标（如果有的话）
REM --add-data: 添加额外的数据文件
REM --clean: 清理临时文件

python -m PyInstaller  --onefile ^
    --windowed ^
    --name port_map ^
    --clean ^
    port_map.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo =====================================
echo [成功] 打包完成！
echo =====================================
echo.
echo 生成的exe文件位于: dist\port_map.exe
echo.
echo 提示：运行port_map.exe时需要以管理员身份运行
echo.

REM 可选：自动打开dist目录
explorer dist

pause
