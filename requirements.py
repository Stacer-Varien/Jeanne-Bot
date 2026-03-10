# To run this bot, the packages are set and ready to install.
import platform
import subprocess

if platform.system() == "Windows":  # If you are using a Windows Operating System
    # Upgrades the pip package for fluent installation
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], check=True)
elif platform.system() == "Linux":  # If you are using a Linux Operating System
    # Upgrades the pip package for fluent installation #You need Python3.9 and over with an activated venv
    subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)
# Required packages for the bot to use. Also upgrades it if a new release is found
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
