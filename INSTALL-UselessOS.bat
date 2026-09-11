@echo off
setlocal enabledelayedexpansion

:: 1. Anchor script to repository root directory
cd /d "%~dp0"

echo ========================================
echo         UselessOS 3.0 Installer
echo   TinkerHub Useless Projects Edition
echo ========================================
echo.
echo This script will verify dependencies, configure VirtualBox,
echo and import the pre-built UselessOS appliance.
echo.
pause

:: 2. Dynamic VirtualBox tool resolution
echo [1/3] Checking for VirtualBox...
set "VBOXMANAGE="

where VBoxManage.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "VBOXMANAGE=VBoxManage.exe"
    goto :vbox_ready
)

if defined VBOX_MSI_INSTALL_PATH (
    if exist "%VBOX_MSI_INSTALL_PATH%VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_MSI_INSTALL_PATH%VBoxManage.exe"
        goto :vbox_ready
    )
    if exist "%VBOX_MSI_INSTALL_PATH%\VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_MSI_INSTALL_PATH%\VBoxManage.exe"
        goto :vbox_ready
    )
)

if defined VBOX_INSTALL_PATH (
    if exist "%VBOX_INSTALL_PATH%VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_INSTALL_PATH%VBoxManage.exe"
        goto :vbox_ready
    )
    if exist "%VBOX_INSTALL_PATH%\VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_INSTALL_PATH%\VBoxManage.exe"
        goto :vbox_ready
    )
)

if exist "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" (
    set "VBOXMANAGE=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    goto :vbox_ready
)

if exist "C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe" (
    set "VBOXMANAGE=C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe"
    goto :vbox_ready
)

echo [INFO] VirtualBox not found. Attempting automatic installation via winget...
winget install -e --id Oracle.VirtualBox --accept-package-agreements --accept-source-agreements
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Automatic installation of VirtualBox failed.
    echo Please install Oracle VirtualBox manually from https://www.virtualbox.org/
    echo and re-run this installer.
    echo.
    pause
    exit /b 1
)

:: Check again after winget
if exist "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" (
    set "VBOXMANAGE=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
) else (
    set "VBOXMANAGE=VBoxManage.exe"
)

:vbox_ready
echo [OK] VirtualBox detected: "%VBOXMANAGE%"

:: 3. Checking for release appliance
echo.
echo [2/3] Checking for UselessOS OVA appliance...
if not exist "release\UselessOS.ova" (
    echo.
    echo [ERROR] Cannot find "release\UselessOS.ova"!
    echo Please ensure the OVA file exists in the release\ folder, or build it using:
    echo    powershell -ExecutionPolicy Bypass -File .\build.ps1
    echo.
    pause
    exit /b 1
)
echo [OK] Found "release\UselessOS.ova"

:: 4. Import appliance into VirtualBox
echo.
echo [3/3] Registering UselessOS in VirtualBox...
set "VM_REGISTERED=0"
for /f "tokens=1 delims= " %%A in ('"%VBOXMANAGE%" list vms 2^>nul') do (
    if /i "%%~A"=="UselessOS" set "VM_REGISTERED=1"
)

if !VM_REGISTERED! EQU 1 (
    echo [INFO] "UselessOS" VM is already registered in VirtualBox.
) else (
    if exist "%USERPROFILE%\VirtualBox VMs\UselessOS\UselessOS.vbox" (
        echo [INFO] Found existing UselessOS VM on disk. Registering...
        "%VBOXMANAGE%" registervm "%USERPROFILE%\VirtualBox VMs\UselessOS\UselessOS.vbox"
        if !ERRORLEVEL! EQU 0 (
            echo [OK] UselessOS registered successfully!
            goto :install_done
        )
    )
    echo [INFO] Importing release\UselessOS.ova... This may take a moment.
    "%VBOXMANAGE%" import "release\UselessOS.ova" --vsys 0 --vmname "UselessOS"
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to import OVA into VirtualBox.
        echo Please verify you have at least 5GB free disk space and VirtualBox permissions.
        echo If an earlier failed import left orphaned media, open VirtualBox,
        echo navigate to File ^> Virtual Media Manager, remove any unused disks, and retry.
        echo.
        pause
        exit /b 1
    )
    echo [OK] UselessOS imported successfully!
)

:install_done

echo.
echo ========================================
echo         INSTALLATION COMPLETE!
echo ========================================
echo.
echo You can now run "START-UselessOS.bat" to launch the operating system.
echo.
pause
exit /b 0
