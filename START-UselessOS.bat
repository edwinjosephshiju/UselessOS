@echo off
setlocal enabledelayedexpansion

:: 1. Anchor script to repository root directory
cd /d "%~dp0"

echo ========================================
echo         UselessOS 3.0 Launcher
echo   TinkerHub Useless Projects Edition
echo ========================================
echo.

:: 2. Dynamic VirtualBox tool resolution
set "VBOXMANAGE="

where VBoxManage.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "VBOXMANAGE=VBoxManage.exe"
    goto :found_vbox
)

if defined VBOX_MSI_INSTALL_PATH (
    if exist "%VBOX_MSI_INSTALL_PATH%VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_MSI_INSTALL_PATH%VBoxManage.exe"
        goto :found_vbox
    )
    if exist "%VBOX_MSI_INSTALL_PATH%\VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_MSI_INSTALL_PATH%\VBoxManage.exe"
        goto :found_vbox
    )
)

if defined VBOX_INSTALL_PATH (
    if exist "%VBOX_INSTALL_PATH%VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_INSTALL_PATH%VBoxManage.exe"
        goto :found_vbox
    )
    if exist "%VBOX_INSTALL_PATH%\VBoxManage.exe" (
        set "VBOXMANAGE=%VBOX_INSTALL_PATH%\VBoxManage.exe"
        goto :found_vbox
    )
)

if exist "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" (
    set "VBOXMANAGE=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    goto :found_vbox
)

if exist "C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe" (
    set "VBOXMANAGE=C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe"
    goto :found_vbox
)

echo [ERROR] VirtualBox was not detected on your system.
echo Please install Oracle VM VirtualBox or ensure VBoxManage.exe is in your PATH.
echo.
pause
exit /b 1

:found_vbox
echo [OK] VirtualBox detected: "%VBOXMANAGE%"

:: 3. Check for UselessOS VM registration & status
echo [INFO] Querying UselessOS VM registration...
set "VM_NAME=UselessOS"
set "VM_REGISTERED=0"
for /f "tokens=1 delims= " %%A in ('"%VBOXMANAGE%" list vms 2^>nul') do (
    if /i "%%~A"=="UselessOS" (
        set "VM_NAME=UselessOS"
        set "VM_REGISTERED=1"
    )
    if /i "%%~A"=="UselessOS_bak" (
        set "VM_NAME=UselessOS_bak"
        set "VM_REGISTERED=1"
    )
)

if !VM_REGISTERED! EQU 0 (
    echo [INFO] "UselessOS" VM is not yet registered in VirtualBox.
    
    :: Check if existing machine files are already on disk
    if exist "%USERPROFILE%\VirtualBox VMs\UselessOS\UselessOS.vbox" (
        echo [INFO] Found existing UselessOS VM files on disk. Registering...
        "%VBOXMANAGE%" registervm "%USERPROFILE%\VirtualBox VMs\UselessOS\UselessOS.vbox"
        if !ERRORLEVEL! EQU 0 (
            set "VM_NAME=UselessOS"
            set "VM_REGISTERED=1"
            echo [SUCCESS] Registered existing UselessOS VM successfully!
            goto :registered_check_done
        )
    )
    if exist "%USERPROFILE%\VirtualBox VMs\UselessOS_bak\UselessOS_bak.vbox" (
        echo [INFO] Found existing UselessOS_bak VM files on disk. Registering...
        "%VBOXMANAGE%" registervm "%USERPROFILE%\VirtualBox VMs\UselessOS_bak\UselessOS_bak.vbox"
        if !ERRORLEVEL! EQU 0 (
            set "VM_NAME=UselessOS_bak"
            set "VM_REGISTERED=1"
            echo [SUCCESS] Registered existing UselessOS_bak VM successfully!
            goto :registered_check_done
        )
    )
    
    echo [INFO] Attempting to import release appliance...
    
    if not exist "release\UselessOS.ova" (
        echo [ERROR] Cannot find "release\UselessOS.ova"!
        echo Please ensure you have downloaded the release OVA into the release\ folder.
        echo.
        pause
        exit /b 1
    )
    
    echo [INFO] Importing release\UselessOS.ova into VirtualBox...
    echo [INFO] This may take 30-60 seconds depending on disk speed...
    "%VBOXMANAGE%" import "release\UselessOS.ova" --vsys 0 --vmname "UselessOS"
    
    if errorlevel 1 (
        echo [ERROR] Failed to import OVA appliance.
        echo Please verify you have at least 5GB free disk space.
        echo If an earlier failed import left orphaned media, open VirtualBox,
        echo navigate to File ^> Virtual Media Manager, remove any unused disks, and retry.
        echo.
        pause
        exit /b 1
    )
    echo [SUCCESS] Import successful!
) else (
    echo [OK] UselessOS VM is registered in VirtualBox.
)

:registered_check_done

:: 4. Evaluate machine state
echo [INFO] Checking runtime state...
set "VM_RUNNING=0"
for /f "tokens=1 delims= " %%A in ('"%VBOXMANAGE%" list runningvms 2^>nul') do (
    if /i "%%~A"=="!VM_NAME!" set "VM_RUNNING=1"
    if /i "%%~A"=="UselessOS" set "VM_RUNNING=1"
    if /i "%%~A"=="UselessOS_bak" set "VM_RUNNING=1"
)

if !VM_RUNNING! EQU 1 (
    echo [INFO] !VM_NAME! is ALREADY running!
    echo.
    echo If the window is not visible or was started in a background session:
    echo   1. Run: "%VBOXMANAGE%" controlvm "!VM_NAME!" poweroff
    echo   2. Re-run this launcher to start the GUI window directly on your desktop.
    echo.
    echo Attempting to bring VirtualBox window into focus...
    "%VBOXMANAGE%" startvm "!VM_NAME!" --type gui >nul 2>&1
    goto :boot_success
)

:: 5. Boot VM
echo [INFO] Starting UselessOS Graphical Shell (!VM_NAME!)...
"%VBOXMANAGE%" startvm "!VM_NAME!" --type gui

if errorlevel 1 (
    echo.
    echo [ERROR] VirtualBox failed to start UselessOS.
    echo If another VirtualBox instance is locked, please close it and retry.
    echo.
    pause
    exit /b 1
)

:boot_success
echo.
echo ========================================
echo        USELESSOS IS NOW RUNNING!
echo ========================================
echo.
echo  * Host Key Shortcut : Press RIGHT CTRL to release mouse/keyboard back to Windows.
echo  * Fullscreen Mode   : Press RIGHT CTRL + F to toggle fullscreen display.
echo  * Credentials       : User: vagrant ^| Password: vagrant (Auto-login active).
echo  * Native UI         : TinkerHub Brutalist macOS Shell running on Openbox + X11.
echo.
echo Press any key to close this launcher window (the VM will keep running)...
pause >nul
exit /b 0
