from Piece import Piece

class ElephantPiece(Piece):
    elephant_positions = {
        'red': ['c1', 'g1'],
        'black': ['c10', 'g10']
    }
    legal_ranks = {
        'red': {'1','2','3','4','5'},
        'black': {'10','9','8','7','6'}
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'diagonal'  # ortho, diagonal, or L shaped
        self._path_length = 2

        # assign a position.
        self._id = id_num
        self._pos = ElephantPiece.elephant_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "El" + str(self._id)

    def is_legal(self, to_pos):
        return super().is_legal(to_pos) and to_pos[1:] in ElephantPiece.legal_ranks[self._side]