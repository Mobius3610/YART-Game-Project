#!/usr/bin/python3

### Yet Another Roguelike Tutorial - Written in Python 3 and TCOD ###

"""
Author: Aaron C.
Start Date: 07/23/2022
Encoding: UTF-8
python 3.8.10

Description: I am following the Python3 r/roguelikedev tutorial to get familiar with the engine 

"""

try: 
	import tcod
	from engine import Engine
	import entity_factories
	from procgen import generate_dungeon
	import copy
	import traceback
	import sys
	import random
	import color

	import colorama
	from colorama import Fore, Back, Style
except:	
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")



def main() -> None:
	print("Elbereth")
	screen_width = 80
	screen_hight = 50

	map_width = 80
	map_height = 43

	room_max_size = 10
	room_min_size = 6
	max_rooms = 30

	max_monsters_per_room = 2
	max_items_per_room = 2

	tileset = tcod.tileset.load_tilesheet("yartTiles.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
	
	player = copy.deepcopy(entity_factories.player)

	engine = Engine(player = player)

	engine.game_map = generate_dungeon(
		max_rooms=max_rooms,
		room_min_size=room_min_size,
		room_max_size=room_max_size,
		map_width=map_width,
		map_height=map_height,
		max_monsters_per_room=max_monsters_per_room,
		max_items_per_room=max_items_per_room,
		engine=engine, 
		)

	engine.update_fov()

	engine.message_log.add_message("Hello and welcome, Adventurer, to yet another dungeon!", color.welcome_text)

	with tcod.context.new_terminal(
		screen_width,
		screen_hight,
		tileset = tileset,
		title = "My Cruddy Rougelike",
		vsync = True,
		) as context:
			root_console = tcod.Console(screen_width, screen_hight, order="F")
			while True: 
				root_console.clear()
				engine.event_handler.on_render(console=root_console)
				context.present(root_console)

				try: 
					for event in tcod.event.wait():
						context.convert_event(event)
						engine.event_handler.handle_events(event)
				except Exception: # Handle exceptions in game
					traceback.print_exc() # print error to stderr
					# Then print the error to the message log.
					engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
	main()