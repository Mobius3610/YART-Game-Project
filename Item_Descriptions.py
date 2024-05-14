#!/usr/bin/python3

from __future__ import annotations

try:
	from typing import Optional, TYPE_CHECKING

	import actions
	import color
	import components.inventory
	from components.base_component import BaseComponent
	from exceptions import Impossible

	from colorama import Fore, Back, Style

except:	
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")

if TYPE_CHECKING:
	from entity import Actor, Item

class description(): # -> if I can impliment a dictionary I should. 
	def wallmeat(self) -> None: 
		self.wallmeat = "A mysterious meat that resembles pork and is seemingly perfectly preserved." 
	
	# def garlic = "asdf"
	# def healthPotion = "asdf"