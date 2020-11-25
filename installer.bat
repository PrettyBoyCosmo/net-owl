REM Get Admin Permissions For Installation
@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

REM Confirm Installation
echo *By selecting "y" or "Y" you are confirming that you will not use this code maliciously or illegally
echo Are you sure you want to lock install "Net-Owl" (Y/N)
set/p "cho=>"
if %cho%==Y goto INSTALL
if %cho%==y goto INSTALL
if %cho%==n goto END
if %cho%==N goto END
echo Invalid choice.
goto END

REM Start Installation
:INSTALL
echo Setting Up Installer...
attrib -h -s -r encrypted.key
attrib -h -s -r credentials.txt

REM Installs Python Dependencies
echo Installing Python Modules...
pip install termcolor
pip install cryptography
echo Modules Installed!

REM Lock Encrypted Files
echo Locking Encryption Key...
attrib +h +s +r encrypted.key
echo Locking Credentials File
attrib +h +s +r encrypted.key
echo Files Locked!
goto RUN

REM Runs Net Owl
:RUN
echo Starting net-owl...
start py -3.8 net-owl.py
goto END

REM Exits Installer
:End
exit
