$ErrorActionPreference = "Stop"
$toolsDir = "C:\Users\VRUNDA\tools"
if (!(Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null
}

Write-Host "1. Downloading MinGit..."
$gitZip = Join-Path $toolsDir "mingit.zip"
$gitDir = Join-Path $toolsDir "git"
if (!(Test-Path (Join-Path $gitDir "cmd\git.exe"))) {
    Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/MinGit-2.45.0-64-bit.zip" -OutFile $gitZip
    Expand-Archive -Path $gitZip -DestinationPath $gitDir -Force
    Remove-Item $gitZip -Force
    Write-Host "MinGit installed successfully."
} else {
    Write-Host "MinGit already installed."
}

Write-Host "2. Downloading Node.js..."
$nodeZip = Join-Path $toolsDir "node.zip"
$nodeDir = Join-Path $toolsDir "nodejs"
if (!(Test-Path (Join-Path $nodeDir "node.exe"))) {
    Invoke-WebRequest -Uri "https://nodejs.org/dist/v20.18.0/node-v20.18.0-win-x64.zip" -OutFile $nodeZip
    Expand-Archive -Path $nodeZip -DestinationPath $toolsDir -Force
    Rename-Item (Join-Path $toolsDir "node-v20.18.0-win-x64") $nodeDir -Force
    Remove-Item $nodeZip -Force
    Write-Host "Node.js installed successfully."
} else {
    Write-Host "Node.js already installed."
}

Write-Host "3. Downloading uv (Python manager)..."
$uvZip = Join-Path $toolsDir "uv.zip"
$uvDir = Join-Path $toolsDir "uv"
if (!(Test-Path (Join-Path $uvDir "uv.exe"))) {
    Invoke-WebRequest -Uri "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip" -OutFile $uvZip
    Expand-Archive -Path $uvZip -DestinationPath $uvDir -Force
    Remove-Item $uvZip -Force
    Write-Host "uv installed successfully."
} else {
    Write-Host "uv already installed."
}

Write-Host "All tools downloaded successfully."
