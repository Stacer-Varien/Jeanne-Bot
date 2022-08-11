#To run this bot, the packages are set and ready to install. Only TopGG is the only package that has the '--no-deps' argument added because discord.py and nextcord will not mix well and you will be expecting some errors

from os import system as console
from platform import system

if system() == "Windows":  # If you are using a Windows Operating System
    # Upgrades the pip package for fluent installation
    upgrade_pip = "python -m pip install --upgrade pip"

elif system() == "Linux":  # If you are using a Linux Operating System
    # Upgrades the pip package for fluent installation #You need Python3.10 with an activated venv
    upgrade_pip = "python3 -m pip install --upgrade pip"

# Required packages for the bot to use. Also upgrades it if a new release is found
essentials = "pip install --upgrade nextcord requests function-cooldowns python-dotenv humanfriendly datetime pillow py-expression-eval"

# TopGG package with the '--no-deps' argument so discord.py doesn't get installed
topgg = "pip install topggpy --no-deps"

packages = [upgrade_pip, essentials, topgg]

for a in packages:
    console(a)
