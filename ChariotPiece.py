import Piece

class ChariotPiece(Piece):
    def __init__(self, player, file):
        super.__init__(self, player)
        if player == 'red':
            self._pos = file + '1'            # chariots start on a1, i1 for red; a10, i10 for black
        elif player == 'black':
            self._pos == file + '10'

    def move(self, to_pos, board):
        """ moves and captures any distance orthogonally. may not jump over intervening pieces"""
        ortho_dir = super.get_ortho_dir(self, to_pos)
        if not ortho_dir:
            return False
        elif ortho_dir == 'file':
            file = to_pos[0]

