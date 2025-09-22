; Nome do instalador e app
OutFile "dist\AnaliseBeneficiarios-Setup.exe"
InstallDir "$PROGRAMFILES\AnaliseBeneficiarios"
InstallDirRegKey HKCU "Software\AnaliseBeneficiarios" "Install_Dir"
RequestExecutionLevel admin

; Página padrão do instalador
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

; Seção principal de instalação
Section "Instalar"
  SetOutPath "$INSTDIR"
  File "dist\Analise Beneficiarios.exe"
  WriteRegStr HKCU "Software\AnaliseBeneficiarios" "Install_Dir" "$INSTDIR"

  ; Atalho no menu iniciar
  CreateDirectory "$SMPROGRAMS\Analise Beneficiarios"
  CreateShortcut "$SMPROGRAMS\Analise Beneficiarios\Analise Beneficiarios.lnk" "$INSTDIR\Analise Beneficiarios.exe"

  ; Atalho na área de trabalho
  CreateShortcut "$DESKTOP\Analise Beneficiarios.lnk" "$INSTDIR\Analise Beneficiarios.exe"
SectionEnd

; Seção de desinstalação
Section "Uninstall"
  Delete "$INSTDIR\Analise Beneficiarios.exe"
  RMDir /r "$INSTDIR"

  Delete "$SMPROGRAMS\Analise Beneficiarios\Analise Beneficiarios.lnk"
  RMDir "$SMPROGRAMS\Analise Beneficiarios"

  Delete "$DESKTOP\Analise Beneficiarios.lnk"

  DeleteRegKey HKCU "Software\AnaliseBeneficiarios"
SectionEnd
