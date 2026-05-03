import os
import sys
import subprocess
import socket
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "app"
RUNTIME_PYTHON = ROOT / "runtime" / "python" / "Scripts" / "python.exe"
CACHE_DIR = ROOT / "cache"
HF_HOME = CACHE_DIR / "huggingface"
MODEL_DIR = ROOT / "models"
APP_SCRIPT = APP_DIR / "app.py"
PORT = int(os.environ.get("FIRERED_PORT", "7860"))
HOST = os.environ.get("FIRERED_HOST", "127.0.0.1")


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


def ensure_dirs():
    for p in [CACHE_DIR, HF_HOME, MODEL_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def ensure_runtime():
    if not RUNTIME_PYTHON.exists():
        print("[ERROR] Missing embedded Python runtime:", RUNTIME_PYTHON) # 缺少内嵌 Python 运行时
        print("Run create_portable_package.ps1 first on Windows. # 请先在 Windows 上执行 create_portable_package.ps1")
        sys.exit(1)


def ensure_models():
    downloader = ROOT / "download_models.py"
    cmd = [str(RUNTIME_PYTHON), str(downloader)]
    env = os.environ.copy()
    env["HF_HOME"] = str(HF_HOME)
    env["HUGGINGFACE_HUB_CACHE"] = str(HF_HOME / "hub")
    env["TRANSFORMERS_CACHE"] = str(HF_HOME / "transformers")
    env["HF_HUB_DISABLE_TELEMETRY"] = "1"
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print("[ERROR] Model download step failed. # 模型下载步骤失败")
        sys.exit(result.returncode)


def launch_app():
    env = os.environ.copy()
    env["HF_HOME"] = str(HF_HOME)
    env["HUGGINGFACE_HUB_CACHE"] = str(HF_HOME / "hub")
    env["TRANSFORMERS_CACHE"] = str(HF_HOME / "transformers")
    env["HF_HUB_DISABLE_TELEMETRY"] = "1"
    env.setdefault("GRADIO_SERVER_NAME", HOST)
    env.setdefault("GRADIO_SERVER_PORT", str(PORT))
    env.setdefault("PYTHONUTF8", "1")

    cmd = [str(RUNTIME_PYTHON), str(APP_SCRIPT)]
    creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    return subprocess.Popen(cmd, cwd=str(APP_DIR), env=env, creationflags=creationflags)


def wait_and_open_browser():
    url = f"http://{HOST}:{PORT}"
    print(f"Waiting for local UI: {url} # 等待本地界面启动")
    for _ in range(180):
        if port_open(HOST, PORT):
            print(f"Opening browser: {url} # 正在打开浏览器")
            webbrowser.open(url)
            return True
        time.sleep(1)
    print("[WARN] App did not become reachable within timeout. # 启动超时，未检测到服务端口")
    return False


def main():
    ensure_dirs()
    ensure_runtime()
    ensure_models()
    proc = launch_app()
    opened = wait_and_open_browser()
    if not opened:
        print(f"App process pid={proc.pid} still running. Check the app window. # 程序进程仍在运行，请查看应用控制台")


if __name__ == "__main__":
    main()
