from Piece import Piece

class ChariotPiece(Piece):
    def __init__(self, board, player, pos):
        super().__init__(board, player, pos)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped


    # def move(self, to_pos, board):
    #     """ moves and captures any distance orthogonally. may not jump over intervening pieces"""
    #     path = super.get_ortho_path(self, to_pos)
    #     if not ortho_path:
    #         return False

    def __repr__(self):
        return self._side[0] + "Ch"