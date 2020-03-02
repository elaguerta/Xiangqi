from Piece import Piece

class GeneralPiece(Piece):
    def __init__(self, board, player, pos):
        super().__init__(board, player, pos)
        self._movement = 'ortho'  #
        self._max_path_length = 1
        self._jumps = 0

    def __repr__(self):
        return self._side[0] + "Ge"

    def is_legal(self, to_pos):
        """ calls super().is_legal and then checks the additional restrictions on the general's movement:
        the general must stay in the palace, and the generals cannot "see" each other """

        # check the typical conditions for all pieces
        if not super().is_legal(to_pos):
            return False

        # check that the general remains in the castle
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False

        #check that to_pos would not allow the generals to "see" each other. This means two generals along the same
        #file with no intervening pieces.

        #get the other general's position
        other_gen_pos = self._board.get_general(self._opp)
        if other_gen_pos[0] == self._pos[0]:             # if both generals on the same file, get the ortho path
            path_to_gen = self.get_path('ortho', other_gen_pos)
            if self.num_jumps(path_to_gen) == 0:        # if no intervening pieces
                return False

        return True
