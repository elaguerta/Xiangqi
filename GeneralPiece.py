from Piece import Piece

class GeneralPiece(Piece):
    general_positions = {'red':'e1', 'black':'e10'}
    def __init__(self, player, board):
        super().__init__(player, board)
        self._movement = 'ortho'  #
        self._max_path_length = 1
        self._pos = GeneralPiece.general_positions[player]

    def __repr__(self):
        return self._side[0] + "Ge"

    def is_legal(self, to_pos):
        """ calls super().is_legal and then checks the additional parameters of the general's movement:
        the general must stay in the palace, flying general move may be executed """
        flying_general_flag = self.is_flying_general(to_pos)

        if flying_general_flag:     # if flying general is possible, temporarily lift path length restriction
            self._max_path_length = None

        # check Piece.is_legal, with max path length restriction lifted if flying general is possible
        if not super().is_legal(to_pos):
            return False

        # in the case that flying general isn't possible, check that the general remains in the castle
        if not flying_general_flag and to_pos not in (self._board.get_castle_spots(self._side)):
            return False

        if flying_general_flag:      # reset path restriction if necessary
            self._max_path_length = 1

        return True

    def is_flying_general(self, to_pos):
        """ helper method to is_legal. Returns True if this general's move to to_pos is a flying general move"""
        other_gen_pos = self._board.get_general_pos(self._opp)  # get the other general's position
        if other_gen_pos == to_pos and other_gen_pos[0] == self._pos[0]:  # if both generals on the same file
            path_to_gen = self.get_path(other_gen_pos)            # get ortho path to general
            if self.num_jumps(path_to_gen) == 0:        # if no intervening pieces, flying general is possible
                return True
