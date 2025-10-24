@echo off
chcp 65001 >nul
echo ========================================
echo    Xeno-canto 鸟类数据集爬虫
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境，请先安装Python
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import requests, urllib3, pathlib" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo.
echo 选择运行模式:
echo 1. 运行主爬虫程序
echo 2. 运行测试程序
echo 3. 运行使用示例
echo 4. 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo 正在启动主爬虫程序...
    python dl_xeno.py
) else if "%choice%"=="2" (
    echo 正在运行测试程序...
    python test_scraper.py
) else if "%choice%"=="3" (
    echo 正在运行使用示例...
    python examples.py
) else if "%choice%"=="4" (
    echo 退出程序
    exit /b 0
) else (
    echo 无效选择
)

echo.
echo 程序已结束
pause