class Piece:
    def __init__(self, player):
        self._side = player
        self._pos = None

    def get_ortho_dir(self, to_pos):
        """ returns "file" if to_pos is ortho to the current position along a file, "rank" if to_pos is ortho to the
        piece's current position along a rank, False otherwise"""

        # the Game checks that the to_pos is not equal to the piece's current pos

        if self._pos[0] == to_pos[0]:            # check if file is equal
            return "file"
        elif self._pos[1] == to_pos[1]:         # check if rank is equal
            return "rank"
        else:
            return False

    def get_pieces_on_path(self, path, board):
        """
        :param path: an ordered list of positions beginning with from_pos and ending with to_pos
        :param board: the Board for the current game
        :return: a list of any pieces that occupy positions along the path
        """

