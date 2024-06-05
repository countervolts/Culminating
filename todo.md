## finished things

- [x] implement function that creates a file and shows the user their game stats.
- [x] improve comments throughout the code.
- [x] implement output when the user dies, showing:
    - score (implemented score system)
    - time played
    - number of moves
    - number of levels completed
- [x] organize the auto move debug_log.

## stuff todo

### new features

- [ ] make the game get harder as the levels go on:
    - make enemy move faster (reduce the time between enemy moves)
    - make maze bigger (increase width height every level or two)
    - [?] implement difficulty scale in settings.py

- [ ] implement an easy way to change settings that isn't in the `settings.py` file.
- [ ] show the user something between levels (possibly use the end game stats logging).
- [ ] show game details before the game starts.

### bug fixes
- [ ] fix the issue where the user can't go to the next level when completing the current level:
    - how to replicate the issue: walk to the yellow dot and it won't let them finish.
    - when in auto move, it will allow them to go to the next level.
- [ ] fix line 317 with player noclip being buggy when walking into walls.
