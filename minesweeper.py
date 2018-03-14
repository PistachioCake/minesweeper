import random


class Cell:
    """A helper class to keep track of a cell"""

    def __init__(self, i, j):  # i = down, j = right therefore self = world[i][j]
        self.mine = False
        self.opened = False
        self.flagged = False
        self.location = (i, j)

    def open(self):
        self.opened = True

    def flag(self):
        self.flagged = not self.flagged

    def set_mine(self):
        self.mine = True


class Board:
    ortho_available = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    diag_available = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    standard_available = [(-1, -1), (-1, 0), (-1, 1),
                          (0,  -1),          (0,  1),
                          (1,  -1), (1,  0), (1,  1)]
    knight_available = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

    def __init__(self, **kwargs):
        self.LENGTH = kwargs.get("LENGTH", 10)
        self.HEIGHT = kwargs.get("HEIGHT", 10)
        self.NUM_MINES = kwargs.get("NUM_MINES", 10)
        self.available = self.__getattribute__(kwargs.get("available", "standard") + "_available")
        self.show_mines = kwargs.get("show_mines", False)

        # Create cells
        self.cells = tuple(tuple(Cell(i, j) for j in range(self.LENGTH)) for i in range(self.HEIGHT))

        # Set mines randomly, up to NUM_MINES
        mines = []
        while len(mines) < self.NUM_MINES:
            candidate = random.choice(list(cell for row in self.cells for cell in row))
            if candidate.mine:
                continue
            else:
                candidate.set_mine()
                mines.append(candidate)

        self.is_playing = True

    def __str__(self):
        """...prints... the... world... what is there not to get, Jeff?"""
        board_string = ""
        for row in self.cells:
            for cell in row:
                board_string += self.cell_string(cell) + " "
            board_string += "\n"
        return board_string

    def cell_string(self, cell):
        """Return the character for the cell"""
        if cell.opened:
            return str(self.get_number_mines(cell))
        else:  # TODO: fix up properly
            if cell.flagged:
                return '!'
            elif cell.mine and self.show_mines:
                return ','
            else:
                return '.'

    @property
    def solved(self):
        return all(cell.mine or cell.opened for row in self.cells for cell in row)

    def parse_input(self):  # TODO: FIX
        """Function to parse user input"""
        while True:
            user_choice = input("Your choice [\"(f)i j\" for the cell i down and j right, f to flag]\n\t> ")
            try:
                flag = False
                if user_choice[0] == 'f':
                    flag = True
                    user_choice = user_choice[1:]
                i, j = map(int, user_choice.split(' '))
                cell = self.cells[i][j]
                break
            except IndexError:
                print("Please use i between 0 and {} and j between 0 and {}".format(self.LENGTH, self.HEIGHT))
            except ValueError:
                if user_choice == 'a':
                    raise KeyboardInterrupt
                print("Please format your input as (f)\"i j\", where i and j are both integers (for example \"1 2\"), \
                 with a \"f\" at the beginning to flag the cell")
        if flag:
            self.flag(cell)
        else:
            if not cell.flagged:
                self.open(cell)

    def flag(self, cell):
        if not cell.opened:
            cell.flag()

    def open(self, cell, open_others=True):
        if cell.opened:
            if open_others and self.get_number_mines(cell) - self.get_number_flags(cell) == 0:
                # If number of surrounding mines equals num of surrounding flags, open all surrounding cells
                for target in self.get_neighbors(cell):
                        if not target.opened and not target.flagged:
                            self.open(target, open_others=False)
        elif cell.mine:
            self.is_playing = False
        else:
            cell.open()
            if self.get_number_mines(cell) == 0:
                for target in self.get_neighbors(cell):
                        self.open(target)

    def get_neighbors(self, cell):
        """Returns a list of the cells around the cell"""
        i, j = cell.location
        neighbors = []
        for x, y in self.available:
            cond0 = 0 <= x + i < self.HEIGHT  # Make sure the target cell is in the world
            cond1 = 0 <= y + j < self.LENGTH
            if cond0 and cond1:
                neighbors.append(self.cells[x + i][y + j])
        return neighbors

    def get_number_mines(self, cell):
        """Returns the number of mines around the cell"""
        return sum(map(lambda target: target.mine, self.get_neighbors(cell)))

    def get_number_flags(self, cell):
        """Returns the number of flags around the cell"""
        return sum(map(lambda target: target.flagged, self.get_neighbors(cell)))


def main():
    while True:
        menu = True
        if menu:
            try:
                user_in_length = int(input("Length (default 10)\t\t > "))
            except ValueError:
                user_in_length = 10
            try:
                user_in_height = int(input("Height (default 10)\t\t > "))
            except ValueError:
                user_in_height = 10
            try:
                user_in_num__mines = int(input("Number of mines (default 10)\t > "))
            except ValueError:
                user_in_num__mines = 10
            try:
                user_in_type = int(input("Type of game: (default Standard)\n[1] Standard \n[2] Orthogonal \n"
                                         "[3] Diagonal \n[4] Knight's Path\t\t > "))
            except ValueError:
                user_in_type = 1
            if user_in_type not in [1, 2, 3, 4]:
                user_in_type = 1
            board = Board(
                LENGTH=user_in_length,
                HEIGHT=user_in_height,
                NUM_MINES=user_in_num__mines,
                available={1: "standard", 2: "ortho", 3: "diag", 4: "knight"}[user_in_type],
            )
        else:
            board = Board()

        while board.is_playing and not board.solved:
            print(board)
            board.parse_input()

        print(board)

        if board.solved:
            print("Congratulations, you won!")
        else:
            print("Boom :( You lost.")

        play_again = input("Would you like to play again? [y/n] ")
        if play_again.lower().startswith("y"):
            continue
        else:
            break


if __name__ == "__main__":
    main()
