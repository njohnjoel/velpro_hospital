import subprocess
import ctypes

USERS = {
    "Doctor": "1212",
    "Reception": "2323",
    "Pharmacy": "3434",
    "Radiology": "4545",
    "Nurse_Station": "5656",
    "Board_Room": "6767"
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_users():
    if not is_admin():
        print("Run as Administrator.")
        return

    print("Creating hospital users...\n")

    for username, password in USERS.items():

        subprocess.run(f'net user "{username}" /delete', shell=True)

        subprocess.run(f'net user "{username}" "{password}" /add', shell=True)
        subprocess.run(f'wmic useraccount where name="{username}" set PasswordExpires=FALSE', shell=True)
        subprocess.run(f'net user "{username}" /PasswordChg:No', shell=True)
        subprocess.run(f'net user "{username}" /active:yes', shell=True)

    print("\nAll users created successfully.\n")