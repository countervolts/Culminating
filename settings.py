## GAME SETTINGS

# game settings
WIDTH, HEIGHT = 21, 21 # map size this will be dynamic in the future as the player goes from level to level
SIZE = 30 
FONT_SIZE = 40 # size of the characters and other things that are classified as "font" 
PLAYER_MOVE_DELAY = 185 
ENEMY_MOVE_DELAY = 175 # bug: when the user freezes then unfreezes the game the enemy, they will go to 175 delay because of ln 255 in game.py

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
FLASHLIGHT_ON = False # this should be a global variable

# end point glow settings
END_GLOW_RADIUS = 5
END_GLOW_ON = False # 

# enemy settings
enemy = [WIDTH // 2, HEIGHT // 2] # dont change please it breaks the game currently
ENEMY_FLASHLIGHT_RADIUS = 5
ENEMY_FLASHLIGHT_ON = True

# debug settings
DEBUG_MODE = True
# F1 - Freeze enemy
# F2 - Auto move/play/solve whatever
# F3 - God mode
# F4 - Noclip
