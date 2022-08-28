@echo off
start cmd.exe /C "conda activate py310 && python D:\server\labone\manage.py runserver"
timeout 5 > NUL
start C:\"Program Files"\Google\Chrome\Application\chrome.exe "http://127.0.0.1:8000/admin/"
