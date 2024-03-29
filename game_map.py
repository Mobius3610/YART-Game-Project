#!/usr/bin/python3

###  Map setup

from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING

try:
	import numpy as np 
	from tcod.console import Console
	#from procgen import generate_dungeon <- Importing here does not wk for whatever reason...

	from entity import Actor, Item
	import tile_types
	from colorama import Fore, Back, Style

except:
	print(Fore.RED + "ERROR: Could not import all necessary libraries (game_map).")

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity


class GameMap:
	def __init__(self, engine: Engine, width:int, height:int, entities: Iterable[Entity] = ()):
		self.engine = engine
		self.width, self.height = width, height
		self.entities = set(entities)
		self.tiles = np.full((width, height), fill_value= tile_types.wall, order="F")

		self.visible = np.full((width, height), fill_value=False, order="F") # Tiles in LOS 
		self.explored = np.full((width, height), fill_value=False, order="F") # Tiles 'in the player character's memory'

		self.downstairs_location = (0, 0)
		# self.tiles[30:33, 22] = tile_types.wall #hard coded wall

	@property
	def gamemap(self) -> GameMap:
		return self

	@property	
	def actors(self) -> Iterator[Actor]:
		# Iterate over this maps living actors.
		yield from (
			entity
			for entity in self.entities
			if isinstance(entity, Actor) and entity.is_alive
		)


	@property
	def items(self) -> Iterator[Item]:
		yield from (entity for entity in self.entities if isinstance(entity, Item))

	def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
		for entity in self.entities:
			if (
				entity.blocks_movement
				and entity.x == location_x
				and entity.y == location_y
			):
				return entity
		
		return None

	def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
		for actor in self.actors:
			if actor.x == x and actor.y == y:
				return actor
		return None


	def in_bounds(self, x:int, y:int) -> bool:
		# if char is in bounds rtn True
		return 0 <= x < self.width and 0 <= y < self.height

	def render(self, console: Console) -> None:
		console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD,
		)

		entities_sorted_for_rendering = sorted(
			self.entities, key=lambda x: x.render_order.value
			)

		for entity in entities_sorted_for_rendering:
			# only print out entities that are in FOV
			if self.visible[entity.x, entity.y]:
				console.print(entity.x, entity.y, entity.char, fg=entity.color)



class GameWorld: 
	# Holds settings for the GameMap and generates new maps when the player moves down the stairs

	def __init__(
		self,
		*, 
		engine: Engine,
		map_width: int,
		map_height: int,
		max_rooms: int, 
		room_min_size: int,
		room_max_size: int,
		current_floor: int = 0, 
	):
		self.engine = engine
		self.map_width = map_width
		self.map_height = map_height
		self.max_rooms = max_rooms
		self.room_min_size = room_min_size
		self.room_max_size = room_max_size
		self.current_floor = current_floor

	def generate_floor(self) -> None: 
		from procgen import generate_dungeon # <- importing here is nessecary???
		self.current_floor += 1

		self.engine.game_map = generate_dungeon(
			max_rooms=self.max_rooms,
			room_min_size=self.room_min_size,
			room_max_size=self.room_max_size,
			map_width=self.map_width,
			map_height=self.map_height,
			engine=self.engine,
		)


