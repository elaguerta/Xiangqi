from Piece import Piece

class ChariotPiece(Piece):
    num_per_game = 20
    id_generator = (str(num) for num in range(1, num_per_game + 1))

    def __init__(self, board, player, pos):
        super().__init__(board, player, pos)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped
        self._id = next(ChariotPiece.id_generator)

    def __repr__(self):
        return self._side[0] + "Ch" + self._id