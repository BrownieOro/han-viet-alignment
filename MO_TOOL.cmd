@echo off
cd /d "%~dp0"
start "" "http://127.0.0.1:7070"
python cong_cu\serve_review.py
pause
