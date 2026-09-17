# Agent Genesis Kit — One-Liner Installer for Windows
# Architected by Viktor (Vik) - Viklabs (https://viklab.net)
# Usage: irm https://raw.githubusercontent.com/xvacorx/agent-genesis-kit/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  ⚡ AGENT GENESIS KIT — Bootstrap & Onboarding Matrix   " -ForegroundColor Cyan
Write-Host "  Architected by Viktor (Vik) — Viklabs.net              " -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$targetDir = Get-Location
$repoUrl = "https://github.com/xvacorx/agent-genesis-kit"
$zipUrl = "https://github.com/xvacorx/agent-genesis-kit/archive/refs/heads/main.zip"
$tempZip = Join-Path $env:TEMP "agent-genesis-kit.zip"
$tempExtract = Join-Path $env:TEMP "agent-genesis-kit-extract"

# Check if git is available
$hasGit = $false
try {
    $null = git --version 2>&1
    $hasGit = $true
} catch {
    $hasGit = $false
}

if ($hasGit) {
    Write-Host "📦 Git detected! Cloning repository..." -ForegroundColor Green
    $genesisFolder = Join-Path $targetDir "agent-genesis-kit"
    if (Test-Path $genesisFolder) {
        Write-Host "ℹ️  Folder 'agent-genesis-kit' already exists. Updating..." -ForegroundColor Yellow
        git -C $genesisFolder pull
    } else {
        git clone $repoUrl $genesisFolder
    }
} else {
    Write-Host "🌐 Git not found. Downloading release package directly via HTTPS..." -ForegroundColor Yellow
    
    if (Test-Path $tempExtract) { Remove-Item $tempExtract -Recurse -Force }
    Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip -UseBasicParsing
    
    Write-Host "📂 Extracting files..." -ForegroundColor Green
    Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
    
    $extractedRoot = Join-Path $tempExtract "agent-genesis-kit-main"
    $genesisFolder = Join-Path $targetDir "agent-genesis-kit"
    
    if (Test-Path $genesisFolder) {
        Write-Host "ℹ️  Folder 'agent-genesis-kit' already exists. Merging..." -ForegroundColor Yellow
    } else {
        New-Item -ItemType Directory -Path $genesisFolder | Out-Null
    }
    
    Copy-Item -Path "$extractedRoot\*" -Destination $genesisFolder -Recurse -Force
    Remove-Item $tempZip -Force -ErrorAction SilentlyContinue
    Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  ✅ INSTALLATION COMPLETE!                               " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next Steps to start your AI assistant:" -ForegroundColor White
Write-Host "  1. Open Antigravity IDE, Claude Code, or Cursor." -ForegroundColor Gray
Write-Host "  2. Open the folder: $genesisFolder" -ForegroundColor Cyan
Write-Host "  3. Open the chat and type:" -ForegroundColor Gray
Write-Host "     /setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "✨ Created by Viktor (Vik) at Viklabs — https://viklab.net" -ForegroundColor DarkGray
Write-Host ""
