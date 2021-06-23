import random
from typing import List, Tuple, Union
import pickle
from copy import deepcopy


class Generator:
    """Object to hold previously created boards and to create more from stored templates
    
    Board templates are stored with string 0 for blanks and string letters to be templated
    """

    PREMADE_BOARD = [
        ["e", "f", 0, "h", "d", "g", 0, 0, 0],
        ["c", 0, "i", 0, 0, 0, "f", 0, 0],
        [0, 0, "h", 0, 0, 0, 0, 0, 0],
        [0, "a", 0, 0, "h", 0, 0, "d", 0],
        ["g", "i", 0, "f", 0, "b", 0, "a", "h"],
        [0, "e", 0, 0, "c", 0, 0, "i", 0],
        [0, 0, 0, 0, 0, 0, "b", 0, 0],
        [0, 0, "f", 0, 0, 0, "h", 0, "g"],
        [0, 0, 0, "c", "a", "f", 0, "e", "i"],
    ]
    ORDER = 3
    FULL_SET = set([i for i in range(1, 10)])

    def __init__(self, filename: str = None) -> None:
        """
        Parameters
        ----------
        filename : str
            location of the pickled boards file. 
            If None or empty string, defaults to Boards/board.pkl and will create the default template
        """
        if not filename:
            self.board_file = "src/Boards/board.pkl"
            pickle.dump(self.PREMADE_BOARD, open(self.board_file, "wb"))
        else:
            self.board_file = filename
        self.boards = []

    def create_board(self) -> List[list]:
        """Randomly choose a template stored in self.boards and return a playable board

        Parameters 
        ----------

        Returns
        -------
        list[list[int]]
            A board of ints
        """
        board = random.choice(self.boards)
        val_dict = {
            "a": 1,
            "b": 1,
            "c": 1,
            "d": 1,
            "e": 1,
            "f": 1,
            "g": 1,
            "h": 1,
            "i": 1,
        }
        val_keys = list(val_dict.keys())
        random.shuffle(val_keys)
        for i, x in enumerate(val_keys, start=1):
            val_dict[x] = i
        for i in range(9):  # board is 9x9
            for j in range(9):
                if isinstance(board[i][j], str):  # only non blanks are string
                    board[i][j] = val_dict[board[i][j]]
        return board

    def load_board_file(self) -> None:
        """Loads the board stored in a pickled file to the object
        """
        try:
            self.boards = pickle.load(open(self.board_file, "rb"))
        except FileNotFoundError:
            print(
                f"Error: file {self.board_file} does not exist. No boards were loaded"
            )

    def output_boards(self) -> None:
        """Writes the board templates to stored board_file, in a pickled format
        """
        pickle.dump(self.boards, open(self.board_file, "wb"))

    @staticmethod
    def check_box(table: List[List[int]], i: int, j: int, cell_val: int) -> int:
        box_row = i - i % 3
        box_col = j - j % 3
        for x in range(3):
            for y in range(3):
                if cell_val == table[box_row + x][box_col + y]:
                    return 0
        return 1

    @staticmethod
    def check_row(table: List[List[int]], i: int, cell_val: int) -> int:
        for x in range(9):
            if cell_val == table[i][x]:
                return 0
        return 1

    @staticmethod
    def check_column(table: List[List[int]], j: int, cell_val: int) -> int:
        for y in range(9):
            if cell_val == table[y][j]:
                return 0
        return 1

    @staticmethod
    def find_blank(table: List[List[int]]) -> Union[tuple, None]:
        for x in range(len(table)):
            for y in range(len(table[0])):
                if table[y][x] == 0:
                    return (y, x)
        return None

    @staticmethod
    def solve_board(table: List[List[int]]) -> bool:
        """Recursive backtrack approach to solve an input sudoku board

        Parameters
        ----------
        table : List[List[int]]
            the sudoku board

        Returns
        -------
        bool
            True on solved, False on failure
        """
        blank = Generator.find_blank(table)
        if blank:
            row, col = blank
        else:
            # return being done with whole board
            return True
        for v in range(1, 10):
            if (
                Generator.check_box(table, row, col, v)
                and Generator.check_row(table, row, v)
                and Generator.check_column(table, col, v)
            ):
                table[col][row] = v
                if Generator.solve_board(
                    table
                ):  # this creates the backtracking approach
                    return True
                table[col][row] = 0
        return False

    @staticmethod
    def pretty_print(board) -> None:
        """Output a pretty board with surrounding horizontal lines. Print to stdout

        Parameters
        ----------
        board : List[List[int]]
            board in list of lists format
        """
        hline = "-" * 36
        print(hline)
        for i in range(9):
            if i % 3 == 0 and i > 0:
                print(hline)
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    print("  |", end="")
                print(f"  {board[i][j]}", end="")
            print()
        print(hline)

    @staticmethod
    def format_board(data):
        """Takes in a list of lists of strings representing a board or boards
        Turns string zeros into ints so board creation works

        Parameters
        ----------
        data : List[str]
            List of strings representing board

        Returns
        -------
        List[list[Union(str, int)]]
        """
        data = [line.split() for line in data]
        for line in range(len(data)):
            for item in range(len(data[line])):
                if data[line][item] == "0":  # get rid of string zeros
                    data[line][item] = 0
        return data

    def get_mul_boards(self, filename: str) -> None:
        """Read in boards from a given plaintext file to store in object

        Board format in plain text should be - 9 rows of 9 elements separated by a space

        Parameters
        ----------
        filename : str
            str representing path to plaintext file
        """
        with open(filename, "r") as file:
            data = file.readlines()
        all_boards = self.format_board(data)
        for i in range(0, len(all_boards), 9):
            self.boards.append(all_boards[i : i + 9])

    @classmethod
    def get_board_diffic(cls, board):
        pass

    def generate_board_template(self, board: List[List[int]], max_iter: int) -> None:
        """Make a new board template from a fully solved board
        # TODO: use Daniel Beer method harden
        """
        best = 0  # keep track of difficulty
        for _ in range(max_iter):
            problem = deepcopy(board)
            for _ in range(20):
                c, r = random.randint(0, 8), random.randint(0, 8)
                if random.random() < 0.5:
                    problem[r][c] = 0
                    problem[8 - r][8 - c] = 0
                else:
                    pass

    def choose_box1(self, grid):
        # modify in place, the first box of the board
        box1 = self.FULL_SET.copy()
        for i in range(self.ORDER):
            for j in range(self.ORDER):
                v = random.choice(list(box1))
                box1.remove(v)
                grid[i][j] = v

    def choose_box2(self, grid):
        # modify in place, the second box based on first box
        rows = [set() for _ in range(self.ORDER)]
        choose = [set() for _ in range(self.ORDER)]
        for i in range(self.ORDER):
            for el in grid[i][:3]:
                rows[i].add(el)
        free_set = rows[1].union(rows[2])
        for i in range(self.ORDER):
            v = random.choice(list(free_set))
            choose[0].add(v)
            free_set.remove(v)
        middle_set = rows[0].union(rows[2]).difference(choose[0])
        last_set = rows[0].union(rows[1]).difference(choose[0])
        while len(last_set) > 3:
            v = random.choice(list(middle_set))
            choose[1].add(v)
            middle_set.remove(v)
            last_set.discard(v)  # discard throws no error if v doesn't exist
        choose[1] = choose[1].union(middle_set.difference(last_set))
        choose[2] = last_set.copy()
        for i in range(self.ORDER):
            l_choose = list(choose[i])
            random.shuffle(l_choose)
            grid[i][self.ORDER : 2 * self.ORDER] = l_choose

    def choose_box3(self, grid):
        # modify in place, choose last possible values
        for i in range(self.ORDER):
            # for each actual row, compute remaining choices and then fill
            used = set()
            for j in range(self.ORDER * 2):
                used.add(grid[i][j])
            free = list(self.FULL_SET.difference(used))
            random.shuffle(free)
            grid[i][self.ORDER * 2 : self.ORDER * self.ORDER] = free

    def choose_col(self, grid):
        # modify in place, choose left column
        used = set()
        for i in range(self.ORDER):
            used.add(grid[i][0])
        free = self.FULL_SET.difference(used)
        for i in range(self.ORDER * 2):
            v = random.choice(list(free))
            free.remove(v)
            grid[self.ORDER + i][0] = v

    @classmethod
    def init_choices(cls, grid, freedom: List[List[set]]):
        # decide possible values for blank/0 cells
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != 0:
                    cls.remove_freedom(freedom, x, y, grid[y][x])

    @classmethod
    def choose_rest(cls, grid, freedom: List[List[set]]):
        # recursively solve the board, allows backtracking
        def least_free(grid, freedom: List[List[set]]) -> Tuple[int, int]:
            index = -1, -1
            score = 0
            for i in range(len(grid)):
                for j, cell_val in enumerate(grid[i]):
                    if cell_val == 0:
                        if score == 0 or score > len(freedom[i][j]):
                            index = (i, j)
                            score = len(freedom[i][j])
            return index

        ind_y, ind_x = least_free(grid, freedom)
        if ind_x < 0 or ind_y < 0:
            return 0
        # need a copy or it gets overwritten in later recursive calls
        current = freedom[ind_y][ind_x].copy()
        while len(current) > 0:
            # need this special function to make copy of each set in list
            new_free = deepcopy(freedom)
            v = random.choice(list(current))
            current.remove(v)
            grid[ind_y][ind_x] = v
            cls.remove_freedom(new_free, ind_x, ind_y, v)

            if cls.choose_rest(grid, new_free) == 0:
                return 0
        grid[ind_y][ind_x] = 0
        return -1

    def generate_beer_board(self):
        """generate a new solved board that will be used to create a template

        This is created following Daniel Beer's algorithm, 
        https://dlbeer.co.nz/articles/sudoku.html
        Copyright (C) 2011 Daniel Beer <dlbeer@gmail.com>
        
        Permission to use, copy, modify, and/or distribute this software for any
        purpose with or without fee is hereby granted, provided that the above
        copyright notice and this permission notice appear in all copies.
        """

        # board demarks the actual board, choices are all possibilities for a cell
        board = [[0 for _ in range(9)] for _ in range(9)]
        choices = [[self.FULL_SET.copy() for _ in range(9)] for _ in range(9)]
        self.choose_box1(board)
        self.choose_box2(board)
        self.choose_box3(board)
        self.choose_col(board)
        self.init_choices(board, choices)
        self.choose_rest(board, choices)

    @classmethod
    def generate_board(cls) -> List[List[int]]:
        board = [[0 for _ in range(9)] for _ in range(9)]
        choices = [[cls.FULL_SET.copy() for _ in range(9)] for _ in range(9)]

        def choose_box(x, y, grid):
            # set to top left of the respective box
            x -= x % cls.ORDER
            y -= y % cls.ORDER
            curr = cls.FULL_SET.copy()
            for i in range(cls.ORDER):
                for j in range(cls.ORDER):
                    v = random.choice(list(curr))
                    curr.remove(v)
                    grid[y + i][x + j] = v

        choose_box(0, 0, board)
        choose_box(3, 3, board)
        choose_box(6, 6, board)
        cls.init_choices(board, choices)
        cls.choose_rest(board, choices)
        return board

    @classmethod
    def remove_freedom(cls, freedom: List[List[set]], x: int, y: int, val: int):

        # remove from column
        for i in range(cls.ORDER ** 2):
            freedom[i][x].discard(val)

        # remove from row
        for i in range(cls.ORDER ** 2):
            freedom[y][i].discard(val)

        # remove from box
        start_row = y - y % cls.ORDER
        start_col = x - x % cls.ORDER
        for i in range(start_row, start_row + cls.ORDER):
            for j in range(start_col, start_col + cls.ORDER):
                freedom[i][j].discard(val)


if __name__ == "__main__":
    gen = Generator()
    b = gen.generate_board()
    gen.pretty_print(b)


"""
To calculate the difficulty of a board, we add the square of the freedom of each
cell as it gets filled in and we dive deeper recursively. Since this uses local variable
its value will be passed along instead of its reference and will only return when fully solved.
"""
