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
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)

class Sword(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class Spear(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class BecDeCorbin(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=5)

class DaneAxe(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=5)

class QuarterStaff(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=3)

class Greatsword(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=6)

'''
# Ranged Weapondry

class Sling(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=1)

class Crossbow(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class Bow(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=5)

class Atlatl(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=6)

'''

# Legedary Melee Weapondry
class Sting(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=10)

class Excalibur(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20)

class Moonlight(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=30)

class RuYi(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=15)

class Mjolnir(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20)

class Reaper(Equippable): 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=100)

'''
# Legedary Ranged Weapondry 
class BowofLegedaryStatus(Equippable): #Look for named mythical Bow#
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=15)

class Musket(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=20)

class Blunderbus(Equippable):
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=30)

class GiantSlayer(Equippable): #Sling weapon# 
	def __init__(self) -> None: 
		super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=10)  

'''


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

