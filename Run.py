from pathlib import Path
import sys
from src.game.Game import Game

# TODO: Paths are still retarded
programPath = Path(".").resolve()
game = Game(programPath, sys.argv)
