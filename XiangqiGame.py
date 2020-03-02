from Board import Board
from ChariotPiece import ChariotPiece

class XiangqiGame():
    def __init__(self):
        self._board = Board()
        self._turn = 'red'          # red goes first

        # instantiate pieces
        self._pieces = set()

        # initialize chariot pieces, at files 'a' and 'i'
        self._pieces.add(ChariotPiece(self._board, 'red', 'a1'))
        self._pieces.add(ChariotPiece(self._board, 'black', 'a10'))
        self._pieces.add(ChariotPiece(self._board, 'red', 'i1'))
        self._pieces.add(ChariotPiece(self._board, 'black', 'i10'))

        # place all pieces in initial positions
        for piece in self._pieces:
            self._board.place_piece(piece, piece.get_pos())

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'RED_WON', or 'BLACK_WON" """
        pass

    def is_in_check(self, player):
        """
        Determines if player is in check.
        :param player: 'red' or black
        :return: True if that player is in check, False otherwise
        """
        pass

    def make_move(self, from_pos, to_pos):
        """

        :param from_pos: string representing the square moved from
        :param to_pos: string representing the square moved to
        :return: True if move is successful, and updates game state and board.
        False if move unsuccessful.

        If the square being moved from does not contain a piece belonging to the player whose turn it is, 
        or if the indicated move is not legal, or if the game has already been won, then it should just return False.  
        
        Otherwise it should make the indicated move, remove any captured piece, update the game state if necessary, 
        update whose turn it is, and return True.

        """
        if from_pos == to_pos:                  # do not allow a move that does not change the board state
            return False
        if self.out_of_range(from_pos) or self.out_of_range(to_pos):    # validate that positions are within range
            return False

        piece = self._board.get_piece_from_pos(from_pos)    # get the piece on from_pos
        if not piece:                                  # the from position is empty
            return False
        elif piece.get_side() != self._turn:             # the piece on the from position does not belong to this player
            return False
        else:
            return piece.move(to_pos)

    def out_of_range(self, pos):
        rank, file = pos[1:], pos[0]
        return rank not in self._board.get_ranks() or file not in self._board.get_files()