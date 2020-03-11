from Piece import Piece

class GeneralPiece(Piece):
    """ Creates GeneralPieces
        general_positions is a class variable, a dictionary of initial positions keyed by player color """
    general_positions = {'red':'e1', 'black':'e10'}

    def __init__(self, side, board):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
                passed as arguments by Player. """
        super().__init__(side, board)
        self._movement = 'ortho'  # generals move ortho
        self._path_length = 1  # generals move one point
        self._pos = GeneralPiece.general_positions[side] # assign a position based on side

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ge".
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ge"

    def is_legal(self, to_pos):
        """ Calls super().is_legal and then checks the additional parameters of the general's movement:
        the general must stay in the palace, flying general move may be executed """

        # check if this general could capture enemy general at to_pos via flying general
        flying_general_flag = self.is_flying_general(to_pos)

        if flying_general_flag:     # if flying general is possible, temporarily lift path length restriction
            self._path_length = None

        # check Piece.is_legal (with max path length restriction lifted if flying general is possible)
        # if it's not legal for a Piece.is_legal() reason, reset path length and return False
        if not super().is_legal(to_pos):
            self._path_length = 1    # reset path length
            return False

        # If we get to this point, all Piece.is_legal() conditions are met.
        # In the case that flying general isn't possible, check also that the general remains in the castle.
        # If not, reset the path length and return False
        if not flying_general_flag and to_pos not in (self._board.get_castle_spots(self._side)):
            self._path_length = 1
            return False

        # Move is legal. Reset path length and return True
        self._path_length = 1
        return True

    def is_flying_general(self, to_pos):
        """ Helper method to self.is_legal.
        Returns True if this general could capture enemy general at to_pos via flying general"""
        other_gen_pos = self._board.get_general_pos(self._opp)  # get the other general's position
        if other_gen_pos == to_pos and other_gen_pos[0] == self._pos[0]:  # if both generals on the same file
            path_to_gen = self.get_path(other_gen_pos)            # get ortho path to general
            if self.num_jumps(path_to_gen) == 0:        # if no intervening pieces, flying general is possible
                return True
