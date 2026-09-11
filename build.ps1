param(
    [switch]$SkipExport
)

$ErrorActionPreference = "Stop"

# Anchor execution to script directory
Set-Location $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   UselessOS 3.0 Build System" -ForegroundColor Cyan
Write-Host "   TinkerHub Useless Projects Edition" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Resolve Vagrant executable dynamically
$vagrantCmd = Get-Command vagrant -ErrorAction SilentlyContinue
if ($vagrantCmd) {
    $vagrant = $vagrantCmd.Source
} elseif (Test-Path "C:\Program Files\Vagrant\bin\vagrant.exe") {
    $vagrant = "C:\Program Files\Vagrant\bin\vagrant.exe"
} elseif (Test-Path "C:\HashiCorp\Vagrant\bin\vagrant.exe") {
    $vagrant = "C:\HashiCorp\Vagrant\bin\vagrant.exe"
} else {
    Write-Host "Error: Vagrant is not installed or not found in PATH." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Vagrant found: $vagrant" -ForegroundColor Green

# 2. Resolve VBoxManage executable dynamically
$vboxCmd = Get-Command VBoxManage -ErrorAction SilentlyContinue
if ($vboxCmd) {
    $vboxmanage = $vboxCmd.Source
} elseif ($env:VBOX_MSI_INSTALL_PATH -and (Test-Path "$($env:VBOX_MSI_INSTALL_PATH)VBoxManage.exe")) {
    $vboxmanage = "$($env:VBOX_MSI_INSTALL_PATH)VBoxManage.exe"
} elseif ($env:VBOX_INSTALL_PATH -and (Test-Path "$($env:VBOX_INSTALL_PATH)VBoxManage.exe")) {
    $vboxmanage = "$($env:VBOX_INSTALL_PATH)VBoxManage.exe"
} elseif (Test-Path "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe") {
    $vboxmanage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
} elseif (Test-Path "C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe") {
    $vboxmanage = "C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe"
} else {
    Write-Host "Error: VirtualBox (VBoxManage.exe) is not installed or not found in PATH." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] VirtualBox found: $vboxmanage" -ForegroundColor Green

Write-Host "`n[1/3] Building and Provisioning Virtual Machine..." -ForegroundColor Cyan
& $vagrant up --provision

Write-Host "`n[2/3] Halting Virtual Machine..." -ForegroundColor Cyan
& $vagrant halt

if (-not $SkipExport) {
    Write-Host "`n[3/3] Exporting to OVA..." -ForegroundColor Cyan
    if (-not (Test-Path "release")) {
        New-Item -ItemType Directory -Path "release" | Out-Null
    }
    
    $ovaPath = "release\UselessOS.ova"
    if (Test-Path $ovaPath) {
        Remove-Item $ovaPath -Force
    }
    
    & $vboxmanage export "UselessOS" -o $ovaPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nBuild Complete! OVA saved to: $ovaPath" -ForegroundColor Green
    } else {
        Write-Host "`nFailed to export OVA." -ForegroundColor Red
    }
} else {
    Write-Host "`nBuild Complete! (Skipped export)" -ForegroundColor Green
}
