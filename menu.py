from colorama import Fore, Style
import re
import os

# this just doesnt work yet but it will create a settings.py with the default settings 
# when chaging settings it just wont change the settings.py nor the game

default_settings = """
# GAME SETTINGS

# game settings
WIDTH = 21
HEIGHT = 21 
SIZE = 30 
FONT_SIZE = 40 # size of the characters and other things that are classified as "font" 
PLAYER_MOVE_DELAY = 185
ENEMY_MOVE_DELAY = 175 # bug: when the user freezes then unfreezes the game the enemy, they will go to 175 delay because of ln 255 in game.py

# modifiers 
LIGHTS_OUT = True

# colours
WALKABLE_COLOR = (200, 200, 200)  # light gray
WALL_COLOR = (50, 50, 50)  # dark gray
END_COLOR = (255, 223, 0)  # yellow
PLAYER_COLOR = (0, 0, 255)  # blue
ENEMY_COLOR = (255, 0, 0)  # red

# maze settings
maze = [['*' for _ in range(WIDTH)] for _ in range(HEIGHT)]
player = [1, 1]
end = [WIDTH - 2, HEIGHT - 2]

# visualize maze settings
VISUALIZE_MAZE_GENERATION = True # just for more visual appeal
MAZE_GENERATION_SPEED = 25 # the speed it will generate the maze infront of the user

# misc settings
FLASHLIGHT_RADIUS = 5
FLASHLIGHT_ON = LIGHTS_OUT  # this should be a global variable
PATROL_POINT_COLOR = (0, 255, 0)  # green

# end point glow settings
END_GLOW_RADIUS = 5
END_GLOW_ON = LIGHTS_OUT

# enemy settings
enemy = [WIDTH // 2, HEIGHT // 2] # dont change please it breaks the game currently
ENEMY_FLASHLIGHT_RADIUS = 5
ENEMY_FLASHLIGHT_ON = LIGHTS_OUT
NUM_PATROL_POINTS = 3 # 3 is normal
WALL_PENALTY = 10

# consts for vision, hearing distances (advanced algo)
VISION_DISTANCE = 5
HEARING_DISTANCE = 3
NOISE_DURATION = 5  # in seconds

# debug settings
DEBUG_MODE = True
# F1 - Freeze enemy
# F2 - Auto move/play/solve whatever
# F3 - God mode
# F4 - Noclip
"""

def backup():
    if not os.path.exists('settings.py'):
        with open('settings.py', 'w') as file:
            file.write(default_settings)
        print("Created default settings.py file.")

backup()

from settings import *

def updating(setting_name, new_value):
    with open('settings.py', 'r') as file:
        contents = file.readlines()

    for i, line in enumerate(contents):
        if setting_name in line:
            if isinstance(new_value, bool):
                old_value = re.search(r'\b(True|False)\b', line).group()
                contents[i] = line.replace(old_value, 'True' if new_value else 'False')
            elif isinstance(new_value, tuple):
                old_value = re.search(r'\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', line).group()
                new_value_str = f"({new_value[0]}, {new_value[1]}, {new_value[2]})"
                contents[i] = line.replace(old_value, new_value_str)
            else:
                old_value = re.search(r'\b\d+\b', line).group()
                contents[i] = line.replace(str(old_value), str(new_value))
            print(f"Updated {setting_name} from {old_value} to {new_value}")

    with open('settings.py', 'w') as file:
        file.writelines(contents)

def display_menu():
    global WIDTH, HEIGHT, SIZE, FONT_SIZE, PLAYER_MOVE_DELAY, ENEMY_MOVE_DELAY, LIGHTS_OUT, WALKABLE_COLOR, WALL_COLOR, END_COLOR, PLAYER_COLOR, ENEMY_COLOR, VISUALIZE_MAZE_GENERATION, MAZE_GENERATION_SPEED, FLASHLIGHT_RADIUS, FLASHLIGHT_ON, END_GLOW_RADIUS, END_GLOW_ON, ENEMY_FLASHLIGHT_RADIUS, ENEMY_FLASHLIGHT_ON, DEBUG_MODE

    def bool_input(prompt, default):
        while True:
            choice = input(f"{prompt} (current: {'ON' if default else 'OFF'}) [y/n]: ").lower()
            if choice in ['y', 'n', '']:
                return choice == 'y' if choice else default
            print("Enter 'y' or 'n'.")

    def num_input(prompt, default):
        while True:
            choice = input(f"{prompt} (current: {default}): ")
            if choice.isdigit():
                return int(choice)
            elif choice == '':
                return default
            print("Enter a number.")

    def colour_input(prompt, default):
        while True:
            choice = input(f"{prompt} (current: {default}): ")
            if choice:
                try:
                    return tuple(map(int, choice.split(',')))
                except ValueError:
                    print("Enter RGB values separated by commas.")
            else:
                return default

    settings = [
        ("Map Width", WIDTH, num_input),
        ("Map Height", HEIGHT, num_input),
        ("Tile Size", SIZE, num_input),
        ("Font Size", FONT_SIZE, num_input),
        ("Player Move Delay (ms)", PLAYER_MOVE_DELAY, num_input),
        ("Enemy Move Delay (ms)", ENEMY_MOVE_DELAY, num_input),
        ("Lights Out Mode", LIGHTS_OUT, bool_input),
        ("Visualize Maze Generation", VISUALIZE_MAZE_GENERATION, bool_input),
        ("Maze Generation Speed (ms)", MAZE_GENERATION_SPEED, num_input),
        ("Flashlight Radius", FLASHLIGHT_RADIUS, num_input),
        ("Flashlight ON", FLASHLIGHT_ON, bool_input),
        ("End Glow Radius", END_GLOW_RADIUS, num_input),
        ("End Glow ON", END_GLOW_ON, bool_input),
        ("Enemy Flashlight Radius", ENEMY_FLASHLIGHT_RADIUS, num_input),
        ("Enemy Flashlight ON", ENEMY_FLASHLIGHT_ON, bool_input),
        ("Number of Patrol Points", NUM_PATROL_POINTS, num_input),
        ("Vision Distance", VISION_DISTANCE, num_input),
        ("Hearing Distance", HEARING_DISTANCE, num_input),
        ("Noise Duration (s)", NOISE_DURATION, num_input),
        ("Debug Mode", DEBUG_MODE, bool_input),
        ("Walkable Color", WALKABLE_COLOR, colour_input),
        ("Wall Color", WALL_COLOR, colour_input),
        ("End Color", END_COLOR, colour_input),
        ("Player Color", PLAYER_COLOR, colour_input),
        ("Enemy Color", ENEMY_COLOR, colour_input),
        ("Patrol Point Color", PATROL_POINT_COLOR, colour_input),
        ("Wall Penalty", WALL_PENALTY, num_input),
    ]

    print("Game Settings Menu")
    print("------------------")
    for i, (name, value, _) in enumerate(settings, start=1):
        print(f"{i}. {Fore.BLUE}{name}{Style.RESET_ALL} (current: {Fore.GREEN}{value}{Style.RESET_ALL})")

    print("\nEnter the number of the setting you want to change (or press Enter to skip):")
    while True:
        choice = input("\nSelection: ")
        if choice == '':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(settings):
            idx = int(choice) - 1
            name, value, func = settings[idx]
            new_value = func(f"Enter new value for {name}", value)
            globals()[name.replace(" ", "_").upper()] = new_value
            settings[idx] = (name, new_value, func)
            updating(name.replace(" ", "_").upper(), new_value)
        else:
            print("Enter a number corresponding to a setting.")

    print("\nSettings updated successfully!\n")
