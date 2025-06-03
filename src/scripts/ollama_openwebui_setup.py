import os
import subprocess
import socket
import shutil

def run_command(command, check=True):
    print(f"\n👉 Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result

def is_installed(command):
    return shutil.which(command) is not None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def install_docker():
    print("🐳 Docker not found. Installing Docker and Docker Compose...")
    run_command("apt update")
    run_command("apt install ca-certificates curl gnupg -y")
    run_command("install -m 0755 -d /etc/apt/keyrings")
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "
                "gpg --dearmor -o /etc/apt/keyrings/docker.gpg")
    run_command("chmod a+r /etc/apt/keyrings/docker.gpg")
    run_command('echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
                'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | '
                'tee /etc/apt/sources.list.d/docker.list > /dev/null')
    run_command("apt update")
    run_command("apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y")

def install_ollama():
    print("📦 Installing Ollama...")
    run_command("curl -fsSL https://ollama.com/install.sh | sh")

def setup_docker_compose_file():
    print("📁 Creating Docker Compose file for OpenWebUI...")
    compose_content = '''
version: '3'
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    ports:
      - 3000:3000
    volumes:
      - openwebui-data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    restart: unless-stopped

volumes:
  openwebui-data:
'''.strip()

    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

def main():
    if os.geteuid() != 0:
        print("❌ Please run this script as root (use sudo).")
        return

    print("🔧 System Update...")
    run_command("apt update && apt upgrade -y")

    if not is_installed("docker"):
        install_docker()
    else:
        print("✅ Docker is already installed.")

    if not is_installed("ollama"):
        install_ollama()
    else:
        print("✅ Ollama is already installed.")

    print("⬇️ Pulling Ollama model (llama2)...")
    run_command("ollama pull llama2")

    setup_docker_compose_file()

    print("🚀 Starting OpenWebUI with Docker Compose...")
    run_command("docker compose up -d")

    ip = get_local_ip()
    print(f"\n✅ SETUP COMPLETE! Access OpenWebUI at: http://{ip}:3000")

if __name__ == "__main__":
    main()
