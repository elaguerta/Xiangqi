from Piece import Piece

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
        self._pos = SoldierPiece.soldier_positions[player][id_num - 1] # keep track of positions used based on id number


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