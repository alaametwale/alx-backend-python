@echo off
cd /d C:\Users\M2h\alx-backend-python

REM إضافة كل الملفات
git add .

REM عمل commit برسالة تلقائية مع التاريخ والوقت
set DATETIME=%DATE%_%TIME%
git commit -m "Auto commit: %DATETIME%"

REM رفع التغييرات إلى GitHub على فرع main
git push origin main

pause
