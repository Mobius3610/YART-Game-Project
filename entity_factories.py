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

from Item_Descriptions import description

# player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

# orc = Entity(char="o", color=(63, 127, 63), name="Orc", blocks_movement=True)
# troll = Entity(char="T", color=(0, 127, 0), name="Troll", blocks_movement=True)

player = Actor(
	char="@",
	color=(0, 0, 0),
	name="Player",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=30, base_defense=0, base_power=5),
	inventory=Inventory(capacity=26),
	level=Level(level_up_base=200),
)

corpse = Actor(
	char="C",
	color=(85, 255, 125), #(63, 127, 63)
	name="Rotting Corpse",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=5, base_defense=0, base_power=2),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=15),
)

skeleton = Actor(
	char="S",
	color=(0, 127, 0),
	name="Skeleton",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=10, base_defense=1, base_power=3),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=20),
)

ghoul = Actor(
	char="U",
	color=(0, 127, 0),
	name="Unfortunate experiment", # might want to find a better name.
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=20, base_defense=5, base_power=4),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=45),
)

enchanted_armor = Actor(
	char="E",
	color=(0, 127, 0),
	name="Enchanted Armor",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=5, base_defense=10, base_power=3),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=80),
)

cultist = Actor(
	char="C",
	color=(200, 16, 16),
	name="Cultist",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=10, base_defense=8, base_power=10),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=10),
)

lesser_vampire = Actor(
	char="L",
	color=(256, 24, 24),
	name="Vampire bloodling",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=50, base_defense=10, base_power=10),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=10),
)

chimera = Actor(
	char="K",
	color=(0, 127, 0),
	name="Chimera",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=25, base_defense=15, base_power=10),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=10),
)

automaton = Actor(
	char="A",
	color=(0, 127, 0),
	name="Automaton", # -> could change name to Golem
	ai_cls=HostileEnemy,
	equipment=Equipment(),
	fighter=Fighter(hp=1, base_defense=10, base_power=10),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=10),
)



### Consumable Items: Healing and Damage
wallmeat = Item(
	char="p",
	color=(127, 0, 225),
	name="Pork Chop",
	consumable=consumable.HealingConsumable(amount=5),
	description="A mysterious meat that resembles pork and is seemingly perfectly preserved."
	#description=Item_Descriptions.wallmeat, # -> putting all the item descriptions in another file to call upon for easy of management
)

health_potion = Item(
	char="h",
	color=(127, 0, 225),
	name="Health Potion",
	consumable=consumable.HealingConsumable(amount=40),
)

blood_vial = Item(
	char="b",
	color=(127, 0, 225),
	name="Blood Vial",
	consumable=consumable.HealingConsumable(amount=10),
)


garlic = Item(
	char="g",
	color=(200, 100, 255),
	name="Garlic Bomb",
	consumable=consumable.ConfusionConsumable(number_of_turns=5,),
)

protection_from_evil = Item(
	char="&",
	color=(200, 100, 255),
	name="Chain Censer",
	consumable=consumable.ConfusionConsumable(number_of_turns=5),
)

oak_stake = Item(
	char="v", 
	color=(255, 255, 0),
	name="Oak Stake",
	consumable=consumable.LightningDamageConsumable(damage=5, maximum_range=5),
	# consumable=consumable.DirectDamageConsumable(damage=10, maximum_range=5),
)

throwing_axe = Item(
	char="p", 
	color=(255, 255, 0),
	name="Throwing Axe",
	consumable=consumable.LightningDamageConsumable(damage=10, maximum_range=5),
	# consumable=consumable.DirectDamageConsumable(damage=10, maximum_range=5),
)

combat_cross = Item(
	char="+", 
	color=(255, 255, 0),
	name="Combat Cross",
	consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
	# consumable=consumable.DirectDamageConsumable(damage=10, maximum_range=5),
)

holy = Item(
	char="0", 
	color=(255, 0, 0), 
	name="Orb of Antioch",
	consumable=consumable.FireballDamageConsumable(damage=100, radius=5), 
	# consumable=consumable.AreaDamageConsumable(damage=12, radius=3), 
)

# confusion_scroll = Item(
# 	char="~",
# 	color=(200, 100, 255),
# 	name="Confusion Scroll",
# 	consumable=consumable.ConfusionConsumable(number_of_turns=10),
# )

# lightning_scroll = Item(
# 	char="~", 
# 	color=(255, 255, 0),
# 	name="Lightning Scroll",
# 	consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
# )

# fireball_scroll = Item(
# 	char="~", 
# 	color=(255, 0, 0), 
# 	name="Fireball Scroll", 
# 	consumable=consumable.FireballDamageConsumable(damage=12, radius=3), 
# )


### Weapons
dagger = Item(
	char="-",
	color=(0, 191, 255),
	name="Dagger",
	equippable=equippable.Dagger(),
)

leather_whip = Item(
	char="s",
	color=(200, 100, 20),
	name="Leather Whip",
	equippable=equippable.LeatherWhip(),
)

arming_sword = Item(
	char="/",
	color=(0, 191, 255),
	name="Arming Sword",
	equippable=equippable.ArmingSword(),
)

spear = Item(
	char="|",
	color=(0, 191, 255),
	name="Spear",
	equippable=equippable.Spear(),
)

poleaxe = Item(
	char="P",
	color=(0, 191, 255),
	name="Poleaxe",
	equippable=equippable.Poleaxe(),
)

battle_axe = Item(
	char="P",
	color=(0, 191, 255),
	name="Battle Axe",
	equippable=equippable.BattleAxe(),
)

claymore = Item(
	char="\\",
	color=(0, 191, 255),
	name="Claymore",
	equippable=equippable.Claymore(),
)

### Unique Weapons
vampire_killer = Item(
	char="s",
	color=(128, 200, 255),
	name="Vampire Killer",
	equippable=equippable.VampireKiller(),
)

excalibur = Item(
	char="/",
	color=(128, 200, 255),
	name="Excalibur",
	equippable=equippable.Excalibur(),
)

mjolnir = Item(
	char="j",
	color=(0, 191, 255),
	name="Mjolnir",
	equippable=equippable.Mjolnir(),
)

reaper = Item(
	char="?",
	color=(0, 191, 255),
	name="Death Scyth",
	equippable=equippable.Reaper(),
)

### Armor
tunic = Item(
	char="[",
	color=(190, 170, 169),
	name="Tunic",
	equippable=equippable.Tunic(),
)

gambeson = Item(
	char="[",
	color=(180, 170, 130),
	name="Gambeson",
	equippable=equippable.Gambeson(),
)

plate = Item(
	char="[", 
	color=(200, 255, 230),
	name="Plate",
	equippable=equippable.Plate(),
)

brigandine = Item(
	char="[",
	color=(139, 16, 69),
	name="Brigandine",
	equippable=equippable.Brigandine(),
)

leather_armor = Item(
	char="[", 
	color=(200, 100, 20),
	name="Leather Armor",
	equippable=equippable.LeatherArmor(),
)

### Unique Armor 

hunter_garb = Item(
	char="{",
	color=(128, 200, 255),
	name="Vampire Hunter's Armor",
	equippable=equippable.HunterGarb(),
)
