# To run this bot, the packages are set and ready to install.
import os
import platform

if platform.system() == "Windows":  # If you are using a Windows Operating System
    # Upgrades the pip package for fluent installation
    os.system("python.exe -m pip install -U pip")
elif platform.system() == "Linux":  # If you are using a Linux Operating System
    # Upgrades the pip package for fluent installation #You need Python3.9 and over with an activated venv
    os.system("python3 -m pip install -U pip")
# Required packages for the bot to use. Also upgrades it if a new release is found
os.system(
    "pip install -U discord.py aiohttp websockets requests asyncio python-dotenv humanfriendly datetime Pillow py-expression-eval topggpy lxml reactionmenu jishaku pandas openpyxl"
)
