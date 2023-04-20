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
	import exceptions
	import input_handlers
	import setup_game
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

	tileset = tcod.tileset.load_tilesheet("yartTiles.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
	
	handler: input_handlers.BaseEventHandler = setup_game.MainMenu()	

	with tcod.context.new_terminal(
		screen_width,
		screen_hight,
		tileset = tileset,
		title = "My Cruddy Rougelike",
		vsync = True,
		) as context:
			root_console = tcod.Console(screen_width, screen_hight, order="F")
			try: 
				while True:
					root_console.clear()
					handler.on_render(console=root_console)
					context.present(root_console)

					try:
						for event in tcod.event.wait():
							context.convert_event(event)
							handler = handler.handle_events(event)
					except Exception: # handle expectations in game
						traceback.print_exc() # print error to stderr
						# Then print the error in the message log
						if isinstance(handler, input_handlers.EventHandler):
							handler.engine.message_log.add_message(traceback.format_exc(), color.error)
			except exceptions.QuitWithoutSaving: 
				raise
			except SystemExit: # save and quit
				raise
			except BaseException: 
				raise


if __name__ == "__main__":
	main()