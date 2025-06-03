import subprocess

#!/usr/bin/env python3


def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        exit(1)

def main():
    # Update, upgrade, and autoremove
    run_command("sudo apt update")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")

    # Install OpenJDK 11

    # Create /proj/tools/jenkins and /proj/tools/docker directories
    run_command("sudo mkdir -p /proj/tools/jenkins")
    run_command("sudo mkdir -p /proj/tools/docker")
    run_command("sudo chown $USER:$USER /proj/tools/jenkins")
    run_command("sudo chown $USER:$USER /proj/tools/docker")
    run_command("sudo apt install -y openjdk-11-jdk")

    # Install Jenkins
    run_command("wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -")
    run_command('sudo sh -c \'echo "deb https://pkg.jenkins.io/debian-stable binary/" > /etc/apt/sources.list.d/jenkins.list\'')
    run_command("sudo apt update")
    run_command("sudo apt install -y jenkins")

    # Install Docker
    run_command("sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release")
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
    run_command('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    run_command("sudo apt update")
    run_command("sudo apt install -y docker-ce docker-ce-cli containerd.io")

    # Install git, curl, wget, net-tools
    run_command("sudo apt install -y git curl wget net-tools")

if __name__ == "__main__":
    main()