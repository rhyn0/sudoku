from math import *

FAIL = -1

def print_board(table):
    ret = ""
    for i in range(9):
        for j in range(9):
            if j % 3 == 0 and j != 0:
                ret = ret + "| "
            if j == 8:
                ret = ret + str(table[j][i]) + "\n"
            else:
                ret = ret + str(table[j][i]) + " "
        if i == 2 or i == 5:
            ret = ret + "---------------------\n"
    print(ret)

def check_box(table, i, j, cell_val):
    box_X = i // 3
    box_Y = j // 3
    for x in range(3):
        for y in range (3):
            if cell_val == table[box_X * 3 + x][box_Y * 3 + y]:
                return FAIL
    return 1

def check_row(table, j, cell_val):
    for x in range(9):
        if cell_val == table[x][j]:
            return FAIL
    return 1

def check_column(table, i, cell_val):
    for y in range(9):
        if cell_val  == table[i][y]:
            return FAIL
    return 1

def check(table, loc, val):
    if check_box(table, loc[0], loc[1], val) == FAIL or check_row(table, loc[1], val) == FAIL or check_column(table, loc[0], val) == FAIL:
        return FAIL
    else:
        return 1

def find_blank(table):
    for x in range(len(table)):
        for y in range(len(table[0])):
            if table[y][x] == 0:
                return (y,x)
    return None

def solve_board(table):
    blank = find_blank(table)
    if blank:
        col, row = blank
    else:
        #return being done with whole board
        return True
    for v in range(1,10):
        if check(table, (col,row), v) == 1:
            table[col][row] = v
            if solve_board(table): #this creates the backtracking approach
                return True
            table[col][row] = 0
    return False


if __name__ == "__main__":
    #arg = [[0,0,0,0,0,0,5,0,0],[0,0,0,0,0,9,0,0,0],[0,0,1,0,4,0,0,2,0],[0,0,0,5,0,0,0,0,0],[0,0,2,0,0,0,0,1,4],[0,3,0,7,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,8,0,0,0,0,7,0,0],[0,5,0,0,0,0,3,0,9]]
    #above is hard on this algorithm
    arg = [[5,6,0,8,4,7,0,0,0],[3,0,9,0,0,0,6,0,0],[0,0,8,0,0,0,0,0,0],[0,1,0,0,8,0,0,4,0],[7,9,0,6,0,2,0,1,8],[0,5,0,0,3,0,0,9,0],[0,0,0,0,0,0,2,0,0],[0,0,6,0,0,0,8,0,7],[0,0,0,3,1,6,0,5,9]]
    #above is a simple board, fast solve time
    print("INITIAL STATE")
    print_board(arg)
    solve_board(arg)
    print("SOLVED")
    print_board(arg)
