import json
import os
import shutil
import pandas as pd
from loguru import logger

class EpicLibrary:
    def __init__(self):
        # check for paths
        self.path = self.heroic_install()

    def heroic_install(self):  # untested
        # Check for flatpak heroic
        flatpak_path = os.path.expanduser(
            "~/.var/app/com.heroicgameslauncher.hgl/config/heroic/"
        )
        if shutil.which("heroic") == "/usr/bin/heroic":
            return os.path.expanduser("~/.config/heroic/")
        elif os.path.isdir(flatpak_path):
            return flatpak_path
        # windows
        elif os.path.exists(
            "C:\\Program Files\\Epic Games\\Epic Games Launcher\\EpicGamesLauncher.exe"
        ):
            return "C:\\Program Files\\Epic Games\\Epic Games Launcher\\EpicGamesLauncher.exe"
        else:
            raise FileNotFoundError("Heroic Launcher path not found")

    def epic_library(self):
        # store_cache/legendary_library.json
        return os.path.join(self.path, "store_cache/legendary_library.json")

    def fetch_games(self):
        with open(self.epic_library(), "r") as f:
            return json.load(f)['library']




# debugging
if __name__ == "__main__":
    epic = EpicLibrary()
    games = (epic.fetch_games())
    # js = json.dumps(games, indent=4)
    df = pd.DataFrame(games)
    print(df.columns)
    df['title'].to_csv("games.csv", index=False)

