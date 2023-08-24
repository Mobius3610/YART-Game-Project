#!/usr/bin/python3

## defines the entities

from components.ai import HostileEnemy
from components.fighter import Fighter
from components import consumable, equippable
from components.equipment import Equipment
from entity import Actor, Item
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

# player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

# orc = Entity(char="o", color=(63, 127, 63), name="Orc", blocks_movement=True)
# troll = Entity(char="T", color=(0, 127, 0), name="Troll", blocks_movement=True)

player = Actor(
	char="@",
	color=(255, 255, 255),
	name="Player",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=30, base_defense=2, base_power=5),
	inventory=Inventory(capacity=26),
	level=Level(level_up_base=200),
)

orc = Actor(
	char="@",
	color=(63, 127, 63),
	name="Orc",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=10, base_defense=0, base_power=3),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=35),
)

troll = Actor(
	char="T",
	color=(0, 127, 0),
	name="Troll",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=16, base_defense=1, base_power=4),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=100),
)

## Items that spawn on the gound of the dungeon

confusion_scroll = Item(
	char="~",
	color=(207, 63, 255),
	name="Confusion Scroll",
	consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

health_potion = Item(
	char="!",
	color=(127, 0, 225),
	name="Health Potion",
	consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
	char="~", 
	color=(255, 255, 0),
	name="Lightning Scroll",
	consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

fireball_scroll = Item(
	char="~", 
	color=(255, 0, 0), 
	name="Fireball Scroll", 
	consumable=consumable.FireballDamageConsumable(damage=12, radius=3), 
)


### Weapons
dagger = Item(
	char="/",
	color=(0, 191, 255),
	name="Dagger",
	equippable=equippable.Dagger(),
)

sword = Item(
	char="/",
	color=(0, 191, 255),
	name="Sword",
	equippable=equippable.Sword(),
)

### Armor
tunic = Item(
	char="[",
	color=(190, 170, 169),
	name="Tunic",
	equippable=equippable.Sword(),
)

gambeson = Item(
	char="[",
	color=(180, 170, 130),
	name="Gambeson",
	equippable=equippable.Gambeson(),
)

chain_mail = Item(
	char="[",
	color=(200, 245, 240),
	name="Chain Mail",
	equippable=equippable.ChainMail(),
)

plate_mail = Item(
	char="[", 
	color=(200, 255, 230),
	name="Plate Mail",
	equippable=equippable.PlateMail(),
)

brigandine = Item(
	char="[",
	color=(139, 16, 69),
	name="Brigandine",
	equippable=equippable.Brigandine(),
)

steel_plate = Item(
	char="[", 
	color=(200, 255, 230),
	name="Steel Plate",
	equippable=equippable.SteelPlate(),
)

leather_armor = Item(
	char="[", 
	color=(130, 100, 120),
	name="Leather Armor",
	equippable=equippable.LeatherArmor(),
)

