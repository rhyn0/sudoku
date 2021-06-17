import random
from sudoku import *
import pickle


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

    def __init__(self, filename) -> None:
        """
        Parameters
        ----------
        filename : str
            location of the pickled boards file. 
            If None or empty string, defaults to Boards/board.pkl
        """
        if not filename:
            self.board_file = "Boards/board.pkl"
            pickle.dump(self.PREMADE_BOARD, open(self.board_file, "wb"))
        else:
            self.board_file = filename
        self.boards = []

    def create_board(self):
        """Randomly choose a template stored in self.boards and return a playable board

        Parameters 
        ----------

        Returns
        -------
        list[list[int]]
            A board of ints
        """
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
        for x in range(9):
            for y in range(9):
                if isinstance(data[x][y], str):
                    data[x][y] = val_dict[data[x][y]]
        return data

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

    def format_board(data):
        for line in range(len(data)):
            data[line] = data[line].split()
            for item in range(len(data[line])):
                if data[line][item] == "0":  # get rid of string zeros
                    data[line][item] = 0
        return data

    def get_mul_boards(filename):
        data = ""
        with open(filename, "r") as file:
            data = file.readlines()
        board = Generator.format_board(data)
        for i in range(len(board) // 9):
            startLine = 9 * i
            temp = []
            for j in range(9):
                temp.append(board[i + j])
            Generator.boards.append(temp)

    def gen_board():
        pass


# if __name__ == "__main__":
#     print_board(Generator.create_board(Generator.get_board_file("boards.txt")))
