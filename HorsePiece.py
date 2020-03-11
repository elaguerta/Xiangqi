from Piece import Piece

class HorsePiece(Piece):
    """Creates HorsePieces
            horse_positions is a class variable, a dictionary of initial positions keyed by player color
            Two HorsePieces are created by a call to Player.__init__()."""
    horse_positions = {
        'red': ['b1', 'h1'],
        'black': ['b10', 'h10']
    }

    def __init__(self, side, board, id_num):
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