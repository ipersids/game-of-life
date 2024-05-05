import curses
import sys
import time
import collections


def main(window):
    pattern_dict = get_pattern()

    game = GameOfLife(pattern_dict)
    pattern = []
    curses.mousemask(4)

    key = ord('p')
    is_pause = True

    while True:
        g_height, g_width, g_y, g_x = game.get_game_grid_sizes(window)
        
        if key == ord('p'):
            window.clear()
            _pattern = game.draw_pattern_menu(window)
            key = 0
            is_pause = True
            if _pattern != None:
                pattern = _pattern
            window.clear()
            continue

        game.draw_main_menu(window)
        game.draw_pattern(window, g_height, g_width, pattern, y_start=g_y, x_start=g_x)

        window.refresh()
        curses.curs_set(0)
        time.sleep(0.2)

        key = window.getch()

        # pattern menu
        if key == ord('q'):
            sys.exit("Thanks for plaing The Game of Life. Have a nice day!")
        
        if key == curses.KEY_RESIZE:
            window.clear()
            continue

        if key == curses.KEY_MOUSE:
            game.input_pattern(pattern, g_height+4, g_width, g_y, g_x)


        if key == ord(' '):
            is_pause = not is_pause

        if is_pause == True:
            window.timeout(-1)
            continue

        if is_pause != True:
            window.timeout(0)
            neighbours = get_neighbours(pattern)
            pattern = run_evolution(pattern, neighbours, g_width, g_height)
            continue


def get_pattern(name=None):
    patterns = {
        "Glader": [[1,0,0],[0,1,1],[1,1,0]],
	    "Blinker": [[1,1,1]],
	    "Toad": [[1, 1, 1, 0],[0, 1, 1, 1]],
	    "Pulsar": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
	    "Gosper Gun": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
			[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ], 
	    "Diehard": [
            [0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1]
        ],
	    "Boat": [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ],
	    "Beacon": [
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
           ],
	    "Acorn": [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1]
        ],
	    "Spaceship": [
            [0, 0, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0]
        ]
    }
        
    
    new_dict = collections.defaultdict(set)

    if name != None:
        preset = patterns[name]
        pattern = []
        for row in range(0, len(preset)):
            for col in range(0, len(preset[row])):
                if preset[row][col] == 1:
                    pattern.append((col+1, row+1))
        new_dict[name] = pattern
    else:
        for key in patterns:
            preset = patterns[key]
            pattern = []
            for row in range(0, len(preset)):
                for col in range(0, len(preset[row])):
                    if preset[row][col] == 1:
                        pattern.append((col+1, row+1))
            new_dict[key] = pattern
    
    return new_dict


def get_neighbours(pattern):
    # find all neighbours for alive cells
    neighbr = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), 
        (0, 1), (1, -1), (1, 0), (1, 1)
    ]
    
    neighbr_count = collections.defaultdict(int)
    # x = i[0], y = i[1]
    for p in pattern:
        for n in neighbr:
            neighbr_count[(p[0]+n[0], p[1]+n[1])] += 1

    return neighbr_count


def run_evolution(pattern, neighbour_dict, width, height):
    """
    The game of Life is a simulation game that has a zero-player.
    This game is a cellular automaton devised 
    by the British mathematician John Horton Conway in 1970.

    The rules: 
    1) Any live cell with fewer than 2 live neighbors dies (underpopulation).
    2) Any live cell with 2 or 3 live neighbors lives on to the next generation.
    3) Any live cell with more than 3 live neighbors dies (overpopulation).
    4) Any dead cell with 3 live neighbors becomes a live cell (reproduction). 
    """
    # check the live status
    new_pattern = []
    for key in neighbour_dict:
        if 2 == neighbour_dict[key] and (key in pattern):
            new_pattern.append(key)
        if (
            neighbour_dict[key] == 3 
            and 0 <= key[0] <= width
            and 0 <= key[1] <= height
        ):
            new_pattern.append(key)
    
    return new_pattern



class GameOfLife:
    def __init__(self, pattern_dict, timeout=0.15, GRID='‧', LIFE='♥'):
        self.pattern_dict = pattern_dict
        self.pattern_names = list(pattern_dict.keys())
        self.timeout = timeout
        self.GRID = GRID
        self.LIFE = LIFE

        self.names = self.pattern_names.append("CREATE PATTERN")

    def _show(self, window):
        self.draw_pattern_menu(window)


    # set up the colors
    def set_color(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # set up the text styles
    def text_style(self, window, y, x, text, color_pair=4, dim=False, bold=False):
        self.set_color()

        if dim:
            window.attron(curses.A_DIM)
        if bold:
            window.attron(curses.A_BOLD)

        window.attron(curses.color_pair(color_pair))

        window.addstr(y, x, text)

        window.attroff(curses.color_pair(color_pair))
        window.attroff(curses.A_DIM)
        window.attroff(curses.A_BOLD)


    def draw_main_menu(self, window):
        # coursor visability and initialisation
        curses.curs_set(1)

        # get size of the screen
        height, width = window.getmaxyx()

        # main screen content
        title = "The Game of Life".upper()
        autor = "Written by Julia Persidskaia"
        command_bar = "Press: 'q' to exit | 'Space' to pause/start | 'p' to choose new pattern"
        scr_size = f"Screen size: {width} x {height}"
        # coordinates
        x_title = (width//2) - (len(title)//2) - 2
        x_autor = width - len(autor) - 2
        y_cmbar = height - 2
        w_cmbar = width - 2 - len(command_bar)
        # rendering
        self.text_style(window, 1, 1, scr_size, dim=True)
        self.text_style(window, 1, x_autor, autor, 4, dim=True)
        self.text_style(window, 3, x_title, title, 1, bold=True)
        self.text_style(window, y_cmbar, 1, command_bar + ' '*w_cmbar, 3)

        window.refresh()

    
    def draw_pattern(self, window, nrow, ncol, pattern=[], y_start=0, x_start=0, border=False, pattern_name=None):
        brd = 0
        if border == True:
            brd+=1
            window.border()
        
        if pattern_name != None:
            pattern = self.pattern_dict[pattern_name]

        for y in range(brd, nrow):
            for x in range(brd, ncol):
                if (x, y) in pattern:
                    self.text_style(window, y+y_start, x+x_start, self.LIFE, 2, bold=True)
                else:
                    self.text_style(window, y+y_start, x+x_start, self.GRID, 4, dim=True)


    def get_game_grid_sizes(self, window):
        # get size of the screen
        height, width = window.getmaxyx()
        # calculate the size and starting coordinates
        g_height = height - 8
        g_y = 5
        g_width = width - 3
        g_x = 1
        return g_height, g_width, g_y, g_x
    
    def draw_pattern_menu(self, window):

        names = self.pattern_names
        
        status = 0
        cursor_y = 0

        while status != ord('q'):
            # get actual grid sizes
            window.clear()
            self.draw_main_menu(window)
            

            # calculate the menu sizes
            height, width, y, x = self.get_game_grid_sizes(window)
            list_width = max(20, max(len(name) for name in self.pattern_names))
            list_height = max(height+4, len(self.pattern_names))
            patt_width = width - list_width
            patt_x = x + list_width + 1

            # create a curses pad to list the pattern names
            listpad = curses.newpad(list_height, list_width)
            listpad.keypad(True)
            listpad.scrollok(True)
            listpad_pminrow = 0
            listpad_refresh = lambda: listpad.refresh(listpad_pminrow, 0, y+1, x, list_height, list_width)
            listpad_refresh()

            # create a new window to display a coosen pattern
            pattwin = curses.newwin(height, patt_width, y, patt_x)
            pattwin.keypad(True)

            # activate the scrollind function in the pad
            # fill the pad with the pattern names
            for i, name in enumerate(names):
                text = (name + " "*(list_width-len(name)-1))[:list_width]
                if i == cursor_y:
                    self.text_style(listpad, i, x, text, 3, bold=True)
                    self.draw_pattern(pattwin, height-1, patt_width-2, border=True, pattern_name=name)
                else:
                    self.text_style(listpad, i, x, text, 4, bold=True)
            
            listpad_refresh()    
            pattwin.refresh()

            status = listpad.getch()

            # scroll and choose a pattern
            if status == curses.KEY_DOWN and cursor_y < len(names)-1:
                cursor_y+=1
            elif status == curses.KEY_UP and cursor_y > 0:
                cursor_y-=1
            elif status == ord('\n') and names[cursor_y] == "CREATE PATTERN":
                return []
            elif status == ord('\n') and names[cursor_y] != "CREATE PATTERN":
                name = names[cursor_y]
                return self.pattern_dict[name]


            if status == ord('q'):
                return None
            
    
    def input_pattern(self, pattern, g_height, g_width, g_y, g_x):
            try:
                _, x, y, _, event = curses.getmouse()
                if event == 4:
                    if g_x <= x <= g_width and g_y <= y <= g_height:
                        cell = (x-g_x, y-g_y)
                        if cell in pattern:
                            pattern.remove(cell)
                        else:
                            pattern.append(cell)
            except:
                pass


if __name__ == "__main__":
    curses.wrapper(main)