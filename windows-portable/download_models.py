import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
HF_HOME = CACHE_DIR / "huggingface"
MODELS_DIR = ROOT / "models"

FIRERED_BASE = "FireRedTeam/FireRed-Image-Edit-1.1"
FIRERED_TRANSFORMER = "prithivMLmods/Qwen-Image-Edit-Rapid-AIO-V19"


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    HF_HOME.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("HF_HOME", str(HF_HOME))
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(HF_HOME / "hub"))
    os.environ.setdefault("TRANSFORMERS_CACHE", str(HF_HOME / "transformers"))
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

    try:
        from huggingface_hub import snapshot_download
    except Exception as e:
        print("[ERROR] huggingface_hub import failed:", e) # 导入 huggingface_hub 失败
        return 1

    try:
        print(f"Downloading/checking model: {FIRERED_BASE} # 下载/检查基础模型")
        base_path = snapshot_download(
            repo_id=FIRERED_BASE,
            local_dir=str(MODELS_DIR / "FireRed-Image-Edit-1.1"),
            local_dir_use_symlinks=False,
            resume_download=True,
        )
        print("Base model ready:", base_path) # 基础模型已就绪

        print(f"Downloading/checking transformer: {FIRERED_TRANSFORMER} # 下载/检查加速Transformer")
        rapid_path = snapshot_download(
            repo_id=FIRERED_TRANSFORMER,
            local_dir=str(MODELS_DIR / "Qwen-Image-Edit-Rapid-AIO-V19"),
            local_dir_use_symlinks=False,
            resume_download=True,
        )
        print("Transformer model ready:", rapid_path) # Transformer模型已就绪
    except Exception as e:
        print("[ERROR] Model download failed:", e) # 模型下载失败
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
