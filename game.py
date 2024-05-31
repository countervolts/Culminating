import pygame
import random
import math
import time
from settings import *
from colorama import init, Fore

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

# enemy movement algorithm
def a_star_search(start, end):
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
        log_debug(f'A* search failed: {end_time - start_time:.2f}ms', level)
    return []

def heuristic(node, end):
    return abs(node[0] - end[0]) + abs(node[1] - end[1])

player_last_move_time = pygame.time.get_ticks()
enemy_last_move_time = pygame.time.get_ticks()

def valid_move(x, y):
    return 0 < x < WIDTH and 0 < y < HEIGHT

def draw_maze():
    screen.fill((0, 0, 0))
    for i in range(HEIGHT):
        for j in range(WIDTH):
            color = WALL_COLOR if maze[i][j] == '*' else WALKABLE_COLOR
            text = font.render(maze[i][j], True, color)
            screen.blit(text, (j * SIZE + SIZE // 2 - text.get_width() // 2, i * SIZE + SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()

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
    enemy = [WIDTH - 2, HEIGHT - 2]

def log_debug(message, level, entity=None):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    if entity == 'Debug':
        color = Fore.RED
    elif entity == 'player':
        color = Fore.GREEN
    else:
        color = colors[level % len(colors)]
    entity_name = "Player" if entity == "player" else "Enemy" if entity == "enemy" else "Debug" if entity == "Debug" else ""
    if DEBUG_MODE:
        print(f"{color}[Level {level}] [{entity_name}] {message}{Fore.RESET}")

clock = pygame.time.Clock()

generate_maze()

running = True

# debug vars
freeze_enemy = False
freeze_delay = 0
automated_movement = False
auto_delay = 0

while running:
    dt = clock.tick()
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

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

    if DEBUG_MODE and keys[pygame.K_F2] and current_time - auto_delay > 500:
        automated_movement = True
        log_debug('Automated movement activated', level)
        automated_start_time = time.time()

    if current_time - player_last_move_time >= PLAYER_MOVE_DELAY:
        if automated_movement:
            path_start_time = time.time()
            path = a_star_search(tuple(player), tuple(end))
            path_end_time = time.time()
            if path:
                player[0], player[1] = path[1]
                log_debug(f'Player moved to {path[1]}', level, entity='player')
                if player == end:
                    log_debug('Reached the end', level, entity='player')
                    end_time = time.time()
                    log_debug(f'Total time: {end_time - automated_start_time:.2f}ms', level)
                    level += 1
                    log_debug('New maze generation', level)
                    generate_maze()
                    automated_movement = False
        else:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if maze[player[1] - 1][player[0]] == '.':
                    maze[player[1]][player[0]] = '.'
                    player[1] -= 1
                    maze[player[1]][player[0]] = ' '
                    log_debug(f'Player moved up to ({player[0]}, {player[1]})', level, entity='player')
                direction = 0
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if maze[player[1]][player[0] - 1] == '.':
                    maze[player[1]][player[0]] = '.'
                    player[0] -= 1
                    maze[player[1]][player[0]] = ' '
                    log_debug(f'Player moved left to ({player[0]}, {player[1]})', level, entity='player')
                direction = 3
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if maze[player[1] + 1][player[0]] == '.':
                    maze[player[1]][player[0]] = '.'
                    player[1] += 1
                    maze[player[1]][player[0]] = ' '
                    log_debug(f'Player moved down to ({player[0]}, {player[1]})', level, entity='player')
                direction = 2
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if maze[player[1]][player[0] + 1] == '.':
                    maze[player[1]][player[0]] = '.'
                    player[0] += 1
                    maze[player[1]][player[0]] = ' '
                    log_debug(f'Player moved right to ({player[0]}, {player[1]})', level, entity='player')
                direction = 1
            player_last_move_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

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
        path = a_star_search(tuple(enemy), tuple(player))
        path_end_time = time.time()
        if DEBUG_MODE:
            log_debug(f'A* search for enemy movement: {path_end_time - path_start_time:.22f}ms', level, entity='enemy')
        if path:
            enemy[0], enemy[1] = path[1]
        enemy_last_move_time = current_time

    enemy_text = font.render('O', True, tuple(ENEMY_COLOR))
    screen.blit(enemy_text, (enemy[0] * SIZE + SIZE // 2 - enemy_text.get_width() // 2, enemy[1] * SIZE + SIZE // 2 - enemy_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()