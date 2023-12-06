import platform
from discordrp import Presence
import psutil


class startGame:
    def __init__(self, game: dict, time: int, process: psutil.Process):
        self.process = process
        self.game = game
        self.presence = Presence(game["clientID"])
        print("connected", game["name"])
        self.presence.set({
            "state": game["state"],
            "details": "running on "+platform.system(),
            "timestamps": {
                "start": int(time)
            },

            "assets": {
                "large_image": "logo"
            }
        })
        print("update", game["name"])
    def close(self):
        self.presence.close()
        print("closed", self.game["name"])