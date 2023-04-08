#!/usr/bin/python3

from __future__ import annotations

try: 
	from typing import List, TYPE_CHECKING
	from components.base_component import BaseComponent
	
	import colorama
	from colorama import Fore, Back, Style
except:	
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")	

if TYPE_CHECKING: 
	from entity import Actor, Item

class Inventory(BaseComponent): 
	parent: Actor

	def __init__(self, capacity: int):
		self.capacity = capacity
		self.items: List[Item] = []

	def drop(self, item: Item) -> None:
		# Removes item from the inventory and places it on the game map at the location of the player
		self.items.remove(item)
		item.place(self.parent.x, self.parent.y, self.gamemap)

		self.engine.message_log.add_message(f"You dropped a {item.name} on the ground.")