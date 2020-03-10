
class Board:
    """ Note: "loc" refers to a [rank][file] location in memory of the 2D matrix that stores the board state
    "pos" refers to a '<file><rank>' string that is passed to the Board class to request access to the corresponding
    board_state location """
    def __init__(self):
        """ initializes a blank Xiangqi Board"""
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']    # column letters, or ranks
        self._ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']   # row numbers, or files

        # store the set of all locations that comprise the castle spots for red
        self._red_castle_spots = {'d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3'}
        # store the set of all locations that comprise the castle spots for black
        self._black_castle_spots = {'d10', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8'}

        # initialize empty board
        self._board_state = [  # board state represented as a 2D array
            [ None for file in self._files] for rank in self._ranks  # initialize all positions to None
        ]

        self._piece_state = {}          # dictionary of piece: pos pairs. When pieces are captured, value is set to None

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

    def get_board_state(self):
        """ returns pointer to 2D matrix that tracks board state. Positions that are not occupied are
        set to None."""
        return self._board_state

    def display_board(self, num_spaces = 2):
        delim = ' ' * num_spaces
        print( (delim * 10), "BLACK")
        print(' ', delim, ("  " + delim).join(self._files))  # print letter files in order
        for rank in reversed(self._ranks):                      #print black side first, from rank 10 to rank 1
            rank_state = self._board_state[int(rank) - 1]
            if rank == '10':
                line = rank + ' ' * (num_spaces - 1)
            else:
                line = rank + delim
            for item in rank_state:
                if item is None:
                    line += '---' + delim
                else:
                    line += repr(item)[:3] + delim # display first 3 characters of string representation, plus delim
            print(line)
        print(' ', delim, ("  " + delim).join(self._files))         # print letter files in order
        print(delim * 10, "RED")
        print()
        print()

    def place_piece(self, piece, to_pos):
        """
        Sets to_pos to be occupied by piece.
        :param item:  a Piece of any type
        :param to_pos: A position that will be occupied by the piece
        :return: Sets to_pos to be occupied by piece. No return value.
        """
        rank,file = self.get_loc_from_pos(to_pos)
        self._board_state[rank][file] = piece  # piece now occupies to_pos
        self._piece_state[str(piece)] = to_pos

    def clear_piece(self, piece):
        """ sets the piece_state for None. Used for keeping track of captures"""
        self._piece_state[str(piece)] = None

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

    def get_general_pos(self, player):
        """ returns the position of the general on side of player"""
        return self._piece_state[ player[0] + "Ge"]

    def get_L_path(self, from_pos, to_pos):
        """ ordered list of [ (position, occupant) tuples] from from_pos to to_pos along L path.
                        Do not include current location in the list. Last item is to_pos. """
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        # generate the max 8 possible L-path destinations from the start location
        # the 4 maximum intermediate locations are one unit in every ortho direction
        loc_diffs_int = [(0,-1), (0,1), (1,0), (-1,0)]# permute one unit difference in rank and file directions
        # create a list of possible intermediate locations
        int_locs = [(from_rank + rank_diff, from_file + file_diff) for rank_diff, file_diff in loc_diffs_int]
        # filter any locs that are out of range
        int_locs = [(rank, file) for rank,file in int_locs if 0 <= rank < len(self._ranks) and 0 <= file < len(self._files)]

        # a valid L path will continue along ortho trajectory set by intermediate location
        # From start to intermediate, and from intermediate to destination, both moves increase rank or file
        # by one unit. Find the corresponding intermediate position,  if any, to to_pos
        int_pos = None
        for int_rank, int_file in int_locs:
            if from_rank - int_rank == int_rank - to_rank: # both ranks increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))
            elif from_file - int_file == int_file - to_file: # both files increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))

        if int_pos:
            try_dest = self.get_diagonal_path(int_pos, to_pos) # find a valid diagonal from intermedate to destination

        if int_pos and try_dest:
            path.append( (int_pos, self.get_piece_from_pos(int_pos)) )
            path.append(try_dest)

        return path

    def get_diagonal_path(self, from_pos, to_pos):
        """ ordered list of [ (location, occupant) tuples] from from_pos to to_pos along diagonal.
                Do not include current location in the list. Last item is to_pos. """
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        if from_rank == to_rank or from_file == to_file: # return empty path if positions are ortho to each other
            return path

        rank_diff = to_rank - from_rank
        file_diff = to_file - from_file
        if abs(rank_diff) != abs(file_diff): # return empty path if horizontal distance does not equal vertical distance
            return path

        flip_file = file_diff < 0
        flip_rank = rank_diff < 0

        if flip_rank:
            rank_range = range(from_rank - 1, to_rank - 1, - 1)
        else:
            rank_range = range(from_rank + 1, to_rank + 1)

        if flip_file:
            file_range = range(from_file -1, to_file - 1, -1)
        else:
            file_range = range(from_file + 1, to_file + 1)

        diag_positions = zip(rank_range, file_range)
        for rank, file in diag_positions:
            pos = self.get_pos_from_loc((rank,file))
            path.append((pos, self.get_piece_from_pos(pos)))
        return path

    def get_ortho_path(self, from_pos, to_pos):
        """ ordered list of [ (location, occupant) tuples] from from_pos to to_pos along ortho.
        Do not include current location in the list. Last item is to_pos. """

        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []
        flip_dir = False

        if from_rank != to_rank and from_file != to_file: # return empty path if to_pos is not ortho to from_pos
            return path

        if to_rank < from_rank:
            flip_dir = True
        if to_file < from_file:
            flip_dir = True

        if from_rank == to_rank and not flip_dir:
            file_range = range(from_file + 1, to_file + 1)
        elif from_rank == to_rank and flip_dir:
            file_range = range(from_file - 1, to_file - 1, -1)
        elif from_file == to_file and not flip_dir:
            rank_range = range(from_rank + 1, to_rank + 1)
        elif from_file == to_file and flip_dir:
            rank_range = range(from_rank - 1, to_rank - 1, -1)

        if from_rank == to_rank:            # get positions along rank from [from_file +1, to_file]
            for file in file_range:
                this_pos = self.get_pos_from_loc((to_rank, file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        elif from_file == to_file:
            for rank in rank_range:
                this_pos = self.get_pos_from_loc((rank, to_file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        return path

    def get_ranks(self):
        return self._ranks

    def get_files(self):
        return self._files

    def get_available_positions(self, side):
        """ returns a list of all positions that are unoccupied, or occupied by side's foe. Includes (at least)
        all possible locations that a Piece on side could occupy to on next move"""
        return_pos = []
        for file_str in self._files:
            for rank_str in self._ranks:
                occupant = self.get_piece_from_pos(file_str + rank_str)
                if occupant is None or occupant.get_side() == side:
                    return_pos.append(file_str + rank_str)
        return return_pos


