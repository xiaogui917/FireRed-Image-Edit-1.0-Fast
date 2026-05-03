@echo off
setlocal
cd /d "%~dp0"

echo Starting FireRed portable launcher... # 启动 FireRed 便携启动器
"%~dp0runtime\python\Scripts\python.exe" "%~dp0start_portable.py"
if errorlevel 1 (
  echo.
  echo Launch failed. Check the console output above. # 启动失败，请查看上方输出
  pause
)
