#!/usr/bin/python3

### The Engine for the game. Going to handle player events here. 

from __future__ import annotations

try:
	from typing import TYPE_CHECKING

	from tcod.context import Context
	from tcod.console import Console
	from tcod.map import compute_fov
	from message_log import MessageLog
	from render_functions import render_bar, render_names_at_mouse_location
	import exceptions
	import lzma
	import pickle

	from colorama import Fore, Back, Style

except:	
	print(Fore.RED + "ERROR: Could not import all necessary libraries (engine).")

if TYPE_CHECKING:
	from entity import Actor
	from game_map import GameMap, GameWorld

class Engine:
	game_map: GameMap
	game_world: GameWorld
	
	def __init__(self, player: Actor):
		self.message_log = MessageLog()
		self.mouse_location = (0,0)
		self.player = player

	def handle_enemy_turns(self) -> None:
		for entity in set(self.game_map.actors) - {self.player}:
			if entity.ai:
				try: 
					entity.ai.perform()
				except exceptions.Impossible:
					pass # Ignore impossible action exceptions from AI. 

	def update_fov(self) -> None:
		self.game_map.visible[:] = compute_fov(
			self.game_map.tiles["transparent"],
			(self.player.x, self.player.y),
			radius=8,
			)
		# if a tile is "visible" it should be added to the list of "explored" tiles. 
		self.game_map.explored |= self.game_map.visible


	def render(self, console: Console) -> None:
		self.game_map.render(console)

		self.message_log.render(console=console, x=21, y=45, width=40, height=5)

		render_bar(
			console=console,
			current_value=self.player.fighter.hp,
			maximum_value=self.player.fighter.max_hp,
			total_width=20,
		)

		render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

		# for entity in self.entities:
		# 	# only print out entities that are in FOV
		# 	if self.game_map.visible[entity.x, entity.y]:
		# 		console.print(entity.x, entity.y, entity.char, fg=entity.color)

	def save_as(self, filename: str) -> None: 
		# save this Engine instance as a compressed file. 
		save_data = lzma.compress(pickle.dumps(self))
		with open(filename, "wb") as f: 
			f.write(save_data)

