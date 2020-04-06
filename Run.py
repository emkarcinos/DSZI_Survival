from pathlib import Path

from src.game.Game import Game

programPath = Path(".").resolve()
game = Game(programPath)
