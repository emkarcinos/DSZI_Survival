import threading
import time


exitFlag = 0


class ThreadedSimulation(threading.Thread):
    def __init__(self, threadID, counter, player, map):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.counter = counter

        self.player = player

        self.result = None

        self.map = map

    def run(self):
        from src.AI.GA import doSimulation
        from src.game.Map import Map
        newMap = Map(self.map.filename, None)
        self.result = doSimulation(self.player, newMap)

    def getResult(self):
        return self.result
