#!/usr/bin/python3

### Tile map setup
try:
	from typing import Tuple
	import numpy as np
	from colorama import Fore, Back, Style

except:
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")

# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
	[
		("ch", np.int32), # Unicode codepoint
		("fg", "3B"),	# 3 unsigned bytes for RGB
		("bg", "3B"),
	]
)

# Tile struct used for statically defined tile data

tile_dt = np.dtype(
	[
		("walkable", np.bool),
		("transparent", np.bool),
		("dark", graphic_dt),
		("light", graphic_dt), 
	]
)

def new_tile(
	*, # Enforce the use of keywords, so that parameter order doesn't matter 
	walkable: int,
	transparent: int, #!/usr/bin/python3

	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
	) -> np.ndarray:
		"""Helper Function: define individual tile types"""
		return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# Shroud is for unexplored tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
	walkable=True, 
	transparent=True,
	dark=(ord(" "), (255, 255, 255), (80, 105, 112)), #(50, 50, 150)
	light=(ord(" "), (255, 255, 255), (120, 120, 90)), #(200, 180, 50)
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord(" "), (255, 255, 255), (70, 90, 110)), # (0, 0, 100)
	light=(ord(" "), (255, 255, 255), (100, 100, 60)), #(130, 110, 50)
)

down_stairs = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(">"), (0, 0, 100), (80, 105, 112)),
	light=(ord(">"), (255, 255, 255), (120, 120, 90)),
)