@echo off
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Limpando arquivos antigos...
rmdir /s /q build dist __pycache__ >nul 2>&1
del desktop.spec >nul 2>&1

echo Gerando novo .exe...
pyinstaller --onefile --windowed --icon=icon.ico ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  desktop.py

echo.
echo Build finalizado! Pressione qualquer tecla para sair.
pause >nul
