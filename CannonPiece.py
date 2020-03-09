from Piece import Piece

class CannonPiece(Piece):
    cannon_postions = {
        'red': ['b3', 'h3'],
        'black': ['b8', 'h8']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # keep track of this chariot by assigning it an ID equal to the lenght of possible positions for this side
        # then destructively popping a position from the class and assigning it to thiis Chariot
        self._id =  id_num
        self._pos = CannonPiece.cannon_postions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ca" + str(self._id)

    def is_legal(self, to_pos):
        # cannon requires screen piece for capture, friend or foe
        # if this move would result in a capture, temporarily set jumps to 1
        occupant = self._board.get_piece_from_pos(to_pos)
        if occupant and occupant.get_side() != self._side:
            self._jumps = 1
        result = super().is_legal(to_pos)           # call super with jumps updated if necessary
        self._jumps = 0                             # reset jumps to 0
        return result
