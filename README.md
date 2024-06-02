## updates

### Update 1 (date: 05-30) [changelog](https://github.com/countervolts/Culminating/commit/4d118febf46d2adf89fd9db028019ccb6e17dd55) 
  - added all files for the first time
  - implimented main core gameplay logic aswell enemy and other things
  - added debug settings

### Update 2 (date: 05-31) [changelog](https://github.com/countervolts/Culminating/commit/d879f4991ae27f6fcb8e69ae3b4436981a3f0db2)
  - lots of comments added
  - added more debug settings (god mode and noclip)
  - added stats logging/outputting, logs the following
      - time played (in seconds and minutes)
      - total moves (by keeping track of the w, a, s, d keypresses)
      - levels completed (just by doing  ```num_levels += 1``` after ever generate_maze func call)
  - added more colours aswell (in the ```log_debug``` function (line 176))
  - attempted to add functions that would create multiple paths to the end (need to fix)
  - improved ```log_debug``` printing for enemy movement (not completely flooding the console now)
      - uses ```player_moved = false``` so that it will only print the enemy movement debug when the player moves (which seems more reasonable)
  - added more to [todo.txt](https://github.com/countervolts/Culminating/blob/main/todo.txt)

### Update 2.5 (date: 06-02) [changelog](https://github.com/countervolts/Culminating/commit/3fddd9b9403ed398d1dd144a7845662fe924e2e2)
  - changed some comments aswell added some
  - fixed issue/bug i didnt know about with users ```automated_movement```
      - to fix this ive added a seperate algorithm ```automove_pf``` that uses BFS (breadth first search) to bruteforce
  - added ```debug_log``` for ```automated_movement```
  -  nothing new with [settings.py](https://github.com/countervolts/Culminating/blob/main/settings.py) or [todo.txt](https://github.com/countervolts/Culminating/blob/main/todo.txt)
