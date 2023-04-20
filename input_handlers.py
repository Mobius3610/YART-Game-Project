#!/usr/bin/python3

### Player input handler class for Yet Another Roguelike Tutorial

from __future__ import annotations

try: 
	from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union
	import tcod.event
	import actions
	from actions import Action, BumpAction, WaitAction, PickupAction
	import color
	import exceptions

	import colorama
	from colorama import Fore, Back, Style
except:	
	print(Fore.RED + "ERROR: Could not import all necessary libraries.")

if TYPE_CHECKING:
	from engine import Engine
	from entity import Item

MOVE_KEYS = {
   # Arrow keys.
   tcod.event.K_UP: (0, -1),
   tcod.event.K_DOWN: (0, 1),
   tcod.event.K_LEFT: (-1, 0),
   tcod.event.K_RIGHT: (1, 0),
   tcod.event.K_HOME: (-1, -1),
   tcod.event.K_END: (-1, 1),
   tcod.event.K_PAGEUP: (1, -1),
   tcod.event.K_PAGEDOWN: (1, 1),
   # Numpad keys.
   tcod.event.K_KP_1: (-1, 1),
   tcod.event.K_KP_2: (0, 1),
   tcod.event.K_KP_3: (1, 1),
   tcod.event.K_KP_4: (-1, 0),
   tcod.event.K_KP_6: (1, 0),
   tcod.event.K_KP_7: (-1, -1),
   tcod.event.K_KP_8: (0, -1),
   tcod.event.K_KP_9: (1, -1),
   # Vi keys.
   tcod.event.K_h: (-1, 0),
   tcod.event.K_j: (0, 1),
   tcod.event.K_k: (0, -1),
   tcod.event.K_l: (1, 0),
   tcod.event.K_y: (-1, -1),
   tcod.event.K_u: (1, -1),
   tcod.event.K_b: (-1, 1),
   tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
   tcod.event.K_PERIOD,
   tcod.event.K_KP_5,
   tcod.event.K_CLEAR,
}

CONFIRM_KEYS = {
	tcod.event.K_RETURN, 
	tcod.event.K_KP_ENTER,
}

CURSOR_Y_KEYS = {
	tcod.event.K_UP: -1, 
	tcod.event.K_DOWN: 1,
	tcod.event.K_PAGEUP: -10,
	tcod.event.K_PAGEDOWN: 10,
}

ActionOrHandler = Union[Action, "BaseEventHandler"]

class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
	def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
		# Handle an event and return the next active event handler. 
		state = self.dispatch(event)
		if isinstance(state, BaseEventHandler):
			return state
		assert not isinstance(state, Action), f"{self!r} can not handle actions."
		return self

	def on_render(self, console: tcod.Console) -> None:
		raise NotImplementedError()

	def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
		raise SystemExit()

class EventHandler(BaseEventHandler):
	def __init__(self, engine: Engine):
		self.engine = engine

	def handle_events(self, event: tcod.event.Event) -> BaseEventHandler: 
		# Handle events for input handlers with an engine
		action_or_state = self.dispatch(event)
		if isinstance(action_or_state, BaseEventHandler):
			return action_or_state
		if self.handle_action(action_or_state):
			# A valid action was performed. 
			if not self.engine.player.is_alive:
				# The player aws killed sometime during or after the action
				return GameOverEventHandler(self.engine)
			return MainGameEventHandler(self.engine) # return to the main handler
		return self

	def handle_action(self, action: Optional[Action]) -> bool: 
		"""Handle actions returned from event methods. Returns true if the action will advance a turn"""
		if action is None: 
			return False
		try:
			action.perform()
		except exceptions.Impossible as exc:
			self.engine.message_log.add_message(exc.args[0], color.impossible)
			return False
		self.engine.handle_enemy_turns()

		self.engine.update_fov()
		return True

	def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
		if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
			self.engine.mouse_location = event.tile.x, event.tile.y

	def on_render(self, console: tcod.Console) -> None:
		self.engine.render(console)

class AskUserEventHandler(EventHandler): 
	# Handles user input for actions which require special inputs

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		# By default any key exits this input handler
		if event.sym in {
			tcod.event.K_LSHIFT,
			tcod.event.K_RSHIFT,
			tcod.event.K_LCTRL,
			tcod.event.K_RCTRL,
			tcod.event.K_LALT,
			tcod.event.K_RALT,
		}:
			return None
		return self.on_exit()

	def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
		# by default any mouse click exits this input handler.
		return self.on_exit()

	def on_exit(self) -> Optional[ActionOrHandler]:
		# Called when the User is trying to exit or cancel an action -> By default this returns to the main event handler. 
		return MainGameEventHandler(self.engine) 

class InventoryEventHandler(AskUserEventHandler): 
	# This handler lets the user select an item 

	TITLE = "<missing titile>"

	def on_render(self, console: tcod.Console) -> None: 
		# Render an inventory menu, which displays the items in the inventory, and the letter to select them. Will move to a different position based on where the player is located, so the player can always see where they are.
		super().on_render(console)
		number_of_items_in_inventory = len(self.engine.player.inventory.items)

		height = number_of_items_in_inventory + 2

		if height <= 3: 
			height = 3

		if self.engine.player.x <= 30:
			x = 40
		else: 
			x = 0
		y = 0

		width = len(self.TITLE) + 4

		console.draw_frame(
			x=x,
			y=y,
			width=width,
			height=height,
			title=self.TITLE,
			clear=True,
			fg=(255, 255, 255),
			bg=(0, 0, 0),
		)

		if number_of_items_in_inventory > 0:
			for i, item in enumerate(self.engine.player.inventory.items):
				item_key = chr(ord("a") + i)
				console.print(x + 1, y + i + 1, f"({item_key}) {item.name}")
		else: 
			console.print(x + 1, y + 1, "(Empty)")

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		player = self.engine.player
		key = event.sym
		index = key - tcod.event.K_a

		if 0 <= index <= 26: 
			try:
				selected_item = player.inventory.items[index]
			except IndexError:
				self.engine.message_log.add_message("Invalid entry.", color.invalid)
				return None
			return self.on_item_selected(selected_item)
		return super().ev_keydown(event)

	def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
		# Called when the user selects a valid item.
		raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
	# Handle using an inventory item.

	TITLE = "Select an Item to use"

	def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
		# Return the action for the selected item.
		return item.consumable.get_action(self.engine.player)

class InventoryDropHandler(InventoryEventHandler):
	# Handle dropping an inventory item. 
	TITLE = "Select an Item to drop."

	def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
		# Drop this item. 
		return actions.DropItem(self.engine.player, item)

class SelectIndexHandler(AskUserEventHandler):
	# Handles asking the userfor an index on the map.

	def __init__(self, engine: Engine): 
		# Sets the cursor to the player when this handler is constructed
		super().__init__(engine)
		player = self.engine.player
		engine.mouse_location = player.x, player.y 

	def on_render(self, console: tcod.Console) -> None:
		# Highlight the tile under the cursor. 
		super().on_render(console)
		x, y = self.engine.mouse_location
		console.tiles_rgb["bg"][x, y] = color.white
		console.tiles_rgb["fg"][x, y] = color.black

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		# Check for key movement or confirmation keys
		key = event.sym
		if key in MOVE_KEYS:
			modifier = 1 # Holding modifier keys will speed up movement.
			if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
				modifier *= 5
			if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
				modifier *= 10
			if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
				modifier *= 20

			x, y = self.engine.mouse_location
			dx, dy = MOVE_KEYS[key]
			x += dx * modifier
			y += dy * modifier
			# Clamp the cursor index to the map size.
			x = max(0, min(x, self.engine.game_map.width - 1))
			y = max(0, min(x, self.engine.game_map.height - 1))
			self.engine.mouse_location = x, y
			return None

		elif key in CONFIRM_KEYS:
			return self.on_index_selected(*self.engine.mouse_location)
		return super().ev_keydown(event)

	def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
		# Left click confirms a selection. 
		if self.engine.game_map.in_bounds(*event.tile):
			if event.button == 1:
				return self.on_index_selected(*event.tile)
			return super().ev_mousebuttondown(event)

	def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
		# Called when an index is selected
		raise NotImplementedError()

class LookHandler(SelectIndexHandler):
	# lets the player look around using the keyboard
	def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
		# Return to main handler
		return MainGameEventHandler(self.engine)

class SingleRangedAttackHandler(SelectIndexHandler):
	# Handles targeting a single enemy
	def __init__(
		self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]
	):
		super().__init__(engine)
		self.callback = callback

	def on_index_selected(self, x: int, y: int) -> Optional[Action]:
		return self.callback((x, y))

class AreaRangedAttackHandler(SelectIndexHandler):
	# Handles targeting an area within a given radius. Any entity within the radius will be affected
	def __init__(
		self,
		engine: Engine, 
		radius: int,
		callback: Callable[[Tuple[int, int]], Optional[Action]],
	):
		super().__init__(engine)

		self.radius = radius
		self.callback = callback

	def on_render(self, console: tcod.Console) -> None:
		# Highlight the tile under the cursor
		super().on_render(console)

		x,y = self.engine.mouse_location

		# draw the affected area 
		console.draw_frame(
			x=x - self.radius - 1, 
			y=y - self.radius - 1, 
			width=self.radius ** 2, 
			height=self.radius ** 2, 
			fg=color.red, 
			clear=False,
		)
		
	def on_index_selected(self, x: int, y: int) -> Optional[Action]:
		return self.callback((x, y))

class MainGameEventHandler(EventHandler):
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		action: Optional[Action] = None
		
		key = event.sym

		player = self.engine.player

		if key in MOVE_KEYS:
			dx, dy = MOVE_KEYS[key]
			action = BumpAction(player, dx, dy)
		
		elif key in WAIT_KEYS:
			action = WaitAction(player)

		elif key == tcod.event.K_ESCAPE:
			raise SystemExit()

		elif key == tcod.event.K_v:
			return HistoryViewer(self.engine)

		elif key == tcod.event.K_g:
			action = PickupAction(player)

		elif key == tcod.event.K_i:
			return InventoryActivateHandler(self.engine)

		elif key == tcod.event.K_d:
			return InventoryActivateHandler(self.engine)

		elif key == tcod.event.K_SLASH:
			return LookHandler(self.engine)

		# No valid key was pressed
		return action

class GameOverEventHandler(EventHandler):
	def ev_keydown(self, event: tcod.event.KeyDown) -> None: 
		if event.sym == tcod.event.K_ESCAPE:
			raise SystemExit()

class HistoryViewer(EventHandler): 
	# Print the history on a larger window which can be navigated

	def __init__(self, engine: Engine):
		super().__init__(engine)
		self.log_length = len(engine.message_log.messages)
		self.cursor = self.log_length - 1

	def on_render(self, console: tcod.Console) -> None:
		super().on_render(console) # Drawing the main state as the background.
		log_console = tcod.Console(console.width - 6, console.height - 6)

		# Drawing a border with a custom banner title. 
		log_console.draw_frame(0, 0, log_console.width, log_console.height)
		log_console.print_box(0, 0, log_console.width, 1, "~ Message History ~", alignment=tcod.CENTER)

		# Render the message log using the cursor parameter
		self.engine.message_log.render_messages(
			log_console,
			1,
			1,
			log_console.width - 2,
			log_console.height - 2, 
			self.engine.message_log.messages[: self.cursor + 1],
		)
		log_console.blit(console, 3, 3)

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]: 
		# Fancy cond movement to make it feel right
		if event.sym in CURSOR_Y_KEYS: 
			adjust = CURSOR_Y_KEYS[event.sym]

			if adjust < 0 and self.cursor == 0: 
				# Only move from the top to the bottom when on the edge. 
				self.cursor = self.log_length - 1
			elif adjust > 0 and self.cursor == 0: 
				# Same with bot and top movement
				self.cursor = 0 
			else:
				# Otherwise move while staying within the bounds of the history log. 
				self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
		elif event.sym == tcod.event.K_HOME: 
			self.cursor = 0 # Shoot to the top
		elif event.sym == tcod.event.K_END: 
			self.cursor = self.log_length - 1 # Shoot to the last message
		else: # Any other input kicks back to the game
			return MainGameEventHandler(self.engine)
		return None 


