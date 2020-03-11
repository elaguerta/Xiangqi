from Piece import Piece

class CannonPiece(Piece):
    """ Instantiates a Cannon Piece
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
        self._pos = CannonPiece.cannon_postions[player][id_num - 1]  # keep track of positions used based on id number

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
