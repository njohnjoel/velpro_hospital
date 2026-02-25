import subprocess
import sys

# List of removable apps
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

def run_powershell(command):
    try:
        subprocess.run(
            ["powershell", "-Command", command],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        print(f"Error: {e}")

print("Starting Windows 11 Debloat Process...\n")

for app in apps:
    print(f"Removing installed package: {app}")
    cmd_remove = f"Get-AppxPackage -AllUsers -Name {app} | Remove-AppxPackage -ErrorAction SilentlyContinue"
    run_powershell(cmd_remove)

for app in apps:
    print(f"Removing provisioned package: {app}")
    cmd_provisioned = (
        f"Get-AppxProvisionedPackage -Online | "
        f"Where-Object {{$_.DisplayName -eq '{app}'}} | "
        f"Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue"
    )
    run_powershell(cmd_provisioned)

print("\nCleanup Completed.")
print("Please reboot your system.")