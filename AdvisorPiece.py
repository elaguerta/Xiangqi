from Piece import Piece

class AdvisorPiece(Piece):
    """ Instantiates an Advisor Piece
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