import subprocess

# ----------------------------------
# CONFIGURATION
# ----------------------------------

users = {
    "Doctor": "1234",
    "Reception": "2345",
    "Pharmacy": "3456",
    "Radiology": "4567",
    "Nurse_Station": "5678",
    "Board_Room": "6789"
}

# ----------------------------------
# FUNCTION TO RUN COMMAND
# ----------------------------------

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[SUCCESS] {command}")
    else:
        print(f"[ERROR] {command}")
        print(result.stderr)

# ----------------------------------
# CREATE USERS
# ----------------------------------

for username, password in users.items():

    print(f"\nCreating user: {username}")

    # Create user
    run_command(f'net user "{username}" "{password}" /add')

    # Set password never expires
    run_command(f'wmic useraccount where name="{username}" set PasswordExpires=FALSE')

    # Prevent user from changing password
    run_command(f'net user "{username}" /PasswordChg:No')

    # Ensure account is active
    run_command(f'net user "{username}" /active:yes')

print("\nAll users processed successfully.")