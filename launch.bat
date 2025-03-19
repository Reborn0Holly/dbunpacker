@echo off
chcp 65001 >nul
title dbunpacker
echo Запуск программы dbunpacker.py...


if not exist "venv\Scripts\activate.bat" (
    echo Виртуальная среда не найдена. Запускаем настройку...
    python setup.py
    if errorlevel 1 (
        echo Ошибка при настройке виртуальной среды. Завершение...
        pause
        exit /b 1
    )
)


call venv\Scripts\activate.bat


python dbunpacker.py


deactivate

echo Программа завершена.
pause
