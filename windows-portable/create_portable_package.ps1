param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [Parameter(Mandatory = $true)]
    [string]$OutDir,

    [string]$PythonExe = "python",
    [switch]$SkipModelDownload
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) {
    Write-Host "`n==== $msg ==== # $msg"
}

$RepoPath = (Resolve-Path $RepoPath).Path
if (-not (Test-Path $RepoPath)) {
    throw "RepoPath not found: $RepoPath # 源码目录不存在"
}

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}
$OutDir = (Resolve-Path $OutDir).Path

$PortableRoot = Join-Path $OutDir "FireRed-Portable"
$RuntimeDir = Join-Path $PortableRoot "runtime"
$PythonDir = Join-Path $RuntimeDir "python"
$AppDir = Join-Path $PortableRoot "app"
$ModelsDir = Join-Path $PortableRoot "models"
$CacheDir = Join-Path $PortableRoot "cache"
$KitDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Step "Preparing directories"
Remove-Item -Recurse -Force $PortableRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $PortableRoot, $RuntimeDir, $PythonDir, $AppDir, $ModelsDir, $CacheDir | Out-Null

Write-Step "Copying app source"
robocopy $RepoPath $AppDir /E /XD .git .github windows-portable /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit code $LASTEXITCODE # 复制源码失败"
}

Write-Step "Copying launcher kit"
Copy-Item -Force (Join-Path $KitDir "Launch-FireRed.bat") $PortableRoot
Copy-Item -Force (Join-Path $KitDir "start_portable.py") $PortableRoot
Copy-Item -Force (Join-Path $KitDir "download_models.py") $PortableRoot

Write-Step "Creating virtual environment"
& $PythonExe -m venv $PythonDir
$EmbeddedPython = Join-Path $PythonDir "Scripts\python.exe"
$EmbeddedPip = Join-Path $PythonDir "Scripts\pip.exe"

Write-Step "Upgrading pip"
& $EmbeddedPython -m pip install --upgrade pip setuptools wheel

Write-Step "Installing torch CUDA build"
& $EmbeddedPip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

Write-Step "Installing app requirements"
& $EmbeddedPip install -r (Join-Path $AppDir "pre-requirements.txt")
& $EmbeddedPip install -r (Join-Path $AppDir "requirements.txt")
& $EmbeddedPip install huggingface_hub safetensors sentencepiece pillow

if (-not $SkipModelDownload) {
    Write-Step "Pre-downloading models"
    $env:HF_HOME = (Join-Path $CacheDir "huggingface")
    $env:HUGGINGFACE_HUB_CACHE = (Join-Path $env:HF_HOME "hub")
    $env:TRANSFORMERS_CACHE = (Join-Path $env:HF_HOME "transformers")
    & $EmbeddedPython (Join-Path $PortableRoot "download_models.py")
}

Write-Step "Done"
Write-Host "Portable package created at: $PortableRoot # 便携包已生成"
Write-Host "End users can now double-click Launch-FireRed.bat # 用户现在可以双击 Launch-FireRed.bat"
