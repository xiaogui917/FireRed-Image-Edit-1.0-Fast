# FireRed Windows 便携版方案 # FireRed Windows portable package plan

这个目录用于把当前项目构建成 **Windows 免手动装 Python / pip 的便携包**。# This directory builds the project into a Windows portable package without manual Python/pip setup

## 最终用户体验 # End-user experience

1. 解压整个便携包 # Extract the portable package
2. 双击 `Launch-FireRed.bat` # Double-click Launch-FireRed.bat
3. 首次自动下载模型 # Automatically download models on first run
4. 自动打开浏览器本地 UI # Automatically open the local browser UI
5. 使用本机 NVIDIA 显卡推理 # Use local NVIDIA GPU inference

## 目录文件 # Files in this directory

- `create_portable_package.ps1` # 在 Windows 构建机上生成便携包
- `start_portable.py` # 便携启动入口，会打开浏览器并启动本地 UI
- `download_models.py` # 首次或手动预下载模型
- `Launch-FireRed.bat` # 给最终用户双击启动

## 构建方式 # Build methods

### 方式 1：GitHub Actions 自动构建 # Method 1: GitHub Actions auto build

仓库已提供 `.github/workflows/build-windows-portable.yml`。# The repo includes a GitHub Actions workflow

手动触发后会：# After manual trigger it will

1. 在 GitHub 的 Windows runner 上创建便携环境 # Build a portable environment on GitHub's Windows runner
2. 安装 CUDA 版 PyTorch 与依赖 # Install CUDA PyTorch and dependencies
3. 生成 `FireRed-Portable-windows.zip` # Produce FireRed-Portable-windows.zip
4. 上传到 Actions Artifacts # Upload the package as an artifact

### 方式 2：本地 Windows 机器手动构建 # Method 2: local Windows build

```powershell
Set-ExecutionPolicy -Scope Process Bypass # 临时允许当前窗口执行脚本
.\windows-portable\create_portable_package.ps1 -RepoPath "D:\FireRed-Image-Edit-1.0-Fast" -OutDir "D:\FireRedBuild" # 本地手动构建
```

如果想在本地构建时预下载模型：# If you want local builds to pre-download models

```powershell
.\windows-portable\create_portable_package.ps1 -RepoPath "D:\FireRed-Image-Edit-1.0-Fast" -OutDir "D:\FireRedBuild" # 默认会预下载模型
```

## 硬件要求 # Hardware requirements

- Windows 10 / 11 64 位 # Windows 10 / 11 64-bit
- NVIDIA 显卡 # NVIDIA GPU
- 最新显卡驱动 # recent NVIDIA driver
- 建议 16GB+ 显存 # recommended 16GB+ VRAM

## 注意事项 # Notes

- GitHub Actions 产物默认 **不内置模型**，避免 zip 过大。# GitHub Actions artifacts do not bundle models by default to keep size manageable
- 首次启动时会自动下载：# First run downloads
  - `FireRedTeam/FireRed-Image-Edit-1.1` # base model
  - `prithivMLmods/Qwen-Image-Edit-Rapid-AIO-V19` # rapid transformer
- 当前项目源码强依赖 NVIDIA CUDA。# The current app source is strongly oriented toward NVIDIA CUDA
