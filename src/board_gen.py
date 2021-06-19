import random
from typing import List
import pickle
from sudoku import *


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
    def pretty_print(board) -> None:
        """Output a pretty board with surrounding horizontal lines. Print to stdout

        Parameters
        ----------
        board : List[List[int]]
            board in list of lists format
        """
        print("-" * 79)
        for i in range(9):
            for j in range(9):
                print(f" {board[i][j]}", end="")
            print()
        print("-" * 79)

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

    def generate_board_template(self, board: List[List[str]]) -> None:
        """Make a new board template from a fully solved list
        TODO: use Daniel Beer method
        """
        pass

    def generate_new_board(self):
        ORDER = 3
        FULL_SET = set([i for i in range(1, 10)])
        # board demarks the actual board, choices are all possibilities for a cell
        board = [[0 for _ in range(9)] for _ in range(9)]
        choices = [[set() for _ in range(9)] for _ in range(9)]

        def choose_box1(grid):
            # modify in place, the first box of the board
            box1 = FULL_SET.copy()
            for i in range(ORDER):
                for j in range(ORDER):
                    v = random.choice(list(box1))
                    box1.remove(v)
                    grid[i][j] = v

        def choose_box2(grid):
            # modify in place, the second box based on first box
            rows = [set() for _ in range(ORDER)]
            choose = [set() for _ in range(ORDER)]
            for i in range(ORDER):
                for el in grid[i][:3]:
                    rows[i].add(el)
            free_set = rows[1].union(rows[2])
            for i in range(ORDER):
                choose[0].add(random.choice(list(free_set)))
            middle_set = rows[0].union(rows[1]).difference(choose[0])
            last_set = rows[0].union(rows[2]).difference(choose[0])
            while len(last_set) > 3:
                v = random.choice(list(middle_set))
                choose[1].add(v)
                middle_set.remove(v)
                if v in last_set:
                    last_set.remove(v)
            choose[1] = choose[1].union(middle_set).difference(last_set)
            choose[2] = last_set.copy()

            for i in range(ORDER):
                l_choose = list(choose[i])
                random.shuffle(l_choose)
                grid[i][ORDER : 2 * ORDER] = l_choose

        def choose_box3(grid):
            # modify in place, choose last possible values
            pass

        def choose_col(grid):
            # modify in place, choose left column
            pass

        def init_choices(grid, freedom):
            # decide possible values for blank/0 cells
            pass

        def choose_rest(grid, freedom):
            # recursively solve the board, allows backtracking
            pass

        choose_box1(board)
        choose_box2(board)
        Generator.pretty_print(board)


if __name__ == "__main__":
    gen = Generator()
    gen.generate_new_board()
