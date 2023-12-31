import psutil
import json
import time
from runningPIDs import pids
import showGame
import re
import traceback


class ProtonDiscordIntegration:
    def __init__(self):
        
        with open("knownGames.json", "r") as file:
            self.knownGames = json.load(file)
    def runCheck(self):
        processes = psutil.process_iter()
        for process in processes:
            if process.pid in pids: continue
            for game in self.knownGames:
                allow = False
                if "name" in game["requirement"] and re.fullmatch(game["requirement"]["name"], process.name()): allow = True
                elif "cmd" in game["requirement"] and re.fullmatch(game["requirement"]["cmd"], " ".join(process.cmdline())): allow = True
                if not allow: continue
                pids[process.pid] = showGame.startGame(game, process.create_time(), process)
        rm = []
        for pid in pids:
            if psutil.pid_exists(pid): continue
            pids[pid].close()
            rm.append(pid)
        for pid in rm:
            del pids[pid]


def main():
    listener = ProtonDiscordIntegration()
    print("Started ProtonDiscordIntegration")
    print("Listening for games...")
    while True:
        try:
            listener.runCheck()
        except Exception:
            print(traceback.format_exc())
        time.sleep(5)

if __name__ == "__main__":
    main()