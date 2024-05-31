# yep
import pygame
import random
import math

# for debug timing aswell printing stats
import time

# for colours
from colorama import init, Fore

# importing from settings.py
from settings import *


init() # for colorama

pygame.init()
screen = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * SIZE))
font = pygame.font.Font(None, FONT_SIZE)

dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]
direction = 1
level = 1
automated_movement = False
automated_start_time = 0

# enemy movement algorithm (this uses a star algo https://en.wikipedia.org/wiki/A*_search_algorithm)
def enemy_pathfinding(start, end):
    start_time = time.time()
    g = {start: 0}
    f = {start: heuristic(start, end)}
    parents = {}
    open_nodes = [start]
    closed_nodes = []
    while open_nodes:
        current = min(open_nodes, key=lambda x: f[x])
        if current == end:
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.append(current)
            path = path[::-1]
            end_time = time.time()
            return path

        open_nodes.remove(current)
        closed_nodes.append(current)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            if not (0 < x < WIDTH and 0 < y < HEIGHT) or maze[y][x] == '*' or (x, y) in closed_nodes:
                continue
            temp_g = g[current] + 1
            if (x, y) not in open_nodes or temp_g < g[(x, y)]:
                g[(x, y)] = temp_g
                f[(x, y)] = temp_g + heuristic((x, y), end)
                parents[(x, y)] = current
                if (x, y) not in open_nodes:
                    open_nodes.append((x, y))

    end_time = time.time()
    if DEBUG_MODE:
        log_debug(f'algorithm failed: {end_time - start_time:.2f}ms', level, entity='enemy')
    return []

def heuristic(node, end):
    return abs(node[0] - end[0]) + abs(node[1] - end[1])

player_last_move_time = pygame.time.get_ticks()
enemy_last_move_time = pygame.time.get_ticks()

# dfs function uses depth-first search to find a path from start to end
def dfs(start, end):
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node == end:
            return True
        if node not in visited:
            visited.add(node)
            for neighbor in get_neighbors(node):
                if maze[neighbor[1]][neighbor[0]] == '.':
                    stack.append(neighbor)
    return False

# remove_path function removes a path from start to end from the maze
def remove_path(start, end):
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node == end:
            break
        if node not in visited:
            visited.add(node)
            for neighbor in get_neighbors(node):
                if maze[neighbor[1]][neighbor[0]] == '.':
                    stack.append(neighbor)
    for node in visited:
        maze[node[1]][node[0]] = '*'

# get_neighbors function returns the valid neighbors of a node
def get_neighbors(node):
    x, y = node
    return [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if valid_move(nx, ny)]

# valid_move function checks if a move is valid
def valid_move(x, y):
    return 0 < x < WIDTH and 0 < y < HEIGHT

# draw_maze function draws the maze on the screen
def draw_maze():
    screen.fill((0, 0, 0))
    for i in range(HEIGHT):
        for j in range(WIDTH):
            color = WALL_COLOR if maze[i][j] == '*' else WALKABLE_COLOR
            text = font.render(maze[i][j], True, color)
            screen.blit(text, (j * SIZE + SIZE // 2 - text.get_width() // 2, i * SIZE + SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()

# carve function carves a path in the maze
def carve(x, y):
    dir = list(range(4))
    random.shuffle(dir)
    for i in dir:
        nx, ny = x + dx[i]*2, y + dy[i]*2
        if valid_move(nx, ny) and maze[ny][nx] == '*':
            maze[y + dy[i]][x + dx[i]] = '.'
            maze[ny][nx] = '.'
            if VISUALIZE_MAZE_GENERATION:
                draw_maze() 
                pygame.time.wait(MAZE_GENERATION_SPEED) 
            carve(nx, ny)

# carves path from starts to finish (this is the SHORTEST path though hence the name carve_sp (short path))
def carve_sp(start, end):
    stack = [start]
    while stack:
        x, y = stack[-1]
        if (x, y) == end:
            break
        dir = list(range(4))
        random.shuffle(dir)
        for i in dir:
            nx, ny = x + dx[i], y + dy[i]
            if valid_move(nx, ny) and maze[ny][nx] == '*':
                maze[ny][nx] = '.'
                stack.append((nx, ny))
                break
        else:
            stack.pop()

# func that generates the maze       
def generate_maze():
    global maze, player, enemy
    maze = [['*' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y in range(1, HEIGHT, 2):
        for x in range(1, WIDTH, 2):
            carve(x, y)
    carve(1, 1)
    maze[end[1]][end[0]] = '.' 
    carve_sp((1, 1), end)
    player = [1, 1]
    enemy = [WIDTH // 2, HEIGHT // 2] 
    # a attempt from me that will make multiple paths to the end (bug idiot <- me)
    paths = 0
    while paths < 3 and dfs((1, 1), end):
        paths += 1
        remove_path((1, 1), end)

# debug logging using colorama for cool looking colours!!! (there is probably a better way to do this)
def log_debug(message, level, entity=None):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
    if entity == 'Debug':
        color = Fore.RED
    elif entity == 'player':
        color = Fore.LIGHTMAGENTA_EX
    elif entity == 'Stats':
        color = Fore.LIGHTCYAN_EX
    elif entity == 'Stats1':
        color = Fore.BLUE 
    elif entity == 'maze gen':
        color = Fore.LIGHTYELLOW_EX
    else:
        color = colors[level % len(colors)]
    entity_name = "Player" if entity == "player" else "Enemy" if entity == "enemy" else "Debug" if entity == "Debug" else "Stats" if entity == "Stats" else "Maze Gen" if entity == "maze gen" else ""
    if DEBUG_MODE:
        print(f"{color}[Level {level}] [{entity_name}] {message}{Fore.RESET}")

# stats init
time_played = 0
num_moves = 0
num_levels = 0
file = 0

# func for logging the users stats then writing them to a file
def log_stats(time_played, num_moves, num_levels):
    global file
    time_played_minutes = time_played / 60
    log_debug(f"\nPlayer stats:", level, entity='Stats1')
    log_debug(f"Time played: {time_played} seconds ({time_played_minutes:.2f} minutes)", level, entity='Stats')
    log_debug(f"Number of moves: {num_moves}", level, entity='Stats')
    log_debug(f"Number of levels completed: {num_levels}", level, entity='Stats')

    # writing the file that will contain the users stats
    with open(f'Stats{file}.txt', 'w') as f:
        f.write(f"Time played: {time_played} seconds ({time_played_minutes:.2f} minutes)\n")
        f.write(f"Number of moves: {num_moves}\n")
        f.write(f"Number of levels completed: {num_levels}\n")

        file += 1 

clock = pygame.time.Clock()

generate_maze()
num_levels += 1

running = True

# debug vars
freeze_enemy = False
freeze_delay = 0

automated_movement = False
auto_delay = 0

god_mode = False
gm_delay = 0

noclip_mode = False
nc_delay = 0

# debug print control
player_moved = False

# this is a capture for the time stat
start_time = pygame.time.get_ticks()  

while running:
    dt = clock.tick()
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    time_played = (current_time - start_time) / 1000  

    # debug settings ive create to help me create this game,
    # these can be turned on/off in the settings.py file
    # aswell for now the settings are
    # F1 - freeze enemy
    # F2 - automated movement
    # F3 - god mode
    # F4 - noclip mode
    if DEBUG_MODE and keys[pygame.K_F1] and current_time - freeze_delay > 500:
        freeze_delay = current_time
        if freeze_enemy:
            ENEMY_MOVE_DELAY = 1000000  # now this is a pro freeze method
            freeze_enemy = False
            log_debug('Enemy freeze toggled on', level, entity='Debug')
        else:
            ENEMY_MOVE_DELAY = 175
            freeze_enemy = True
            log_debug('Enemy freeze toggled off', level, entity='Debug')

    # this is a comment to say that this code below me will automate the player movement when they press F2 
    if DEBUG_MODE and keys[pygame.K_F2] and current_time - auto_delay > 500:
        automated_movement = True
        log_debug('Automated movement activated', level) # idk why this prints like 10 million times when used
        automated_start_time = time.time()

    # blah blah blah F3 = god mode = true
    if DEBUG_MODE and keys[pygame.K_F3] and current_time - gm_delay > 500:
        gm_delay = current_time
        if god_mode:
            god_mode = False
            log_debug('God mode toggled off', level, entity='Debug')
        else:
            god_mode = True
            log_debug('God mode toggled on', level, entity='Debug')

    # yes!! pressing F4 key will make me have no collision 
    if DEBUG_MODE and keys[pygame.K_F4] and current_time - nc_delay > 500:
        nc_delay = current_time
        if noclip_mode:
            noclip_mode = False
            log_debug('Noclip mode toggled off', level, entity='Debug')
        else:
            noclip_mode = True
            log_debug('Noclip mode toggled on', level, entity='Debug')

    # lazy bypass for player_move_delay when using automated movement
    if automated_movement or current_time - player_last_move_time >= PLAYER_MOVE_DELAY:
        player_old_position = tuple(player)
        if automated_movement:
            path_start_time = time.time()
            path = enemy_pathfinding(tuple(player), tuple(end))
            path_end_time = time.time()
            if path:
                # noclip is so cool, anyways this just is sanity check for noclip mode
                if noclip_mode or maze[path[1][0]][path[1][1]] != '*':
                    player[0], player[1] = path[1]
                    log_debug(f'Player moved to {path[1]}', level, entity='player')
                if player == end:
                    log_debug('Reached the end', level, entity='player')
                    end_time = time.time()
                    log_debug(f'Total time: {end_time - automated_start_time:.2f}ms', level, entity='maze gen')
                    level += 1
                    log_debug('New maze generation', level, entity='maze gen')
                    generate_maze()
                    num_levels += 1
                    automated_movement = False

        # all player movement when pressing the w, a, s, c keys
        # aswell printing those movements
        # bug: when the user uses noclip it will turn the walls into walkable parts (turns them into . instead of *)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if noclip_mode or maze[player[1] - 1][player[0]] == '.':
                maze[player[1]][player[0]] = '.'
                player[1] -= 1
                maze[player[1]][player[0]] = ' '
                log_debug(f'Player moved up to ({player[0]}, {player[1]})', level, entity='player')
            direction = 0

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if noclip_mode or maze[player[1]][player[0] - 1] == '.':
                maze[player[1]][player[0]] = '.'
                player[0] -= 1
                maze[player[1]][player[0]] = ' '
                log_debug(f'Player moved left to ({player[0]}, {player[1]})', level, entity='player')
            direction = 3

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if noclip_mode or maze[player[1] + 1][player[0]] == '.':
                maze[player[1]][player[0]] = '.'
                player[1] += 1
                maze[player[1]][player[0]] = ' '
                log_debug(f'Player moved down to ({player[0]}, {player[1]})', level, entity='player')
            direction = 2

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if noclip_mode or maze[player[1]][player[0] + 1] == '.':
                maze[player[1]][player[0]] = '.'
                player[0] += 1
                maze[player[1]][player[0]] = ' '
                log_debug(f'Player moved right to ({player[0]}, {player[1]})', level, entity='player')
            direction = 1

        player_last_move_time = current_time
        player_moved = tuple(player) != player_old_position

    # processes gameplay (player movement, and quiting)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                num_moves += 1 

    # visual fix cause pygame is stupid
    screen.fill((0, 0, 0))

    # rendering the game and some other stuff ill comment in later (yes, im lazy)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            player_distance = math.sqrt((player[0] - j)**2 + (player[1] - i)**2)
            enemy_distance = math.sqrt((enemy[0] - j)**2 + (enemy[1] - i)**2)
            end_distance = math.sqrt((end[0] - j)**2 + (end[1] - i)**2)
            distance = min(player_distance, enemy_distance, end_distance)
            dimming_factor = max(0, 1 - distance / FLASHLIGHT_RADIUS) if FLASHLIGHT_ON or (ENEMY_FLASHLIGHT_ON and distance == enemy_distance) else 1
            color = tuple(int(c * dimming_factor) for c in (255, 255, 255))
            if maze[i][j] == '*':
                color = WALL_COLOR
            if (j, i) == tuple(end):
                glow_factor = max(0, 1 - end_distance / END_GLOW_RADIUS)
                color = tuple(int(c * glow_factor) for c in END_COLOR)
            text = font.render(maze[i][j], True, color)
            screen.blit(text, (j * SIZE + SIZE // 2 - text.get_width() // 2, i * SIZE + SIZE // 2 - text.get_height() // 2))

    player_text = font.render('O', True, PLAYER_COLOR)
    screen.blit(player_text, (player[0] * SIZE + SIZE // 2 - player_text.get_width() // 2, player[1] * SIZE + SIZE // 2 - player_text.get_height() // 2))

    if current_time - enemy_last_move_time >= ENEMY_MOVE_DELAY:
        path_start_time = time.time()
        path = enemy_pathfinding(tuple(enemy), tuple(player))
        path_end_time = time.time()
        if DEBUG_MODE and player_moved:
            log_debug(f'algorithm for enemy movement: {(path_end_time - path_start_time) * 1000:.2f}µs', level, entity='enemy')
        # Check that path has at least two elements before trying to access path[1]
        if path and len(path) > 1:
            enemy[0], enemy[1] = path[1]
        enemy_last_move_time = current_time

        # sanity check for god mode if true it wont end game
        if player == enemy and not god_mode:
            log_stats(time_played, num_moves, num_levels)
            running = False

    enemy_text = font.render('O', True, tuple(ENEMY_COLOR))
    screen.blit(enemy_text, (enemy[0] * SIZE + SIZE // 2 - enemy_text.get_width() // 2, enemy[1] * SIZE + SIZE // 2 - enemy_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
