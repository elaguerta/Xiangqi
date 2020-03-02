
class Board:
    """ Note: "loc" refers to a [rank][file] location in memory of the 2D matrix that stores the board state
    "pos" refers to a '<file><rank>' string that is passed to the Board class to request access to the corresponding
    board_state location """
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
            [ None for file in self._files] for rank in self._ranks  # initialize all positions to None
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

    def display_board(self, num_spaces = 2):
        delim = ' ' * num_spaces
        print( (delim * 10), "RED")
        print(' ', delim, ("  " + delim).join(self._files))
        for rank in self._ranks:
            rank_state = self._board_state[int(rank) - 1]
            if rank == '10':
                line = rank + ' ' * (num_spaces - 1)
            else:
                line = rank + delim
            for item in rank_state:
                if item is None:
                    line += '---' + delim
                else:
                    line += repr(item) + delim
            print(line)
        print(delim * 10, "BLACK")

    def place_piece(self, piece, to_pos):
        """
        Sets to_pos to be occupied by item. Returns the piece, if any, that was previously on to_pos.
        Note: does not check if the move is legal.
        :param item:  a Piece of any type
        :param to_pos: A position that will be occupied by the piece
        :return: Sets to_pos to be occupied by piece. Get's the piece's previous pos, if any, sets
        the previous pos to None. Returns any piece that was previously on to_pos. 
        """
        rank,file = self.get_loc_from_pos(to_pos)
        self._board_state[rank][file] = piece  # piece now occupies to_pos

    def clear_pos(self, pos):
        """ Sets pos to None. Used for clearing a pos when a piece moves away from pos"""
        rank, file = self.get_loc_from_pos(pos)
        self._board_state[rank][file] = None  # set pos to None

    def get_loc_from_pos(self, pos):
        """ Helper method to translate pos strings to indices, to
        set and get positions in the board state"""
        rank_index = int(pos[1:]) - 1
        file_index = self._files.index(pos[0])
        return (rank_index, file_index) # return pointer to the pos location in the board_state

    def get_pos_from_loc(self, loc):
        """ Helper method to translate a (rank, file) tuple index into a position string"""
        rank_str = str(loc[0] + 1)
        file_str = str(self._files[loc[1]])
        return file_str + rank_str

    def get_piece_from_pos(self, pos):
        """ Returns the piece at pos, or None if pos is not occupied"""
        rank, file = self.get_loc_from_pos(pos)
        return self._board_state[rank][file]

    def get_ortho_path(self, from_pos, to_pos):
        """ ordered list of [ (location, occupant) tuples] from current pos to to_pos along ortho.
        Do not include current location in the list. Last item is to_pos.
        Does not check if there is a valid ortho path from from_pos to to_pos. That is the responsibility of Piece."""

        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []
        if from_rank == to_rank:            # get positions along rank from [from_file +1, to_file]
            for file in range(from_file + 1, to_file + 1):
                this_pos = self.get_pos_from_loc((to_rank, file))
                occupant = self._board.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        elif from_file == to_file:
            for rank in range(from_rank + 1, to_rank + 1):
                this_pos = self.get_pos_from_loc((rank, to_file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        return path

    def get_ranks(self):
        return self._ranks

    def get_files(self):
        return self._files

