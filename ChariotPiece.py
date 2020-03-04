from Piece import Piece

class ChariotPiece(Piece):
    chariot_postions = {
        'red': ['a1', 'i1'],
        'black': ['a10', 'i10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # keep track of this chariot by assigning it an ID equal to the lenght of possible positions for this side
        # then destructively popping a position from the class and assigning it to thiis Chariot
        self._id =  id_num
        self._pos = ChariotPiece.chariot_postions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ch" + str(self._id)