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
		hit_bonus: int = 0, 
		evasion_bonus: int = 0,
	):
		self.equipment_type = equipment_type
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.hit_bonus = hit_bonus
		self.evasion_bonus = evasion_bonus

### Weapons 
class LeatherWhip(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=1, hit_bonus=1)

class Dagger(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2, hit_bonus=1)

class ArmingSword(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4, hit_bonus=3)

class Spear(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4, hit_bonus=3)

class Poleaxe(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=5, hit_bonus=4)

class BattleAxe(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=5, hit_bonus=3)

class Claymore(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=6, hit_bonus=5)

'''
# Ranged Weapondry
class Sling(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=1, range=5)

class Crossbow(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4, range=8)

class Flintlock(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20, range=20)

class Blunderbuss dmg=30, range=5

'''

# Legedary Melee Weapondry
class VampireKiller(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20, hit_bonus=10)

class Excalibur(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20, hit_bonus=10)

class Mjolnir(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=25, hit_bonus=10, evasion_bonus=-5) #might need to debug...

class Reaper(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20, hit_bonus=10)

class BeastHunter(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=15, hit_bonus=5, evasion_bonus=5)


### Armor
class Tunic(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, evasion_bonus=1)

class Gambeson(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=4, evasion_bonus=1)

class Brigandine(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=8, evasion_bonus=3)

class Plate(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=10, evasion_bonus=6)

class LeatherArmor(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, evasion_bonus=3)

### Unique Armor
class HunterGarb(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=8, evasion_bonus=9)
class MythrilPlate(Equippable):
	def __init__(self) -> None:
		super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=15, evasion_bonus=5)
		
