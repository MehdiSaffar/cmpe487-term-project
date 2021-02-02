from pathlib import Path
import os

WIDTH = 350
HEIGHT = 300
FPS = 60

UDP_PORT = 5000
TCP_PORT = 5000

root_path = Path(os.path.dirname(__file__)).parent


class Color:
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    DARK_GRAY = (50, 50, 50)
