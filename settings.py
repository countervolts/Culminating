## GAME SETTINGS

# game settings
WIDTH, HEIGHT = 21, 21
SIZE = 30
FONT_SIZE = 40
PLAYER_MOVE_DELAY = 185 
ENEMY_MOVE_DELAY = 175  

# colours
WALKABLE_COLOR = (200, 200, 200)
WALL_COLOR = (50, 50, 50)
END_COLOR = (255, 223, 0)
PLAYER_COLOR = (0, 0, 255)
ENEMY_COLOR = [255, 0, 0] 

# maze settings
maze = [['*' for _ in range(WIDTH)] for _ in range(HEIGHT)]
player = [1, 1]
end = [WIDTH - 2, HEIGHT - 2]

# visualize maze settings
VISUALIZE_MAZE_GENERATION = True
MAZE_GENERATION_SPEED = 25

# misc settings
FLASHLIGHT_RADIUS = 5
FLASHLIGHT_ON = True

# end point glow settings
END_GLOW_RADIUS = 5
END_GLOW_ON = True

# enemy settings
enemy = [WIDTH // 2, HEIGHT // 2]
ENEMY_FLASHLIGHT_RADIUS = 5
ENEMY_FLASHLIGHT_ON = True

# debug settings
DEBUG_MODE = True