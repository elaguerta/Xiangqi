from Piece import Piece

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