from Piece import Piece

class SoldierPiece(Piece):
    num_per_game = 10
    instances = 1

    def __init__(self, board, player, pos):
        super().__init__(board, player, pos)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped
        self._id = SoldierPiece.instances % SoldierPiece.num_per_game
        SoldierPiece.instances += 1
        self._movement = 'ortho'  #
        self._max_path_length = 1
        self._crossed_river = False

    def __repr__(self):
        return self._side[0] + "So" + str(self._id)

    def is_legal(self, to_pos):
        """ calls super().is_legal and then checks the additional restrictions on the soldier's movement:
        cannot retreat, can move and capture by advancing one point, can move and capture horizontally by
        one point after crossing river"""

        # check the conditions that are checked for all pieces
        if not super().is_legal(to_pos):
            return False

        to_rank, to_file = self._board.get_loc_from_pos(to_pos)
        from_rank, from_file = self._board.get_loc_from_pos(self._pos)

        # if the move is a retreat, return False
        # red retreats along the same file from a higher rank to a lower rank
        if from_file == to_file and self.__side == 'red' and to_rank < from_rank:
            return False
        # black retreats along the same file from a lower rank to a higher rank
        if from_file == to_file and self.__side == 'black' and to_rank > from_rank:
            return False

        # if the move is horizontal and the Soldier has not yet crossed the river, return false
        # if the rank is the same, the move is horizontal
        if to_pos[1:] == self._pos[1:] and not self._crossed_river:
            return False




    def move(self, to_pos):
        super().move(to_pos)        # move as usual
        # if red makes it to 6, or black makes it to 5, river was crossed. Set self._crossed_river to True
        if self._side == 'red' and to_pos[1:] == '6':
            self._crossed_river = True

        if self._side == 'black' and to_pos[1:] == '5':
            self._crossed_river = True

        return True