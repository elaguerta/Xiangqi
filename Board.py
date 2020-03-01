
class Board:
    def __init__(self):
        """ initializes a blank Xiangqi Board"""
        self._files = ['a', 'b', 'c', 'd', 'd', 'e', 'f', 'g', 'h', 'i']    # column letters, or ranks
        self._ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']   # row numbers, or files

        # store the set of all locations that comprise the castle spots for red
        self._red_castle_spots = {'d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3'}
        # store the set of all locations that comprise the castle spots for black
        self._black_castle_spots = {'d10', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8'}

        # store the rank that represents the boundary of the river on the red side
        self._red_river_bank = '5'
        # store the rank that represents the boundary of the river on the black side
        self._black_river_bank = '6'

        # initialize empty board
        self._board_state = [  # board state represented as a 2D array
            ['-' for file in self._files] for rank in self._ranks  # initialize all positions to empty string
        ]

    def get_castle_spots(self, player):
        """
        :param player: "red" or "black"
        :return: A set of positions that comprise the castle positions for that player
        """
        if player == 'red':
            return self._red_castle_spots
        elif player == 'black':
            return self._black_castle_spots
        else:
            return False

    def get_river_bank(self, player):
        """
        :param player: "red" or "black"
        :return: the rank that represents the boundary of the river on the player's side
        """
        if player == "red":
            return self._red_river_bank
        elif player == "black":
            return self._black_river_bank
        else:
            return False

    def get_board_state(self):
        """ returns the current board state as a 2D matrix. Positions that are not occupied are
        set to the empty string."""
        return self._board_state

    def get_occupant(self, pos):
        """returns the piece on location pos, or False if pos is vacant"""
        pos_rank = pos[1]
        pos_file = pos[0]
        piece = self._board_state[pos_rank][pos_file]
        if not piece:
            return False
        return piece

    def display_board(self, num_spaces = 2):
        delim = ' ' * num_spaces
        print( (delim * 6), "RED")
        print(' ', delim, delim.join(self._files))
        for rank in self._ranks:
            if rank == '10':
                print(rank, ' ' * (num_spaces - 1), delim.join(self._board_state[int(rank) - 1]))
            else:
                print(rank, delim, delim.join(self._board_state[int(rank) - 1]))
        print(delim * 6, "BLACK")


