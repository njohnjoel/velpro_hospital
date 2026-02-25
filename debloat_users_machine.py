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

def run_ps(command):
    subprocess.run(
        ["powershell", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

print("Starting User Machine Cleanup...\n")

# -----------------------------
# REMOVE INSTALLED APPS
# -----------------------------

for app in apps_to_remove:
    print(f"Removing installed: {app}")
    run_ps(f"Get-AppxPackage -AllUsers -Name {app} | Remove-AppxPackage -ErrorAction SilentlyContinue")

# -----------------------------
# REMOVE PROVISIONED APPS
# -----------------------------

for app in apps_to_remove:
    print(f"Removing provisioned: {app}")
    run_ps(
        f"Get-AppxProvisionedPackage -Online | "
        f"Where-Object {{$_.DisplayName -eq '{app}'}} | "
        f"Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue"
    )

# -----------------------------
# INSTALL REQUIRED SOFTWARE
# -----------------------------

download_folder = "C:\\temp_installers"
os.makedirs(download_folder, exist_ok=True)

def download_file(url, path):
    print(f"Downloading {url}")
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

print("\nUser Machine Setup Completed.")
print("Reboot recommended.")