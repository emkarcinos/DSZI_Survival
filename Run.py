from pathlib import Path

from src.game.Game import Game

# TODO: Paths are still retarded
programPath = Path(".").resolve()
game = Game(programPath)
