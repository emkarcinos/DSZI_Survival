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
        self.map.respawn()
        self.result = doSimulation(self.player, self.map)

    def getResult(self):
        return self.result
