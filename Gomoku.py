#!/usr/bin/env python3

GOMOKU_BOARD_SIZE = 15
DIRECTIONS = {
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UPPER LEFT": (-1, 1),
    "UPPER RIGHT": (1, 1),
    "DOWN LEFT": (-1, -1),
    "DOWN RIGHT": (1, -1)
}

class Gomoku:
    def __init__(self):
        self.gomoku_board = []
        self.b_pieces = []
        self.w_pieces = []
        self.player_turn = "B"

    def create_new_board(self):
        self.player_turn = "B"
        self.gomoku_board = []
        self.b_pieces = []
        self.w_pieces = []
        for i in range(GOMOKU_BOARD_SIZE):
            board_row = []
            for j in range(GOMOKU_BOARD_SIZE):
                board_row.append("")
            self.gomoku_board.append(board_row)

    def place_piece(self, row: int, column: int) -> bool:
        if row not in range(GOMOKU_BOARD_SIZE):
            return False
        if column not in range(GOMOKU_BOARD_SIZE):
            return False
        if self.gomoku_board[row][column] == "":
            if(self.gomoku_board[row][column] == ""):
                if self.player_turn == "B":
                        self.b_pieces.append((row, column))
                elif self.player_turn == "W":
                    self.w_pieces.append((row, column))
                self.gomoku_board[row][column] = self.player_turn
                if self.check_win() == False:
                    if self.player_turn == "B":
                        self.b_pieces.append((row, column))
                        self.player_turn = "W"
                    elif self.player_turn == "W":
                        self.w_pieces.append((row, column))
                        self.player_turn = "B"
                return True
        return False

    def check_win(self):
        game_won = False
        if self.player_turn == "B":
            for place in self.b_pieces:
                row = place[0]
                column = place[1]
                for d in DIRECTIONS:
                    if self.recursive_check(row, column, 0, d):
                        game_won = True
        elif self.player_turn == "W":
            for place in self.w_pieces:
                row = place[0]
                column = place[1]
                for d in DIRECTIONS:
                    if self.recursive_check(row, column, 0, d):
                        game_won = True
        if game_won:
            print("Game won by Player " + self.player_turn)
            print("Restarting game...")
            self.create_new_board()
            return True
        return False

    def recursive_check(
                        self,
                        row: int,
                        column: int,
                        chain: int,
                        direction: str) -> bool:
        if chain == 4:
            return True
        horizontal_movement = DIRECTIONS[direction][0]
        vertical_movement = DIRECTIONS[direction][1]
        if horizontal_movement < 0:
            if row - 1 < 0:
                return False
        if horizontal_movement > 0:
            if row + 1 >= GOMOKU_BOARD_SIZE:
                return False
        if vertical_movement < 0:
            if column - 1 < 0:
                return False
        if vertical_movement > 0:
            if column + 1 >= GOMOKU_BOARD_SIZE:
                return False
        row_change = row + horizontal_movement
        column_change = column + vertical_movement
        if(self.gomoku_board[row_change][column_change] != self.player_turn):
            return False
        return self.recursive_check(
                                    row + horizontal_movement,
                                    column + vertical_movement,
                                    chain + 1,
                                    direction)

    def draw_board(self):
        column_str = ""
        for n in range(9):
            column_str += str(n) + "  "
        for m in range(9, GOMOKU_BOARD_SIZE):
            column_str += str(m) + " "
        print(column_str)
        for i in range(GOMOKU_BOARD_SIZE):
            row_str = ""
            for j in range(GOMOKU_BOARD_SIZE):
                if self.gomoku_board[i][j] == "":
                    row_str += "+"
                else:
                    row_str += self.gomoku_board[i][j]
                if j < GOMOKU_BOARD_SIZE - 1:
                    row_str += "--"
                else:
                    row_str += " " + str(i)
            print(row_str)
            lines_str = ""
            if i < GOMOKU_BOARD_SIZE - 1:
                for p in range(GOMOKU_BOARD_SIZE):
                    lines_str += "|  "
                print(lines_str)

if __name__ == '__main__':
    gmk = Gomoku()
    gmk.create_new_board()
    while True:
        gmk.draw_board()
        print("It is Player " + gmk.player_turn + "'s turn.")
        command = input("Enter command:")
        if command == "quit":
            print("Understood, farewell.")
            exit()
        elif command == "restart":
            print("Restarting game...")
            gmk.create_new_board()
        elif "," in command:
            command_split = command.split(",")
            if len(command_split) == 2:
                if command_split[0].isdigit() and command_split[1].isdigit():
                    row = int(command_split[0])
                    column = int(command_split[1])
                    success = gmk.place_piece(row, column)
                    if success == False:
                        print("Invalid placement")
                else:
                    print("Placement command must be in format of:"
                           + " [int >= 0],[int >= 0]")
        else:
            print("Invalid input. Please choose one of the following:\n")
            print("- Input a row and column int, seperated by a ',' to"
                    + " try to place a game piece on the board")
            print("     Ex. 1,3 to place a piece at row 1, column 3")
            print("- 'quit': Exit program")
            print("- 'restart': Restarts game from the start")
        print("------------------------------------------------------------")