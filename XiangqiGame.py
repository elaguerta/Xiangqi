from Board import Board
from ChariotPiece import ChariotPiece
from GeneralPiece import GeneralPiece

class XiangqiGame():
    def __init__(self):
        self._board = Board()
        self._turn = 'red'          # red goes first
        self._next_turn = 'black'   # for easy toggling between turns
        self._game_state = 'UNFINISHED'

        # instantiate pieces
        self._pieces = set()

        # initialize generals, at file e
        self._pieces.add(GeneralPiece(self._board, 'red', 'e1'))
        self._pieces.add(GeneralPiece(self._board, 'black', 'e10'))

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
        if self._game_state != 'UNFINISHED':    # if the game has already been won, return False
            return False
        if from_pos == to_pos:                  # do not allow a move that does not change the board state
            return False
        if self.out_of_range(from_pos) or self.out_of_range(to_pos):    # validate that positions are within range
            return False

        piece = self._board.get_piece_from_pos(from_pos)    # get the piece on from_pos
        if not piece:                                   # the from position is empty
            return False
        if piece.get_side() != self._turn:             # the piece on the from position does not belong to this player
            return False

        # try to make the move
        try_move = piece.move(to_pos)
        if not try_move:                            # if not successful, return False
            return False

        # if move is successful, update the turn
        self._turn, self._next_turn = self._next_turn, self._turn
        # update the game state
        self.update_game_state()

        return True

    def update_game_state(self):
        """ checks if there is a checkmate or stalemate and updates game state if so. Otherwise,
         does nothing """
        pass


    def out_of_range(self, pos):
        rank, file = pos[1:], pos[0]
        return rank not in self._board.get_ranks() or file not in self._board.get_files()