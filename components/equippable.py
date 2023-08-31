#!/usr/bin/python3

from __future__ import annotations 

try: 
	from typing import TYPE_CHECKING
	from components.base_component import BaseComponent
	from equipment_types import EquipmentType
except: 
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")

if TYPE_CHECKING: 
	from entity import Item

class Equippable(BaseComponent):
	parent: Item

	def __init__(
		self,
		equipment_type: EquipmentType,
		power_bonus: int = 0,
		defense_bonus: int = 0,
	):
		self.equipment_type = equipment_type
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus

### Weapons 
class Dagger(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=200)

class Sword(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

### Armor
class Tunic(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=0)

class Gambeson(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2)

class ChainMail(Equippable):
	def __init__(self) -> None:
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=4)

class PlateMail(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=6)

class Brigandine(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=8)

class SteelPlate(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=10)

class LeatherArmor(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=0)

