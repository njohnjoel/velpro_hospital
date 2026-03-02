import subprocess
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_ps(command):
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command]
    )

def winget_available():
    result = subprocess.run(["where", "winget"], capture_output=True)
    return result.returncode == 0


def install_software():
    if not is_admin():
        print("Run as Administrator.")
        return

    if not winget_available():
        print("Winget not found. Install App Installer first.")
        return

    print("Installing Google Chrome (Machine Scope)...")
    subprocess.run([
        "winget", "install",
        "--id", "Google.Chrome",
        "-e",
        "--scope", "machine",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--silent"
    ])

    print("Installing WPS Office (Machine Scope)...")
    subprocess.run([
        "winget", "install",
        "--id", "Kingsoft.WPSOffice",
        "-e",
        "--scope", "machine",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--silent"
    ])

    print("Installing WhatsApp (Machine Scope)...")
    subprocess.run([
        "winget", "install",
        "--id", "WhatsApp.WhatsApp",
        "-e",
        "--scope", "machine",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--silent"
    ])

    print("Software installation completed.\n")

COMMON_APPS = [
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
    "MSTeams"
]


def remove_apps():
    for app in COMMON_APPS:
        run_ps(f"Get-AppxPackage -AllUsers -Name {app} | Remove-AppxPackage -ErrorAction SilentlyContinue")
        run_ps(
            f"Get-AppxProvisionedPackage -Online | "
            f"Where-Object {{$_.DisplayName -eq '{app}'}} | "
            f"Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue"
        )

def disable_consumer_features():
    run_ps(r'''
    New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\CloudContent" -Force | Out-Null
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\CloudContent" `
        -Name "DisableWindowsConsumerFeatures" -Value 1 -Type DWord
    ''')

SERVICES_DISABLE = [
    "DiagTrack",
    "dmwappushservice",
    "MapsBroker",
    "XblAuthManager",
    "XblGameSave",
    "XboxNetApiSvc",
    "XboxGipSvc",
    "RetailDemo",
    "WSearch",
    "SysMain"
]

SERVICES_MANUAL = [
    "DoSvc",
    "DusmSvc",
    "SSDPSRV",
    "RemoteRegistry"
]


def optimize_services():
    for svc in SERVICES_DISABLE:
        run_ps(f"Stop-Service {svc} -Force -ErrorAction SilentlyContinue")
        run_ps(f"Set-Service {svc} -StartupType Disabled")

    for svc in SERVICES_MANUAL:
        run_ps(f"Set-Service {svc} -StartupType Manual")

def prepare_admin():
    if not is_admin():
        print("Run as Administrator.")
        return

    print("Preparing ADMIN machine...\n")

    remove_apps()
    disable_consumer_features()
    optimize_services()
    install_software()

    print("\nAdmin Prepare Completed. Reboot Recommended.\n")


def prepare_users():
    if not is_admin():
        print("Run as Administrator.")
        return

    print("Preparing USER machine...\n")

    remove_apps()
    disable_consumer_features()
    optimize_services()
    install_software()

    print("\nUser Prepare Completed. Reboot Recommended.\n")