import random
from sudoku import *

class Generator:

    boards = []

    def create_board(data):
        val_table = {"a":1, "b":1, "c":1, "d":1, "e":1, "f":1, "g":1, "h":1, "i":1}
        val_keys = list(val_table.keys())
        random.shuffle(val_keys)
        for x in range(9):
            val_table[val_keys[x]] = x + 1
        for x in range(9):
            for y in range(9):
                if isinstance(data[x][y],str):
                    data[x][y] = val_table[data[x][y]]
        return data

    def get_board_file(filename):
        """
        retrieves a board from a file that contains only one board
        """
        with open(filename, "r") as file:
            data = file.readlines()
            board = Generator.format_board(data)
        return board

    def format_board(data):
        for line in range(len(data)):
            data[line] = data[line].split()
            for item in range(len(data[line])):
                if data[line][item] == "0": #get rid of string zeros
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
                temp.append(board[i+j])
            Generator.boards.append(temp)

    def output_boards(target):
        """
        output all the boards in class variable 'boards' to a target file
        """
        for board in Generator.boards:
            write_str = ""
            for x in range(len(board)):
                for y in range(len(board[x])):
                    write_str += str(board[x][y]) + " "
                write_str += "\n"
            with open(target, "a") as file:
                file.write(write_str)

    def gen_board():
        pass


# if __name__ == "__main__":
#     print_board(Generator.create_board(Generator.get_board_file("boards.txt")))
