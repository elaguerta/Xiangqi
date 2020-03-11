from Piece import Piece

class AdvisorPiece(Piece):
    """ Instantiates an Advisor Piece"""

    # advisor_positions is a class variable, a dictionary of initial positions keyed by player color
    advisor_positions = {
        'red': ['d1', 'f1'],
        'black': ['d10', 'f10']
    }

    def __init__(self, player, board, id_num):
        """ Initializes an advisor piece. The player who owns the piece, the board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(player, board) # call the Piece init with player and board
        self._movement = 'diagonal'  # advisors can move diagonally
        self._path_length = 1       # advisors can only move one location

        # assign a position.
        self._id = id_num      # passed as argument, 1 or 2
        self._pos = AdvisorPiece.advisor_positions[player][id_num - 1] # keep track of positions used
        # and available in the Advisor class based on id number

    def __repr__(self):
        """return an informative string about this piece ["r" or "b"] + "Ad" + [id_num for this specific piece], unique
         for every piece in a Game """
        return self._side[0] + "Ad" + str(self._id)

    def is_legal(self, to_pos):
        """ check Piece legal conditions for moving to to_pos, with the additional restriction that the advisor
        remain in the castle"""

        # to_pos must be a castle spot for this piece's side
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False
        # if it is a castle spot, check that all other legal conditions for Piece hold
        return super().is_legal(to_pos)