import subprocess
import sys

# -----------------------------
# APPS TO REMOVE
# -----------------------------

apps = [
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
    "5319275A.WhatsAppDesktop",
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
# SERVICE OPTIMIZATION LIST
# -----------------------------

services_disable = [
    "SysMain",
    "WSearch",
    "DiagTrack",
    "MapsBroker",
    "XblAuthManager",
    "XblGameSave",
    "XboxNetApiSvc",
    "XboxGipSvc"
]

services_manual = [
    "DoSvc",
    "DusmSvc",
    "lfsvc",
    "SSDPSRV",
    "WerSvc"
]


def run_powershell(command):
    subprocess.run(
        ["powershell", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# -----------------------------
# CLEAN MODE
# -----------------------------

def clean_apps():
    print("Starting Windows 11 Debloat Process...\n")

    for app in apps:
        print(f"Removing installed package: {app}")
        run_powershell(
            f"Get-AppxPackage -AllUsers -Name {app} | "
            f"Remove-AppxPackage -ErrorAction SilentlyContinue"
        )

    for app in apps:
        print(f"Removing provisioned package: {app}")
        run_powershell(
            f"Get-AppxProvisionedPackage -Online | "
            f"Where-Object {{$_.DisplayName -eq '{app}'}} | "
            f"Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue"
        )

    print("\nApp Cleanup Completed.")
    print("Reboot recommended.\n")


# -----------------------------
# STOP MODE (SERVICE TUNING)
# -----------------------------

def optimize_services():
    print("Applying Safe Infra Performance Mode...\n")

    for service in services_disable:
        print(f"Disabling service: {service}")
        run_powershell(
            f"Stop-Service {service} -Force -ErrorAction SilentlyContinue; "
            f"Set-Service {service} -StartupType Disabled"
        )

    for service in services_manual:
        print(f"Setting Manual: {service}")
        run_powershell(
            f"Set-Service {service} -StartupType Manual"
        )

    print("\nService Optimization Completed.")
    print("Reboot recommended.\n")


# -----------------------------
# MAIN ENTRY
# -----------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python debloat_admin_machine.py clean")
        print("  python debloat_admin_machine.py stop")
        sys.exit()

    mode = sys.argv[1].lower()

    if mode == "clean":
        clean_apps()
    elif mode == "stop":
        optimize_services()
    else:
        print("Invalid option. Use 'clean' or 'stop'.")