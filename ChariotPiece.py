from Piece import Piece

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