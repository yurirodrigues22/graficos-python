@echo off
echo ==================================
echo ATUALIZANDO APP: Analise Beneficiarios
echo ==================================

REM 1) Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate

REM 2) Gerar executável com PyInstaller
echo ==================================
echo GERANDO EXECUTAVEL COM PYINSTALLER...
echo ==================================
pyinstaller ^
  --noconfirm ^
  --onefile ^
  --noconsole ^
  --icon=icon.ico ^
  --name "Analise Beneficiarios" ^
  --distpath dist ^
  --hidden-import pandas ^
  --hidden-import seaborn ^
  --hidden-import matplotlib ^
  --collect-all seaborn ^
  --collect-all pandas ^
  --collect-all matplotlib ^
  main.py


IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: Nao foi possivel gerar o executavel.
    pause
    exit /b %ERRORLEVEL%
)

REM 3) Criar instalador com NSIS (se existir o .nsi)
echo ==================================
echo CRIANDO INSTALADOR COM NSIS...
echo ==================================
IF EXIST installer.nsi (
    "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
) ELSE (
    echo Nenhum arquivo installer.nsi encontrado. Pulando etapa do instalador.
)

echo ==================================
echo PROCESSO FINALIZADO COM SUCESSO!
echo ==================================
pause
