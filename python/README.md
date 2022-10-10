# Python
Folder for miscellaneous Python scripts, probably for solving various puzzles.

## Turtle Square
Prints all possible orientations of solutions to the 3x3 Turtle square puzzle, similar to what's shown [here](https://www.penguin.com/static/packages/us/yr-microsites/crazygamesolution/images/turtle.jpg).
```bash
python magic_square.py
```

## Talos
Solves the puzzles that are present in the game ["The Talos Principle"](https://store.steampowered.com/app/257510/The_Talos_Principle/).

In `solve.py`, in the `prep` function, set the puzzle board size and initial shapes, then:
```bash
python solve.py
```

## Color Sort
Solves the various types of Color Sort puzzles.

In `puzzle.py`, define all the tube with colors, then:
```bash
python puzzle.py
```

If you want to see what the game looks like through each iteration of the solving, enabling debug logging:
```bash
DEBUG_SOLVE=1 python puzzle.py
```
