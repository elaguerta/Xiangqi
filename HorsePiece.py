from Piece import Piece

class HorsePiece(Piece):
    horse_positions = {
        'red': ['b1', 'h1'],
        'black': ['b10', 'h10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'L-shaped'  # ortho, diagonal, or L shaped
        self._path_length = 2   # one point ortho, one point diagonal

        # assign a position.
        self._id = id_num
        self._pos = HorsePiece.horse_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ho" + str(self._id)