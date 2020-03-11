class GeneralPiece(Piece):
    """ Creates GeneralPieces
        general_positions is a class variable, a dictionary of initial positions keyed by player color """
    general_positions = {'red':'e1', 'black':'e10'}

    def __init__(self, side, board):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
                passed as arguments by Player. """
        super().__init__(side, board)
        self._movement = 'ortho'  # generals move ortho
        self._path_length = 1  # generals move one point
        self._pos = GeneralPiece.general_positions[side] # assign a position based on side

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ge".
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ge"

    def is_legal(self, to_pos):
        """ Calls super().is_legal and then checks the additional parameters of the general's movement:
        the general must stay in the palace, flying general move may be executed """

        # check if this general could capture enemy general at to_pos via flying general
        flying_general_flag = self.is_flying_general(to_pos)

        if flying_general_flag:     # if flying general is possible, temporarily lift path length restriction
            self._path_length = None

        # check Piece.is_legal (with max path length restriction lifted if flying general is possible)
        # if it's not legal for a Piece.is_legal() reason, reset path length and return False
        if not super().is_legal(to_pos):
            self._path_length = 1    # reset path length
            return False

        # If we get to this point, all Piece.is_legal() conditions are met.
        # In the case that flying general isn't possible, check also that the general remains in the castle.
        # If not, reset the path length and return False
        if not flying_general_flag and to_pos not in (self._board.get_castle_spots(self._side)):
            self._path_length = 1
            return False

        # Move is legal. Reset path length and return True
        self._path_length = 1
        return True

    def is_flying_general(self, to_pos):
        """ Helper method to self.is_legal.
        Returns True if this general could capture enemy general at to_pos via flying general"""
        other_gen_pos = self._board.get_general_pos(self._opp)  # get the other general's position
        if other_gen_pos == to_pos and other_gen_pos[0] == self._pos[0]:  # if both generals on the same file
            path_to_gen = self.get_path(other_gen_pos)            # get ortho path to general
            if self.num_jumps(path_to_gen) == 0:        # if no intervening pieces, flying general is possible
                return True

class AdvisorPiece(Piece):
    """ Creates AdvisorPieces
    Advisor_positions is a class variable, a dictionary of initial positions keyed by player color
    Two Advisor pieces are created by a call to Player.__init__(), one for each of the two positions
    per side."""
    advisor_positions = {
        'red': ['d1', 'f1'],
        'black': ['d10', 'f10']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board) # call the Piece init with side and board
        self._movement = 'diagonal'  # Advisors can move diagonally
        self._path_length = 1       # Advisors can only move one point

        # Assign a position from Advisor Piece.
        self._id = id_num      # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = AdvisorPiece.advisor_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ad" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ad" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Advisor to move to to_pos. Checks Piece.is_legal() conditions,
        with additional restriction that Advisors remain in the castle."""

        # to_pos must be a castle spot for this piece's side
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False

        # if it is a castle spot, check that all other legal conditions for Piece hold
        return super().is_legal(to_pos)

class ElephantPiece(Piece):
    """Creates ElephantPieces
                elephant_positions is a class variable, a dictionary of initial positions keyed by player color
                Two ElephantPieces are created by a call to Player.__init__()."""
    elephant_positions = {
        'red': ['c1', 'g1'],
        'black': ['c10', 'g10']
    }
    # legal_ranks is a class variable, a set of ranks that elephants may occupy keyed by player side
    # Elephants cannot cross the river.
    legal_ranks = {
        'red': {'1','2','3','4','5'},
        'black': {'10','9','8','7','6'}
    }

    def __init__(self, side, board, id_num):
        """ Initializes an Elephant Piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'diagonal'  # Elephants move diagonal
        self._path_length = 2 # Elephants move 2 points

        # assign a position from ElephantPiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = ElephantPiece.elephant_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "El" + [id_num for this specific piece].
                        This is intended to be unique for every piece in a Game """
        return self._side[0] + "El" + str(self._id)

    def is_legal(self, to_pos):
        """ call Piece.is_legal() with additional restriction that Elephants stay within their legal ranks,
        i.e. they don't cross the river."""
        return super().is_legal(to_pos) and to_pos[1:] in ElephantPiece.legal_ranks[self._side]

class HorsePiece(Piece):
    """Creates HorsePieces
            horse_positions is a class variable, a dictionary of initial positions keyed by player color
            Two HorsePieces are created by a call to Player.__init__()."""
    horse_positions = {
        'red': ['b1', 'h1'],
        'black': ['b10', 'h10']
    }

    def __init__(self, side, board, id_num):
        """Initialize a Horse piece. Side is 'red' or 'black' Side, board, and id_num are passed as arguments
        by Player. """
        super().__init__(side, board)
        self._movement = 'L-shaped'  # Horses move L-shaped
        self._path_length = 2   # L-paths are length 2: one point ortho, one point diagonal

        # assign a position from HorsePiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = HorsePiece.horse_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ho" + [id_num for this specific piece].
                This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ho" + str(self._id)

class ChariotPiece(Piece):
    """Creates ChariotPieces
        chariot_positions is a class variable, a dictionary of initial positions keyed by player color
        Two ChariotPositions are created by a call to Player.__init__()."""
    chariot_postions = {
        'red': ['a1', 'i1'],
        'black': ['a10', 'i10']
    }

    def __init__(self, side, board, id_num):
        """ Initializes a chariot piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
                passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # assign a position from ChariotPiece
        self._id =  id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = ChariotPiece.chariot_postions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ch" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ch" + str(self._id)

class CannonPiece(Piece):
    """ Creates CannonPieces
        cannon_positions is a class variable, a dictionary of initial positions keyed by player color
        Two Cannon pieces are created by a call to Player.__init__()."""
    cannon_postions = {
        'red': ['b3', 'h3'],
        'black': ['b8', 'h8']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho'  # Cannons move ortho

        # Assign a position from CannonPiece
        self._id =  id_num  # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = CannonPiece.cannon_postions[side][id_num - 1]  # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ca" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ca" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Cannon to move to to_pos. Checks Piece.is_legal() conditions,
        with additional support for exactly 1 jump if move to to_pos would result in a capture."""

        # cannon requires screen piece for capture, friend or foe
        # if this move would result in a capture, temporarily set jumps to 1
        occupant = self._board.get_piece_from_pos(to_pos)  # get the potential capture
        if occupant and occupant.get_side() != self._side: # if the potential capture is a foe, must have exactly 1 jump
            self._jumps = 1
        result = super().is_legal(to_pos)           # call super with jumps updated if necessary
        self._jumps = 0                             # reset jumps to 0
        return result

class SoldierPiece(Piece):
    """Creates SoliderPieces
    soldier_positions is a class variable, a dictionary of initial positions keyed by player color
    Two SoldierPieces are created by a call to Player.__init__()."""

    soldier_positions = {
        'red': ['a4', 'c4', 'e4', 'g4', 'i4'],
        'black': ['a7', 'c7', 'e7', 'g7', 'i7']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an soldier piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho' # soldiers move ortho
        self._path_length = 1
        self._crossed_river = False

        # assign a position from SoldierPiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = SoldierPiece.soldier_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "So" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "So" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Soldier to move to to_pos. Checks Piece.is_legal() conditions,
        with additional restrictions on the soldier's movement:
        Soldier cannot retreat, solider cannot move horizontally until it has crossed river."""

        # Check Piece.is_legal() conditions
        try_path = super().is_legal(to_pos)
        if not try_path:
            return False

        to_rank, to_file = self._board.get_loc_from_pos(to_pos)
        from_rank, from_file = self._board.get_loc_from_pos(self._pos)

        # If the move is a retreat, return False
        # red retreats along the same file from a higher rank to a lower rank
        if from_file == to_file and self._side == 'red' and to_rank < from_rank:
            return False
        # black retreats along the same file from a lower rank to a higher rank
        if from_file == to_file and self._side == 'black' and to_rank > from_rank:
            return False

        # if the move is horizontal and the Soldier has not yet crossed the river, return false
        # if the rank is the same, the move is horizontal
        if to_pos[1:] == self._pos[1:] and not self._crossed_river:
            return False

        # if we made it this far, move is legal for the Soldier. Return True
        return True

    def move(self, to_pos):
        """ Calls Piece.move(), then tags on a check for whether the soldier has crossed the river."""
        move_result = super().move(to_pos)        # move as usual

        # if red makes it to 6, or black makes it to 5, river was crossed. Set self._crossed_river to True
        if self._side == 'red' and to_pos[1:] == '6':
            self._crossed_river = True

        if self._side == 'black' and to_pos[1:] == '5':
            self._crossed_river = True

        return move_result

class Board:
    """ Creates Boards for use by XiangqiGame, Players, and Pieces
    Language notes:
        'loc' refers to a [rank][file] location in memory of the 2D matrix that stores the board state
        'pos' refers to a '<file><rank>' string used throughout the project as an alias for locations
        'side' refers to a player side of interest, and is string that may be 'red' or 'black'.
        Elsewhere in the project, 'player' is used as a parameter name for Player objects."""

    def __init__(self):
        """ Creates a Board, receives no arguments. The Board tracks the state of Pieces with two instance variables:
        self._board_state, which is keyed by location, and self._pieces, which is keyed by Piece.
        self._board_state is a 2D array where indices are [rank][file] locations, and values are Piece objects, or None.
        self._pieces is a dictionary where each key is the unique string representation of a Piece on the Board,
        and values are that Piece's current position.
        The two representations are intended to be equivalent before and after every call to Piece.move() and
        Piece.reverse_move() """

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

        self._piece_state = {} # dictionary of piece: pos pairs. When pieces are captured, value is set to None

    def get_castle_spots(self, side):
        """Returns the set of all positions that comprise the castle positions for side."""
        if side == 'red':
            return self._red_castle_spots
        elif side == 'black':
            return self._black_castle_spots
        else:
            return False

    def get_board_state(self):
        """ returns pointer to the 2D array that tracks the occupants of locations on the Board."""
        return self._board_state

    def display_board(self, num_spaces = 2):
        """ Displays the board to the console."""
        delim = ' ' * num_spaces        # number of spaces between each location in a rank
        print( (delim * 9), "BLACK")   # print black label, somewhat centered
        print(' ', delim, ("  " + delim).join(self._files))  # print letter files in order
        for rank in reversed(self._ranks):                      # print black side first, from rank 10 to rank 1
            rank_state = self._board_state[int(rank) - 1]
            if rank == '10':
                line = rank + ' ' * (num_spaces - 1)
            else:
                line = rank + delim
            for piece in rank_state:
                if piece is None:
                    line += '---' + delim
                else:
                    line += repr(piece)[:3] + delim # display first 3 chars of Piece's string representation, plus delim
            print(line)
        print(' ', delim, ("  " + delim).join(self._files))         # print letter files in order
        print(delim * 9, "RED") # print red label, somewhat centered
        print() # blank line

    def place_piece(self, piece, to_pos):
        """ Updates self._board_state and self._piece_state so that to_pos is occupied by piece.
        Note that Board has no access to Pieces.
        Piece is responsible for updating its own variable tracking its current position"""
        rank,file = self.get_loc_from_pos(to_pos) # translate the to_pos string to a [rank][file] index
        self._board_state[rank][file] = piece  # piece now occupies to_pos
        self._piece_state[str(piece)] = to_pos # update piece's position in self._piece_state dictionary
        return True

    def clear_piece(self, piece):
        """ Sets self._piece_state[piece] to None. Used for keeping track of captures.
        Note that this is not symmetrical with place_piece, since it does not affect self._board_state.
        This is because capturing a piece means that its previous location will be occupied by its captor."""
        self._piece_state[str(piece)] = None

    def clear_pos(self, pos):
        """ Sets pos to None. Used for clearing a pos when a piece moves away from pos"""
        rank, file = self.get_loc_from_pos(pos)
        self._board_state[rank][file] = None  # set pos to None

    def get_loc_from_pos(self, pos):
        """ Helper method to translate pos strings to indices, in order to set and get occupants of the board state"""
        rank_index = int(pos[1:]) - 1
        file_index = self._files.index(pos[0])
        return (rank_index, file_index) # return [rank][file] tuple corresponding to pos in self._board_state

    def get_pos_from_loc(self, loc):
        """ Helper method to translate a (rank, file) tuple index into a position string"""
        rank_str = str(loc[0] + 1)
        file_str = str(self._files[loc[1]])
        return file_str + rank_str

    def get_piece_from_pos(self, pos):
        """ Returns the piece at pos, or None if pos is not occupied"""
        rank, file = self.get_loc_from_pos(pos)
        return self._board_state[rank][file]

    def get_general_pos(self, side):
        """Returns the position of the general on side. Side is a string passed as 'red' or 'black'."""
        return self._piece_state[ side[0] + "Ge"]

    def get_L_path(self, from_pos, to_pos):
        """ Returns an ordered list of [(position, occupant) tuples] from from_pos to to_pos along L path.
        Do not include current location in the list. Last item is to_pos."""
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        # Generate the max 8 possible L-path destinations from the start location. L-paths consist of 3 points:
        # a start_loc(not returned), an intermediate_loc one point orthogonal from start_loc, and a dest_loc
        # one point diagonal to intermediate_loc

        # Generate the 4 maximum intermediate locations are one unit in every ortho direction from start_loc
        loc_diffs_int = [(0,-1), (0,1), (1,0), (-1,0)] # permute one unit difference in rank and file directions
        # create a list of possible intermediate locations
        int_locs = [(from_rank + rank_diff, from_file + file_diff) for rank_diff, file_diff in loc_diffs_int]
        # filter any locs that are out of range
        int_locs = [(rank, file) for rank,file in int_locs
                    if 0 <= rank < len(self._ranks) and 0 <= file < len(self._files)]

        # A valid L path will continue to dest_loc along the ortho trajectory set by intermediate location.
        # That is, from start_loc to intermediate_loc, and from intermediate_loc to destination,
        # both moves increase in either rank or file by exactly one unit.
        # For any valid L-path, there is only one intermediate location that corresponds to destination.
        # Find the intermediate location corresponding to destination.
        int_pos = None
        for int_rank, int_file in int_locs:
            if from_rank - int_rank == int_rank - to_rank: # both ranks increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))
            elif from_file - int_file == int_file - to_file: # both files increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))

        if int_pos:
            try_dest = self.get_diagonal_path(int_pos, to_pos) # find a diagonal, if any from int to dest

        if int_pos and try_dest:           # valid diagonal found, append both to path
            path.append( (int_pos, self.get_piece_from_pos(int_pos)) )
            path += try_dest

        return path # path will be a valid L path, or empty if no valid L path

    def get_diagonal_path(self, from_pos, to_pos):
        """ Returns an ordered list of [ (location, occupant) tuples] from from_pos to to_pos along diagonal.
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

        # determine which direction we are iterating over the ranks and files
        flip_file = file_diff < 0
        flip_rank = rank_diff < 0

        # get the ranges over the ranks and files in the correct order of iteration
        if flip_rank:
            rank_range = range(from_rank - 1, to_rank - 1, - 1)
        else:
            rank_range = range(from_rank + 1, to_rank + 1)

        if flip_file:
            file_range = range(from_file -1, to_file - 1, -1)
        else:
            file_range = range(from_file + 1, to_file + 1)

        # generate the positions along diagonal by pairing rank range and file range
        diag_positions = zip(rank_range, file_range) # zip([0,1,2] , [0,1,2]) will give (0,0), (1,1), (2,2)
        for rank, file in diag_positions:
            pos = self.get_pos_from_loc((rank,file))
            path.append((pos, self.get_piece_from_pos(pos)))  # add the position and occupant at pos to the path
        return path

    def get_ortho_path(self, from_pos, to_pos):
        """Returns ordered list of [ (location, occupant) tuples] from from_pos to to_pos along ortho.
        Do not include current location in the list. Last item is to_pos. """

        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []
        flip_dir = False

        if from_rank != to_rank and from_file != to_file: # return empty path if to_pos is not ortho to from_pos
            return path

        # determine which direction we are iterating over the ranks and files
        if to_rank < from_rank:
            flip_dir = True
        if to_file < from_file:
            flip_dir = True

        # get the ranges over the ranks and files in the correct order of iteration
        if from_rank == to_rank and not flip_dir:
            file_range = range(from_file + 1, to_file + 1)
        elif from_rank == to_rank and flip_dir:
            file_range = range(from_file - 1, to_file - 1, -1)
        elif from_file == to_file and not flip_dir:
            rank_range = range(from_rank + 1, to_rank + 1)
        elif from_file == to_file and flip_dir:
            rank_range = range(from_rank - 1, to_rank - 1, -1)

        if from_rank == to_rank:   # keep rank constant, add all file steps in range
            for file in file_range: # get positions along rank from [from_file +1, to_file]
                this_pos = self.get_pos_from_loc((to_rank, file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant)) # add position and occupant to path

        elif from_file == to_file: # keep file constant, add all rank steps in range
            for rank in rank_range: # get positions along file from [from_rank + 1, to_rank]
                this_pos = self.get_pos_from_loc((rank, to_file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant)) # add position and occupant to path
        return path

    def get_ranks(self):
        """Returns an ordered array of the Board's rank letters, 'a' through 'i'."""
        return self._ranks

    def get_files(self):
        """Returns an ordered array of the Board's file numbers, '1' through '10'."""
        return self._files

    def get_available_positions(self, side):
        """ Returns a list of all positions that are unoccupied, or occupied by side's foe. Includes (at least)
        all possible locations that a Piece on side could occupy to on next move. Side is passed as 'red' or 'black'. """
        return_pos = []
        for file_str in self._files:
            for rank_str in self._ranks:
                occupant = self.get_piece_from_pos(file_str + rank_str)
                if occupant is None or occupant.get_side() != side:
                    return_pos.append(file_str + rank_str)
        return return_pos