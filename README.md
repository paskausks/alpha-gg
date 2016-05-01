# AlphaGG
An interactive bot for Galactic Gaming's Discord server.

# Requirements
 * Python 3.5+
 * [Rapptz' discord.py](https://github.com/Rapptz/discord.py)
 * [requests](https://pypi.python.org/pypi/requests)

# Installation
Install dependencies:
```sh
pip install -r requirements.txt
```

Register an application at [https://discordapp.com/developers/applications/me/create](https://discordapp.com/developers/applications/me/create) and add an app bot user to it.

Go to `https://discordapp.com/oauth2/authorize?&client_id=<client_id>&scope=bot&permissions=0` where `<client_id>` is your Application's Client ID to have it join your server.

Edit the values in `config.example.py` and save it as `config.py`.
