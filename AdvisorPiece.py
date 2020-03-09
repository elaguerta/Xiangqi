from Piece import Piece

class AdvisorPiece(Piece):
    advisor_positions = {
        'red': ['d1', 'f1'],
        'black': ['d10', 'f10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'diagonal'  # ortho, diagonal, or L shaped
        self._path_length = 1

        # assign a position.
        self._id = id_num
        self._pos = AdvisorPiece.advisor_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ad" + str(self._id)

    def is_legal(self, to_pos):
        # advisors must remain in castle
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False
        return super().is_legal(to_pos)