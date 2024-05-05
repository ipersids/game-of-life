# Conway's Game of Life

### Description:
<center>
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGNyMDltMHo4dWkwN2hpYm0ya2ZzMDc3d3NwdWFkbnhrNTBjNXVwaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/z46VFoWnTgCpGq56Uy/giphy.gif"/>
</center>

<br>

> <br>The Game of Life is a zero-player simulation game designed by the British mathematician _John Horton Conway_ in 1970.<br>
    <br>
    **The rules:**  <br>
    1) Any live cell with fewer than 2 live neighbors dies (underpopulation). <br>
    2) Any live cell with 2 or 3 live neighbors lives on to the next generation. <br>
    3) Any live cell with more than 3 live neighbors dies (overpopulation). <br>
    4) Any dead cell with 3 live neighbors becomes a live cell (reproduction). <br>
    <br>
    <br>
    _More about the game and its history: [Wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)_<br>
    <br>


**What's inside**<br>
The content of the project folder:
```
Game_of_Life/
├── project.py
├── test_project.py
└── README.md
```
The `project/project.py` file contains all the necessary code to run the program. <br>
The `project/test_project.py` file is used to test the main functions.

Used libraries:

```Python
import curses
import sys
import time
import collections
```
Let's take a closer look on the content of the `project/project.py` file.

```Python
def get_pattern(name=None):
    patterns = {
        "Glader": [[1, 0, 0], [0, 1, 1], [1, 1, 0]],
        "Blinker": [[1, 1, 1]],
        ...
    }
    ...

>>> Example Output
{
    "Glader": [(1, 1), (2, 2), (3, 2), (1, 3), (2, 3)]
    "Blinker": [(1, 1), (2, 1), (3, 1)],
    ...
}
```
This function contains a dictionary of available patterns for the game and generates a dictionary with the coordinates of alive cells. You can find new patterns on the internet (typically formatted similarly to this function, using `list[list[int]]` typing) and add new patterns to the game menu. If name is not None, the function returns the specific pattern chosen by name only.


```Python
def get_neighbours(pattern: dict[str, list[tuple[int, int]]]) -> dict:
    ...

>>> Example Output
{
    ...
    (2, 0): 1,
    (2, 1): 3,
    (2, 2): 4,
    (2, 3): 3,
    ...
}
```
The `get_neighbours` function counts the total number of alive cells for each neighbor and returns a dictionary with the coordinates of each neighbor and the number of alive cells around them.

```Python
def run_evolution(pattern: dict, neighbour_dict: dict, width: int, height: int) -> list[tuple[int, int]]:
    ...

>>> Example Output
[(2, 0), (2, 1), (2, 2)]
```
This function implements the rules of the game and returns a new pattern that fits within the current `width` and `height` of the game grid for dynamic resizing during the game.

```Python
class GameOfLife:
    def __init__(self, pattern_dict, timeout=0.15, GRID='‧', LIFE='♥'):
        self.pattern_dict = pattern_dict
        self.pattern_names = list(pattern_dict.keys())
        self.timeout = timeout
        self.GRID = GRID
        self.LIFE = LIFE

        self.names = self.pattern_names.append("CREATE PATTERN")

    ...
```
The `GameOfLife` class uses the `curses` library to draw the Game of Life in the terminal.<br>
<br>
### Game Features Description:

* Pattern menu: Access this menu by pressing `p`, choose a pattern using the arrow keys (`up` or `down`), and run it by pressing `Enter`.
* Create your own pattern from scratch.
* Main game screen: Pause/start evolution by pressing `Space`.
* Add/remove new alive cells by clicking on the game grid on the main game screen.
* Exit from the pattern menu or the game by pressing `q`.
* Dynamic screen resizing.

## Installation

To run Conway's Game of Life, follow these steps:
1. Clone the Repository to your local machine using git:
```bash
git clone git@github.com:ucylama/Game_of_Life.git
```
2. Dependencies are not required. <br>
4. Run the Game <br>
This will launch the game interface in the terminale using the curses library.
```bash
python project.py
```
5. **Enjoy Playing!** <br>
Explore the pattern menu, interact with the game grid, and enjoy the evolution!
<br>

<br>
_________

Written by Julia Persidskaia.<br>
[LinkedIn](https://www.linkedin.com/in/iuliia-persidskaia/) <br>