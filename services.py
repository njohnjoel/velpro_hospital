import subprocess
import sys
import os
import shutil
from pathlib import Path
from typing import Optional

# ...existing code...

# Lists of services to manage
SERVICES_DISABLE = [
    "DiagTrack",
    "dmwappushservice",
    "MapsBroker",
    "XblAuthManager",
    "XblGameSave",
    "XboxNetApiSvc",
    "XboxGipSvc",
    "RetailDemo",
    "WerSvc",
    "lfsvc",
    "WSearch",
    "SysMain"
]

SERVICES_MANUAL = [
    "DoSvc",
    "DusmSvc",
    "SSDPSRV",
    "RemoteRegistry",
    "PhoneSvc"
]


def run_ps(command: str, capture: bool = False) -> Optional[subprocess.CompletedProcess]:
    """
    Run a PowerShell command. Returns CompletedProcess if capture=True, otherwise prints output.
    """
    args = ["powershell", "-NoProfile", "-NonInteractive", "-Command", command]
    try:
        if capture:
            proc = subprocess.run(args, capture_output=True, text=True, check=False)
            return proc
        else:
            subprocess.run(args, check=False)
            return None
    except Exception as e:
        # keep output concise
        print(f"run_ps error: {e}")
        return None


def optimize_user_services():
    print("Applying Business Safe Service Optimization...\n")

    for svc in SERVICES_DISABLE:
        run_ps(f"Stop-Service {svc} -Force -ErrorAction SilentlyContinue")
        run_ps(f"Set-Service {svc} -StartupType Disabled")

    for svc in SERVICES_MANUAL:
        run_ps(f"Set-Service {svc} -StartupType Manual")

    print("\nUser Service Optimization Completed.\n")


def stop():
    """
    Stop all services listed in SERVICES_DISABLE and SERVICES_MANUAL.
    Uses -Force and SilentlyContinue to avoid throwing on already-stopped or missing services.
    """
    print("Stopping listed services...\n")
    for svc in SERVICES_DISABLE + SERVICES_MANUAL:
        run_ps(f"Stop-Service {svc} -Force -ErrorAction SilentlyContinue")
    print("\nAll listed services stop attempted.\n")


def prepare():
    """
    Perform project-local cleanup and installation tasks, then apply service optimization.
    - Cleans project temp folder (./temp) if present.
    - Creates ./logs folder.
    - If requirements.txt exists in project root, runs pip install -r requirements.txt.
    - Calls optimize_user_services().
    """
    project_root = Path(__file__).resolve().parent
    temp_dir = project_root / "temp"
    logs_dir = project_root / "logs"
    requirements = project_root / "requirements.txt"

    print("Prepare: starting cleanup and installation tasks...\n")

    # Clean project temp folder (safe, project-local)
    if temp_dir.exists() and temp_dir.is_dir():
        try:
            for item in temp_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
            print(f"Cleaned project temp folder: {temp_dir}")
        except Exception as e:
            print(f"Failed to clean temp folder: {e}")
    else:
        print(f"No project temp folder to clean at: {temp_dir}")

    # Ensure logs directory exists
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        print(f"Ensured logs directory exists: {logs_dir}")
    except Exception as e:
        print(f"Failed to ensure logs directory: {e}")

    # Optional: install requirements if present
    if requirements.exists() and requirements.is_file():
        print("requirements.txt found, running pip install -r requirements.txt ...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)], check=False)
            print("pip install completed (non-fatal on failure).")
        except Exception as e:
            print(f"pip install failed: {e}")
    else:
        print("No requirements.txt found, skipping pip install.")

    # Apply service optimization
    optimize_user_services()

    print("Prepare: completed.\n")

