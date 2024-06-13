## formatting

```
## Update [Version] [changelog](LINK TO THE UPDATED GAME.PY NOT THE ENTIRE VERSION)
(if the version is a whole number its a release, if its something else its just minor fixes or changes)

### tl;dr for update
  - changes
    - something i added or changed within that change
```

# updates

## Update 1 (date: 05-30) [changelog](https://github.com/countervolts/Culminating/commit/4d118febf46d2adf89fd9db028019ccb6e17dd55) 
### first actual update
  - added all files for the first time
  - implimented main core gameplay logic aswell enemy and other things
  - added debug settings

## Update 2 (date: 05-31) [changelog](https://github.com/countervolts/Culminating/commit/d879f4991ae27f6fcb8e69ae3b4436981a3f0db2)
### docs updating, improving outputs
  - lots of comments added
  - added more debug settings (god mode and noclip)
  - added stats logging/outputting, logs the following
      - time played (in seconds and minutes)
      - total moves (by keeping track of the w, a, s, d keypresses)
      - levels completed (just by doing  `num_levels += 1` after ever generate_maze func call)
  - added more colours aswell (in the `log_debug` function (line 176))
  - attempted to add functions that would create multiple paths to the end (need to fix)
  - improved `log_debug` printing for enemy movement (not completely flooding the console now)
      - uses `player_moved = false` so that it will only print the enemy movement debug when the player moves (which seems more reasonable)
  - added more to [todo.txt](https://github.com/countervolts/Culminating/blob/main/todo.txt)

## Update 2.5 (date: 06-02) [changelog](https://github.com/countervolts/Culminating/commit/3fddd9b9403ed398d1dd144a7845662fe924e2e2)
### half update (not full update/minor changes)
  - changed some comments aswell added some
  - fixed issue/bug i didnt know about with users `automated_movement`
      - to fix this ive added a seperate algorithm `automove_pf` that uses BFS (breadth first search) to bruteforce
  - added `debug_log` for `automated_movement`
  -  nothing new with [settings.py](https://github.com/countervolts/Culminating/blob/main/settings.py) or [todo.txt](https://github.com/countervolts/Culminating/blob/main/todo.txt)

## Update 3ish (date: 06-05 (2:10 am)) [changelog](https://github.com/countervolts/Culminating/commit/00da44a554b4ee5e22be93ada6632dffe99871c8)
### half update (not full update/minor changes)
  - changed some naming
  - fixed output for `debug_log` when `automated_movement`
     - i added a flag so it will only print once
  - changed todo.txt to [todo.md](https://github.com/countervolts/Culminating/blob/main/todo.md) (looks better)
  -  nothing new with [settings.py](https://github.com/countervolts/Culminating/blob/main/settings.py) 

## Update 3 (date 06-05 (5:26 pm)) [changelog](https://github.com/countervolts/Culminating/commit/f8171a510a5cc8e726e4a61cc4fd81f43cb9a41b)
### full v3 update, added display_menu, and modifiers
  - added `display_menu` to show the user all the settings and allowing them to change it
    - doesnt currently update the settings.py file for some reason [see](https://github.com/countervolts/Culminating/blob/87a6406db63cf7b6840a37b9a05c35a907e27bf5/todo.md?plain=1#L32)
  - within `menu.py` ive added `default_settings` so that if the settings.py file isnt there it will create it with the default values
  - added "modifiers"
    - `LIGHTS_OUT` settings this to true will make all these settings become true aswell
      - `END_GLOW_ON`
      - `FLASHLIGHT_ON`
      - `ENEMY_FLASHLIGHT_ON`
    - when set to false those will be set to false
  - in [settings.py](https://github.com/countervolts/Culminating/blob/main/settings.py) changed `WIDTH` and `HEIGHT` to seperate lines (visually better)
  - in [todo.md](https://github.com/countervolts/Culminating/blob/main/todo.md) changed "implement an easy way to change settings that isn't in the `settings.py` file." into `finished things`
    - aswell added new bug [here](https://github.com/countervolts/Culminating/blob/87a6406db63cf7b6840a37b9a05c35a907e27bf5/todo.md?plain=1#L32)

## Update 3.5 (date 06-07) [changelog](https://github.com/countervolts/Culminating/commit/35275e1e019ffa08006783e6beb6c388c2aa9d59)
### half update (not full update/minor changes)
  - fixed output for `automated_movement` so it actually only prints once this time

## Update 4 (date 06-11) [changelog](https://github.com/countervolts/Culminating/commit/d86039434c243903df3766f411449b60234ef108)
### fixed the following: noclip, getting to next level and printing improvements. added print_info 
  - fixed the user not being able to finish the game when reaching the end
  - fixed noclip removing things (walls and walkables) when moved over
  - showing the user information on the following events, the function is `print_info` you can find it [here](https://github.com/countervolts/Culminating/commit/d86039434c243903df3766f411449b60234ef108#diff-cc0ae3198bf596e4b93f96f7168c61db98f4b773af06509a829115ede915a079R268) (doesnt require `debug_mode` to be true)
      - when game first started
      - when next level is generated
  - information being show is the following:
      - `PLAYER_MOVE_DELAY` returns the user movement delay [this can be found here](https://github.com/countervolts/Culminating/blob/81c67d080846739f208c45f4c08506fd4702645a/settings.py#L8) 
      - `ENEMY_MOVE_DELAY` returns the enemy movement delay [this can be found here](https://github.com/countervolts/Culminating/blob/81c67d080846739f208c45f4c08506fd4702645a/settings.py#L9) 
      - `LIGHTS_OUT` returns "True" or "False" [this can be found here](https://github.com/countervolts/Culminating/blob/81c67d080846739f208c45f4c08506fd4702645a/settings.py#L12)
      - `DEBUG_MODE` returns "True" or "False" [this can be found here](https://github.com/countervolts/Culminating/blob/81c67d080846739f208c45f4c08506fd4702645a/settings.py#L44)
  - remove some stupid comments
  - imported `os` ([python.org](https://docs.python.org/3/library/os.html))
    - used for clearing console before showing information using `os.system` ([find here](https://docs.python.org/3/library/os.html#os.system))
  - general printing impovements
  - updated [todo.md](https://github.com/countervolts/Culminating/commit/ce910f495d9945659aae9cf2c378648b3eccd5d1)

## Update 5 (date 06-13) [changelog](https://github.com/countervolts/Culminating/commit/47ead1cc025723b95f9bbd6503eda5fbc5846826)
### huge improvements to the enemies AI/pathfinding, added hearing, vision and patrol points
  - generates new [patrol points](https://github.com/countervolts/Culminating/commit/47ead1cc025723b95f9bbd6503eda5fbc5846826#diff-cc0ae3198bf596e4b93f96f7168c61db98f4b773af06509a829115ede915a079R328)
  - huge improvements to enemy pathfinding/AI
  - **I was inspired to do this after seeing a video about the AI used in the game [Alien Isolation](https://en.wikipedia.org/wiki/Alien:_Isolation), and how the enemy AI works in that game this is done on a EXTREMELY simple way only with the hearing and vision addation**
  - anyways it now does the following,
    - now can hear the player when they move
    - can see the player if they are in their sight (if ai sees player) (uses [bresenhamas algo](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm))
    - goes between 3 patrol points (or whatever `NUM_PATROL_POINTS` is set to)
  - player now makes noise when moving
  - prints AI version in the `print_info` (current verison 1.2.0)
  - added new consts to [settings.py](https://github.com/countervolts/Culminating/commit/a4e77d5cb859b3e75467533d5f2d8fc32db33a36)
    - `NUM_PATROL_POINTS` - declares the amount of partrol points the AI will go to (default 3)
    - `VISION_DISTANCE` - how far the AI's vision will be (default 5)
    - `HEARING_DISTANCE` - how far the AI can hear from (default 3)
    - `NOISE_DURATION` - how long noise will last when the user moves
  - updated (menu.py)[https://github.com/countervolts/Culminating/commit/0125bbb298c29b201a1725f1e633da722b525c80] to include the previously said consts
 
