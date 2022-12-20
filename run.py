import os
from pathlib import Path
import sys

import uncooperative


resource_path = Path(__file__).parents[0] / 'res'
game = uncooperative.get_game((1280,720), resource_path)
game.run(uncooperative.AttractMode())
