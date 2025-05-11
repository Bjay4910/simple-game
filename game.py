#!/usr/bin/env python3

import random
import time
import os
import json

class TextAdventure:
    def __init__(self):
        self.player = {
            "name": "",
            "health": 100,
            "inventory": [],
            "location": "forest_entrance"
        }
        
        self.locations = {
            "forest_entrance": {
                "description": "You stand at the entrance of a mysterious forest. Tall trees loom ahead, and a narrow path leads deeper inside.",
                "exits": {"north": "forest_clearing", "east": "river_bank"},
                "items": ["stick"]
            },
            "forest_clearing": {
                "description": "A small clearing in the forest. Sunlight filters through the trees above.",
                "exits": {"south": "forest_entrance", "west": "ancient_tree"},
                "items": ["berries"]
            },
            "river_bank": {
                "description": "A peaceful river flows beside you. The water is clear and looks refreshing.",
                "exits": {"west": "forest_entrance", "north": "cave_entrance"},
                "items": ["water_flask"]
            },
            "ancient_tree": {
                "description": "An enormous ancient tree stands before you. Its trunk must be centuries old.",
                "exits": {"east": "forest_clearing"},
                "items": ["magic_leaf"]
            },
            "cave_entrance": {
                "description": "A dark cave yawns open in the hillside. Strange sounds echo from within.",
                "exits": {"south": "river_bank", "north": "cave_interior"},
                "items": []
            },
            "cave_interior": {
                "description": "The interior of the cave is dimly lit. Bizarre crystals grow from the walls, giving off a soft glow.",
                "exits": {"south": "cave_entrance"},
                "items": ["treasure_chest"]
            }
        }
        
        self.items = {
            "stick": "A sturdy wooden stick that could be used as a basic weapon.",
            "berries": "Red berries that look edible and might restore some health.",
            "water_flask": "A flask that can be filled with water for drinking later.",
            "magic_leaf": "A glowing leaf from the ancient tree. It pulses with strange energy.",
            "treasure_chest": "A locked chest that seems to contain something valuable."
        }
        
        self.events = {
            "forest_clearing": lambda: self.forest_event(),
            "cave_interior": lambda: self.cave_event()
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_slowly(self, text):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.02)
        print()
    
    def forest_event(self):
        if random.random() < 0.3 and "forest_event_happened" not in self.player:
            self.print_slowly("\nA wild fox appears from behind a bush!")
            self.print_slowly("It seems curious about you, but not threatening.")
            self.print_slowly("The fox watches you for a moment, then disappears back into the forest.")
            self.player["forest_event_happened"] = True
    
    def cave_event(self):
        if "treasure_chest" in self.locations["cave_interior"]["items"] and "magic_leaf" in self.player["inventory"]:
            self.print_slowly("\nYour magic leaf begins to glow brighter as you approach the treasure chest.")
            self.print_slowly("You hold it near the chest, and the lock clicks open!")
            self.print_slowly("Inside, you find a golden amulet. You take it and put it in your inventory.")
            self.player["inventory"].append("golden_amulet")
            self.locations["cave_interior"]["items"].remove("treasure_chest")
            self.items["golden_amulet"] = "A beautiful golden amulet that seems to radiate power."
    
    def start_game(self):
        self.clear_screen()
        self.print_slowly("Welcome to the Forest Adventure!")
        self.print_slowly("In this game, you'll explore a mysterious forest and discover its secrets.")
        self.print_slowly("\nWhat is your name, adventurer?")
        
        self.player["name"] = input("> ")
        
        self.clear_screen()
        self.print_slowly(f"Welcome, {self.player['name']}! Your adventure begins now...\n")
        time.sleep(1)
        
        self.game_loop()
    
    def show_status(self):
        location = self.player["location"]
        loc_info = self.locations[location]
        
        self.print_slowly(f"\n--- {location.replace('_', ' ').title()} ---")
        self.print_slowly(loc_info["description"])
        
        if loc_info["items"]:
            self.print_slowly("\nYou see the following items:")
            for item in loc_info["items"]:
                self.print_slowly(f"- {item.replace('_', ' ').title()}")
        
        self.print_slowly("\nPossible exits:")
        for direction, destination in loc_info["exits"].items():
            self.print_slowly(f"- {direction.title()} to {destination.replace('_', ' ').title()}")
        
        self.print_slowly(f"\nHealth: {self.player['health']}")
        
        if self.player["inventory"]:
            self.print_slowly("\nInventory:")
            for item in self.player["inventory"]:
                self.print_slowly(f"- {item.replace('_', ' ').title()}")
        else:
            self.print_slowly("\nInventory: Empty")
        
        # Check for location-specific events
        if self.player["location"] in self.events:
            self.events[self.player["location"]]()
    
    def get_command(self):
        self.print_slowly("\nWhat would you like to do?")
        return input("> ").lower().strip()
    
    def process_command(self, command):
        words = command.split()
        
        if not words:
            return
        
        action = words[0]
        
        if action in ["quit", "exit"]:
            return "quit"
        
        if action in ["north", "south", "east", "west", "n", "s", "e", "w"]:
            # Handle movement shortcuts
            if action == "n": action = "north"
            if action == "s": action = "south"
            if action == "e": action = "east"
            if action == "w": action = "west"
            
            # Try to move in the specified direction
            exits = self.locations[self.player["location"]]["exits"]
            if action in exits:
                self.player["location"] = exits[action]
                return "moved"
            else:
                self.print_slowly("You can't go that way.")
        
        elif action in ["take", "get", "pickup"] and len(words) > 1:
            item_name = ' '.join(words[1:])
            # Convert spaces to underscores for internal representation
            item_key = item_name.replace(' ', '_').lower()
            
            # Check if the item is in the current location
            location_items = self.locations[self.player["location"]]["items"]
            matching_items = [i for i in location_items if i.lower() == item_key]
            
            if matching_items:
                item = matching_items[0]
                self.player["inventory"].append(item)
                self.locations[self.player["location"]]["items"].remove(item)
                self.print_slowly(f"You picked up the {item.replace('_', ' ')}.")
            else:
                self.print_slowly(f"There is no {item_name} here.")
        
        elif action in ["drop"] and len(words) > 1:
            item_name = ' '.join(words[1:])
            item_key = item_name.replace(' ', '_').lower()
            
            if item_key in self.player["inventory"]:
                self.player["inventory"].remove(item_key)
                self.locations[self.player["location"]]["items"].append(item_key)
                self.print_slowly(f"You dropped the {item_name}.")
            else:
                self.print_slowly(f"You don't have a {item_name}.")
        
        elif action in ["examine", "look", "inspect"] and len(words) > 1:
            item_name = ' '.join(words[1:])
            item_key = item_name.replace(' ', '_').lower()
            
            # Check inventory and location
            if item_key in self.player["inventory"]:
                self.print_slowly(self.items.get(item_key, f"It's a {item_name}."))
            elif item_key in self.locations[self.player["location"]]["items"]:
                self.print_slowly(self.items.get(item_key, f"It's a {item_name}."))
            else:
                self.print_slowly(f"You don't see a {item_name} here.")
        
        elif action in ["use"] and len(words) > 1:
            item_name = ' '.join(words[1:])
            item_key = item_name.replace(' ', '_').lower()
            
            if item_key in self.player["inventory"]:
                if item_key == "berries":
                    self.print_slowly("You eat the berries. They're sweet and refreshing.")
                    self.player["health"] = min(100, self.player["health"] + 15)
                    self.player["inventory"].remove("berries")
                    self.print_slowly(f"Your health is now {self.player['health']}.")
                elif item_key == "water_flask":
                    if self.player["location"] == "river_bank":
                        self.print_slowly("You fill your flask with fresh water from the river.")
                        self.player["inventory"].remove("water_flask")
                        self.player["inventory"].append("filled_water_flask")
                        self.items["filled_water_flask"] = "A flask filled with fresh water. Drinking it might restore health."
                    else:
                        self.print_slowly("You need to be near water to fill this flask.")
                elif item_key == "filled_water_flask":
                    self.print_slowly("You drink the refreshing water.")
                    self.player["health"] = min(100, self.player["health"] + 20)
                    self.player["inventory"].remove("filled_water_flask")
                    self.player["inventory"].append("water_flask")
                    self.print_slowly(f"Your health is now {self.player['health']}.")
                else:
                    self.print_slowly(f"You're not sure how to use the {item_name} right now.")
            else:
                self.print_slowly(f"You don't have a {item_name}.")
        
        elif action in ["help"]:
            self.show_help()

        elif action in ["save"]:
            success, message = self.save_game()
            if success:
                self.print_slowly(f"\nGame saved successfully to {message}")
            else:
                self.print_slowly(f"\nFailed to save game: {message}")

        elif action in ["load"]:
            success, message = self.load_game()
            if success:
                self.print_slowly(f"\n{message}")
                self.clear_screen()
                return "loaded"  # Special signal to refresh game state
            else:
                self.print_slowly(f"\n{message}")
    
    def show_help(self):
        self.print_slowly("\n--- Help Menu ---")
        self.print_slowly("Commands you can use:")
        self.print_slowly("- north/south/east/west (or n/s/e/w): Move in a direction")
        self.print_slowly("- take/get [item]: Pick up an item")
        self.print_slowly("- drop [item]: Drop an item from your inventory")
        self.print_slowly("- examine/look/inspect [item]: Look at an item more closely")
        self.print_slowly("- use [item]: Use an item in your inventory")
        self.print_slowly("- save: Save your current game")
        self.print_slowly("- load: Load a previously saved game")
        self.print_slowly("- help: Show this help menu")
        self.print_slowly("- quit/exit: End the game")

    def save_game(self):
        """Save the current game state to a JSON file."""
        save_data = {
            "player": self.player,
            "locations": self.locations
        }

        # Create saves directory if it doesn't exist
        if not os.path.exists("saves"):
            os.makedirs("saves")

        # Get player name or use 'default' if not set
        player_name = self.player.get("name", "default").lower().replace(" ", "_")
        save_path = f"saves/{player_name}_save.json"

        try:
            with open(save_path, 'w') as save_file:
                json.dump(save_data, save_file, indent=4)
            return True, save_path
        except Exception as e:
            return False, str(e)

    def load_game(self):
        """Load a game from a JSON save file."""
        # Check if saves directory exists
        if not os.path.exists("saves"):
            return False, "No saved games found."

        # List available save files
        save_files = [f for f in os.listdir("saves") if f.endswith("_save.json")]

        if not save_files:
            return False, "No saved games found."

        # If player name is known, try to load their save directly
        player_name = self.player.get("name", "").lower().replace(" ", "_")
        player_save = f"{player_name}_save.json"

        save_path = None
        if player_name and player_save in save_files:
            save_path = f"saves/{player_save}"
        elif len(save_files) == 1:
            # If only one save exists, use that
            save_path = f"saves/{save_files[0]}"
        else:
            # Let the player choose from multiple saves
            self.print_slowly("\nAvailable saved games:")
            for i, save_file in enumerate(save_files, 1):
                # Display without the _save.json part
                name = save_file.replace("_save.json", "").replace("_", " ").title()
                self.print_slowly(f"{i}. {name}")

            self.print_slowly("\nEnter the number of the save to load, or 'cancel' to go back:")
            choice = input("> ").strip().lower()

            if choice == "cancel":
                return False, "Load canceled."

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(save_files):
                    save_path = f"saves/{save_files[choice_index]}"
                else:
                    return False, "Invalid selection."
            except ValueError:
                return False, "Invalid input."

        try:
            with open(save_path, 'r') as save_file:
                save_data = json.load(save_file)

            # Restore game state
            self.player = save_data["player"]
            self.locations = save_data["locations"]
            return True, f"Game loaded from {save_path}"
        except Exception as e:
            return False, f"Error loading game: {str(e)}"

    def game_loop(self):
        while True:
            self.show_status()
            cmd = self.get_command()

            result = self.process_command(cmd)
            if result == "quit":
                self.print_slowly("\nThanks for playing! Goodbye.")
                break
            elif result == "loaded":
                # Game state has been loaded, continue with refreshed state
                continue

            self.clear_screen()

if __name__ == "__main__":
    game = TextAdventure()
    game.start_game()