# Configs imports from here

import os


if os.path.exists("config.py"):
    from config import Development as Config
else:
    from .d3vil_config import Config

#d3vilbot
