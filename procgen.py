#!/usr/bin/python3

### Procedural generator for the tile map

from __future__ import annotations
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity

try:
	import random
	from colorama import Fore, Back, Style
	from game_map import GameMap
	import tile_types
	import tcod
	import copy
	import entity_factories
except:
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")

max_items_by_floor = [
	(1,1),
	(4,2),
]

max_monsters_by_floor = [
	(1,2),
	(4,3),
	(6,5),
	(8,7),
	(10,9),
	(12,11),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
	0: [(entity_factories.health_potion, 35), (entity_factories.leather_armor, 10),],
	2: [(entity_factories.confusion_scroll, 10), (entity_factories.gambeson, 2), (entity_factories.quarter_staff, 5)],
	4: [(entity_factories.lightning_scroll, 10), (entity_factories.sword, 5)], 
	6: [(entity_factories.fireball_scroll,10), (entity_factories.chain_mail, 2), (entity_factories.spear, 5)],
	8: [(entity_factories.plate_mail, 10), (entity_factories.bec_de_corbin, 5), (entity_factories.dane_axe, 5)],
	10: [(entity_factories.brigandine, 10), (entity_factories.greatsword, 5)],
	12: [(entity_factories.steel_plate, 10)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
	0: [(entity_factories.orc, 60)],
	3: [(entity_factories.troll, 10),(entity_factories.orc, 30)],
	5: [(entity_factories.troll, 30),(entity_factories.orc, 10)],
	7: [(entity_factories.troll, 50),(entity_factories.orc, 0)],
}

def get_max_value_for_floor(
weighted_chances_by_floor: List[Tuple[int, int]], floor: int
)-> int: 
	current_value = 0

	for floor_minimum, value in weighted_chances_by_floor:
		if floor_minimum > floor:
			break
		else: 
			current_value = value
	return current_value

def get_entities_at_random(
	weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
	number_of_entities: int,
	floor: int,
) -> List[Entity]:
	entity_weighted_changes = {}

	for key, values in weighted_chances_by_floor.items():
		if key > floor:
			break
		else:
			for value in values:
				entity = value[0]
				weighted_chance = value[1]

				entity_weighted_changes[entity] = weighted_chance
	entities = list(entity_weighted_changes.keys())
	entity_weighted_chance_values = list(entity_weighted_changes.values())

	choosen_entities = random.choices(
		entities, weights=entity_weighted_chance_values, k=number_of_entities
	)

	return choosen_entities

class RectangularRoom:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height

	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)		

		return center_x, center_y

	@property
	def inner(self) -> Tuple[slice, slice]:
		''' Return the inner area of this room as a 2D array index. '''
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

	def intersects(self, other: RectangularRoom) -> bool:
		"""Return True if this room overlaps with another room"""
		return (
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
			)

def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
	number_of_monsters = random.randint(
		0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
	)
	number_of_items = random.randint(
		0, get_max_value_for_floor(max_items_by_floor, floor_number)
	)

	monsters: List[Entity] = get_entities_at_random(
		enemy_chances, number_of_monsters, floor_number
	)
	items: List[Entity] = get_entities_at_random(
		item_chances, number_of_items, floor_number
	)

	for entity in monsters + items:
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)

		if not any(entity.x == x and entity.y == y for entity in dungeon.entities): 
			entity.spawn(dungeon, x, y)

def tunnel_between(
	start: Tuple[int, int], end: Tuple[int, int]
	)-> Iterator[Tuple[int, int]]:
	"""Return an L-shaped tunnel between these two points."""
	x1, y1 = start
	x2, y2 = end 
	if random.random() < 0.5: # 50% chance
		# Move horizontally, then vertically.
		corner_x, corner_y = x2, y1
	else: 
		# Move vertically, then horizontally.
		corner_x, corner_y = x1, y2

	# Generate the coordinates for this tunnel 
	for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
		yield x, y
	for x, y in tcod.los.bresenham((x2, y2), (corner_x, corner_y)).tolist():
		yield x, y

def generate_dungeon(
	max_rooms: int,
	room_min_size: int, 
	room_max_size: int, 
	map_width: int,
	map_height: int, 
	engine: Engine, ) -> GameMap:
	"""Generate a new dungeon map."""
	player = engine.player
	dungeon = GameMap(engine, map_width, map_height, entities=[player])

	rooms: List[RectangularRoom] = []
	center_of_last_room = (0, 0)

	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)

		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)

		# "RectangularRoom" class makes rectangles eaasier to work with
		new_room = RectangularRoom(x, y, room_width, room_height)

		# runs through the list of rooms to check for intersections
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue
		# if there are no intersections the room can be spwaned in

		# 'Dig out' the room's inner area
		dungeon.tiles[new_room.inner] = tile_types.floor

		if len(rooms) == 0:
			# The first room, where the player spawns
			player.place(*new_room.center, dungeon)
		else: # for all rooms after the 'Spawn Room'
			# 'Dig' tunnel from room to room
			for x , y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor

			center_of_last_room = new_room.center
		
		place_entities(new_room, dungeon, engine.game_world.current_floor)

		dungeon.tiles[center_of_last_room] = tile_types.down_stairs
		dungeon.downstairs_location = center_of_last_room

		# Finally, append the new room to the list of rooms
		rooms.append(new_room)

	return dungeon 





