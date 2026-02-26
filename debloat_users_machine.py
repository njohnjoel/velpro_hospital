import subprocess
import os
import sys
import urllib.request

# -----------------------------
# APPS TO REMOVE
# -----------------------------

apps_to_remove = [
    "Clipchamp.Clipchamp",
    "Microsoft.BingNews",
    "Microsoft.BingWeather",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.GamingApp",
    "Microsoft.ZuneMusic",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.GetHelp",
    "Microsoft.YourPhone",
    "Microsoft.Todos",
    "Microsoft.Windows.DevHome",
    "Microsoft.PowerAutomateDesktop",
    "MicrosoftCorporationII.QuickAssist",
    "Microsoft.OutlookForWindows",
    "MSTeams",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.WindowsCamera",
    "Microsoft.Paint",
    "Microsoft.Windows.Photos",
    "Microsoft.MicrosoftStickyNotes",
    "Microsoft.WindowsCalculator",
    "Microsoft.WindowsTerminal",
    "MicrosoftWindows.Client.WebExperience"
]

# -----------------------------
# SERVICE OPTIMIZATION
# -----------------------------

services_disable = [
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

services_manual = [
    "DoSvc",
    "DusmSvc",
    "SSDPSRV",
    "RemoteRegistry",
    "PhoneSvc"
]

def run_ps(command):
    subprocess.run(
        ["powershell", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# -----------------------------
# PREPARE MODE
# -----------------------------

def prepare():
    print("Starting User Machine Preparation...\n")

    # Remove installed apps
    for app in apps_to_remove:
        print(f"Removing installed: {app}")
        run_ps(
            f"Get-AppxPackage -AllUsers -Name {app} | "
            f"Remove-AppxPackage -ErrorAction SilentlyContinue"
        )

    # Remove provisioned apps
    for app in apps_to_remove:
        print(f"Removing provisioned: {app}")
        run_ps(
            f"Get-AppxProvisionedPackage -Online | "
            f"Where-Object {{$_.DisplayName -eq '{app}'}} | "
            f"Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue"
        )

    # Install Required Software
    download_folder = "C:\\temp_installers"
    os.makedirs(download_folder, exist_ok=True)

    def download_file(url, path):
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, path)

    # Chrome
    chrome_url = "https://dl.google.com/chrome/install/latest/chrome/install_google_chrome_enterprise.msi"
    chrome_path = os.path.join(download_folder, "chrome.msi")
    download_file(chrome_url, chrome_path)
    subprocess.run(["msiexec", "/i", chrome_path, "/qn"])

    # WhatsApp
    whatsapp_url = "https://web.whatsapp.com/desktop/windows/release/x64/WhatsAppSetup.exe"
    whatsapp_path = os.path.join(download_folder, "whatsapp.exe")
    download_file(whatsapp_url, whatsapp_path)
    subprocess.run([whatsapp_path, "/silent"])

    # WPS Office Free
    wps_url = "https://wdl1.pcfg.cache.wpscdn.com/wpsdl/wpsoffice/download/12.2.0.13110/WPSOffice_12.2.0.13110_x64.exe"
    wps_path = os.path.join(download_folder, "wps.exe")
    download_file(wps_url, wps_path)
    subprocess.run([wps_path, "/silent"])

    print("\nPreparation Completed.")
    print("Reboot recommended.\n")


# -----------------------------
# STOP MODE (SERVICE HARDENING)
# -----------------------------

def stop_services():
    print("Applying Business Safe Service Optimization...\n")

    for svc in services_disable:
        print(f"Disabling: {svc}")
        run_ps(
            f"Stop-Service {svc} -Force -ErrorAction SilentlyContinue; "
            f"Set-Service {svc} -StartupType Disabled"
        )

    for svc in services_manual:
        print(f"Setting Manual: {svc}")
        run_ps(
            f"Set-Service {svc} -StartupType Manual"
        )

    print("\nService Optimization Completed.")
    print("Reboot recommended.\n")


# -----------------------------
# MAIN ENTRY
# -----------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python debloat_users_machine.py prepare")
        print("  python debloat_users_machine.py stop")
        sys.exit()

    mode = sys.argv[1].lower()

    if mode == "prepare":
        prepare()
    elif mode == "stop":
        stop_services()
    else:
        print("Invalid option. Use 'prepare' or 'stop'.")