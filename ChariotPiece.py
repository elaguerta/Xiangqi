from Piece import Piece

class ChariotPiece(Piece):
    num_per_game = 4
    instances = 1

    def __init__(self, board, player, pos):
        super().__init__(board, player, pos)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped
        self._id = ChariotPiece.instances % ChariotPiece.num_per_game
        ChariotPiece.instances += 1

    def __repr__(self):
        return self._side[0] + "Ch" + str(self._id)