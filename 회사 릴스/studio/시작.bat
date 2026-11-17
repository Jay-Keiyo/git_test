@echo off
chcp 65001 > nul
cd /d "%~dp0"
where py > nul 2>&1 && (py -3 server.py) || (python server.py)
if errorlevel 1 (
  echo.
  echo 파이썬이 없어서 제작실을 켜지 못했습니다. python.org 에서 파이썬을 설치한 뒤 다시 눌러 주세요.
  pause
)
