import random
from typing import List, Set, SupportsInt, Tuple, Union, overload
import pickle
from copy import deepcopy
import os.path


class Generator:
    """Object to hold previously created boards and to create more from stored templates
    
    Board templates are stored with int 0 for blanks and string letters to be templated
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

    def __init__(self, filename: str = None) -> None:
        """
        Parameters
        ----------
        filename : str
            location of the pickled boards file. 
            If None or empty string, defaults to Boards/board.pkl and will create the default template
        """
        if filename is None or not os.path.isfile(filename):
            self.board_file = "src/Boards/board.pkl"
            if not os.path.isfile(
                self.board_file
            ):  # someone using default shouldn't lose all stored data
                with open(self.board_file, "wb") as fp:
                    pickle.dump([self.PREMADE_BOARD], fp)
        else:
            self.board_file = filename
        self.boards = []  # type: ignore

    def templatize_board(self, board: List[List[int]]) -> None:
        """Takes a board and converts clues to string placeholders. Appends result to self.boards

        Parameters
        ----------
        board : List[List[int]]
            solvable board with clues
        """
        temp: List[List[Union[int, str]]] = []
        holders = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        random.shuffle(holders)
        d = {i: k for i, k in enumerate(holders, start=1)}
        for row in board:
            temp.append([d[k] if k != 0 else 0 for k in row])
        self.boards.append(temp)

    def create_board(self) -> List[List[int]]:
        """Randomly choose a template stored in self.boards and return a playable board

        Returns
        -------
        list[list[int]]
            A board of ints
        """
        board = random.choice(self.boards)
        holders = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        random.shuffle(holders)
        val_dict = {x: i for i, x in enumerate(holders, start=1)}
        for i in range(9):  # board is 9x9
            for j in range(9):
                if isinstance(board[i][j], str):  # only non blanks are string
                    board[i][j] = val_dict[board[i][j]]
        return board

    def load_board_file(self) -> None:
        """Loads the board stored in a pickled file to the object
        
        File location is stored in self.board_file from initialization.
        Do not call unless file exists, should only need to output_boards at end of use
        """
        try:
            with open(self.board_file, "rb") as fp:
                temp_boards = pickle.load(fp)
            for b in temp_boards:
                if b not in self.boards:
                    self.boards.append(b)
        except FileNotFoundError:
            print(
                f"Error: file {self.board_file} does not exist. No boards were loaded"
            )

    def output_boards(self) -> None:
        """Writes the board templates to stored board_file, in a pickled format
        """
        with open(self.board_file, "wb") as fp:
            pickle.dump(self.boards, fp)

    @staticmethod
    def pretty_print(board: List[List[int]]) -> None:
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
        """Takes in a list of strings representing a board(s)
        Turns string zeros into ints so board creation works

        Parameters
        ----------
        data : List[str]
            List of strings representing board

        Returns
        -------
        List[List[str | int]]]
        """
        ret = [line.split() for line in data]
        for line in range(len(ret)):
            for item in range(len(ret[line])):
                if ret[line][item] == "0":  # get rid of string zeros
                    ret[line][item] = 0
        return ret

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


class NaiveSolver:
    """Simple backtracking solver that incrementally tries each value in a cell

    Recursive and no object __init__
    """

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
        blank = NaiveSolver.find_blank(table)
        if blank:
            row, col = blank
        else:
            # return being done with whole board
            return True
        for v in range(1, 10):
            if (
                NaiveSolver.check_box(table, row, col, v)
                and NaiveSolver.check_row(table, row, v)
                and NaiveSolver.check_column(table, col, v)
            ):
                table[col][row] = v
                if NaiveSolver.solve_board(
                    table
                ):  # this creates the backtracking approach
                    return True
                table[col][row] = 0
        return False


class BeerGenerator(Generator):
    ORDER = 3  # store like this to allow scaling up to 'larger' sudoku
    FULL_SET = set([i for i in range(1, 10)])

    def __init__(self, filename: str = None) -> None:
        """create a sudoku board generator that uses Daniel Beer's methodology

        This is created following Daniel Beer's algorithm, 
        https://dlbeer.co.nz/articles/sudoku.html
        Copyright (C) 2011 Daniel Beer <dlbeer@gmail.com>
        
        Permission to use, copy, modify, and/or distribute this software for any
        purpose with or without fee is hereby granted, provided that the above
        copyright notice and this permission notice appear in all copies.

        Parameters
        ----------
        filename : str, optional
            file path to read in board data from, or where to store it, by default None
        """
        super().__init__(filename=filename)

    @classmethod
    def get_board_diffic(
        cls, board: List[List[int]], freedom: List[List[Set[int]]] = None
    ) -> int:
        """Calculate board difficulty, usually used on unsolved boards

        # TODO: complete and think about branching coefficients

        Parameters
        ----------
        board : List[List[int]]
            board to find difficulty of
        freedom : List[List[Set[int]]], optional
            List of sets containing choices for each cell, by default None

        Returns
        -------
        int
        """
        if freedom is None:
            freedom = cls.init_choices(board)
        diff = 0
        for row in freedom:
            for st in row:
                diff += len(st) ** 2
        return diff

    def generate_board_template(self, solution: List[List[int]], max_iter: int):
        """Make a new board template from a fully solved board
        
        Will append to self.boards. Either removes clues on the board or adds a pair back in. 
        Increasing max_iter will make a more difficult puzzle. 
        # TODO: verify that a board is uniquely solvable after a cycle else return

        Parameters
        ----------
        solution : List[List[int]]
            solved board to generate an unsolved board from
        max_iter : int
            how many cycles of revisions should a board go through
        """
        board = deepcopy(solution)
        for _ in range(max_iter):
            problem = deepcopy(board)
            for _ in range(20):
                s = random.randint(0, 80)
                r, c = s // 9, s % 9
                # flip a coin on removing a pair of values, or adding them in
                if random.random() < 0.5:
                    problem[r][c] = 0
                    problem[8 - r][8 - c] = 0
                else:
                    problem[r][c] = solution[r][c]
                    problem[8 - r][8 - c] = solution[8 - r][8 - c]
                choices = self.init_choices(problem)
                if self.is_legal_board(problem, choices):
                    test = deepcopy(problem)
                    if self.choose_rest(test, choices) == 0:
                        board = problem
        self.templatize_board(board)

    @classmethod
    def init_choices(cls, grid: List[List[int]]) -> List[List[Set[int]]]:
        """initialize the possible values for all cells in a grid

        Cells that have been filled in already will be demarked by a set containing only that value.

        Parameters
        ----------
        grid : List[List[int]]
            board to initialize the choices based on

        Returns
        -------
        List[List[Set[int]]]
        """
        freedom = [[cls.FULL_SET.copy() for _ in range(9)] for _ in range(9)]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != 0:
                    cls.remove_freedom(freedom, x, y, grid[y][x])
        return freedom

    @classmethod
    def remove_freedom(cls, freedom: List[List[set]], x: int, y: int, val: int):
        """Change the freedom based on adding val to the cell at position [y][x]

        Restores original state of cell [y][x] at end, so every cell will have at least 1 choice

        Parameters
        ----------
        freedom : List[List[set]]
            List of lists containing the freedoms for each cell
        x : int
        y : int
        val : int
            value to be inserted
        """
        saved = freedom[y][x].copy()
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
        freedom[y][x] = saved

    @classmethod
    def is_legal_board(cls, grid: List[List[int]], freedom: List[List[set]]) -> bool:
        """Labeled as a sanity checker, usually to make sure a board is solvable

        Makes sure that each filled in cell has its value in the appropriate freedom cell.
        If a cell's freedom set doesn't contain the value it is, then there is a reused value issue making it unsolvable.

        Parameters
        ----------
        grid : List[List[int]]
        freedom : List[List[set]]

        Returns
        -------
        bool
            True/False to answer whether it is solvable or not
        """
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != 0 and grid[y][x] not in freedom[y][x]:
                    return False
        return True

    @classmethod
    def choose_rest(cls, grid: List[List[int]], freedom: List[List[set]]) -> int:
        """Recursively solve grid, allows backtracking

        Parameters
        ----------
        grid : List[List[int]]
        freedom : List[List[set]]

        Returns
        -------
        int
            0 on completion, -1 on errors
        """

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

    def choose_box1(self, grid: List[List[int]]) -> None:
        """Fill in place the first box, starting in upper left hand corner of the grid

        Randomly chooses from set of remaining values for each cell

        Parameters
        ----------
        grid : List[List[int]]
            the completely empty board
        """
        box1 = self.FULL_SET.copy()
        for i in range(self.ORDER):
            for j in range(self.ORDER):
                v = random.choice(list(box1))
                box1.remove(v)
                grid[i][j] = v

    def choose_box2(self, grid: List[List[int]]) -> None:
        """Fill in place the second box, upper row - middle column

        For each box-row, stores the used values from the previous box then chooses a value
        from the other 2 box-rows.

        Parameters
        ----------
        grid : List[List[int]]
            board that has only the first box filled in
        """
        rows: List[Set[int]] = [set() for _ in range(self.ORDER)]
        choose: List[Set[int]] = [set() for _ in range(self.ORDER)]
        for i in range(self.ORDER):
            for el in grid[i][:3]:
                rows[i].add(el)
        # randomly choose 3 element for first box-row from the 6 possible elements
        free_set = rows[1].union(rows[2])
        for i in range(self.ORDER):
            v = random.choice(list(free_set))
            choose[0].add(v)
            free_set.remove(v)
        # make sure each doesn't reuse a value
        # middle_set = (rows[0] | rows[2]) - choose[0]
        # last_set = (rows[0] | rows[1]) - choose[0]
        middle_set = rows[0].union(rows[2]).difference(choose[0])
        last_set = rows[0].union(rows[1]).difference(choose[0])
        while len(last_set) > 3:
            v = random.choice(list(middle_set))
            choose[1].add(v)
            middle_set.remove(v)
            last_set.discard(v)  # discard throws no error if v doesn't exist
        # choose[1] = choose[1] | (middle_set - last_set)
        choose[1] = choose[1].union(middle_set.difference(last_set))
        choose[2] = last_set.copy()
        # slice assignment for speed
        for i in range(self.ORDER):
            l_choose = list(choose[i])
            random.shuffle(l_choose)
            grid[i][self.ORDER : 2 * self.ORDER] = l_choose

    def choose_box3(self, grid: List[List[int]]) -> None:
        """fill in the last box of the top row, needs to have other 2 boxes filled in

        For each row, finds remaining 3 elements available and randomly chooses location

        Parameters
        ----------
        grid : List[List[int]]
            board to fill in that has 2 boxes filled in
        """
        for i in range(self.ORDER):
            avail = self.FULL_SET.copy()
            for j in range(self.ORDER * 2):
                avail.remove(grid[i][j])
            free = list(avail)
            random.shuffle(free)
            grid[i][self.ORDER * 2 : self.ORDER * self.ORDER] = free

    def choose_col(self, grid: List[List[int]]) -> None:
        """choose left hand column values, should be called after box 1 is filled

        Removes the used values from first box, then randomly selects them to place in.

        Parameters
        ----------
        grid : List[List[int]]
        """
        avail = self.FULL_SET.copy()
        for i in range(self.ORDER):
            avail.remove(grid[i][0])
        for i in range(self.ORDER * 2):
            v = random.choice(list(avail))
            avail.remove(v)
            grid[self.ORDER + i][0] = v

    def generate_board(self) -> List[List[int]]:
        """Generate new solved board following Beer method

        Returns
        -------
        List[List[int]]
        """
        # board demarks the actual board, choices are all possibilities for a cell
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.choose_box1(board)
        self.choose_box2(board)
        self.choose_box3(board)
        self.choose_col(board)
        choices = self.init_choices(board)
        self.choose_rest(board, choices)
        return board


class DiagonalGenerator(BeerGenerator):
    def __init__(self, filename: str = None) -> None:
        """Class that uses slightly different methodology to Beer method

        Fills in diagonal, top-left to bottom-right, boxes then solves
        
        Parameters
        ----------
        filename : str, optional
            location to store pickled boards or of existing file, by default None
        """
        super().__init__(filename)

    def generate_board(self) -> List[List[int]]:
        """Generate new solved board

        Returns
        -------
        List[List[int]]
        """
        board = [[0 for _ in range(9)] for _ in range(9)]

        def choose_box(x, y, grid):
            # set to top left of the respective box
            x -= x % self.ORDER
            y -= y % self.ORDER
            curr = self.FULL_SET.copy()
            for i in range(self.ORDER):
                for j in range(self.ORDER):
                    v = random.choice(list(curr))
                    curr.remove(v)
                    grid[y + i][x + j] = v

        choose_box(0, 0, board)
        choose_box(3, 3, board)
        choose_box(6, 6, board)
        choices = self.init_choices(board)
        self.choose_rest(board, choices)
        return board


if __name__ == "__main__":
    gen = DiagonalGenerator()
    gen.generate_board()

