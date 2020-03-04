from GeneralPiece import GeneralPiece
from ChariotPiece import ChariotPiece
from SoldierPiece import SoldierPiece

class Player():

    def __init__(self, side, board):
        self._side = side   # 'black' or 'red'
        self._board = board
        self._pieces = set()

        # initialize general and save to an instance variable for easy access. add the general to the set of this
        # Player's pieces.
        self._general = (GeneralPiece(side, board))
        self._pieces.add(self._general)

        # initialize 2 chariot pieces
        self._pieces.add(ChariotPiece(side, board, 1))
        self._pieces.add(ChariotPiece(side, board, 2))

        # initialize 5 soldiers
        self._pieces.add(SoldierPiece(side, board, 1))
        self._pieces.add(SoldierPiece(side, board, 2))
        self._pieces.add(SoldierPiece(side, board, 3))
        self._pieces.add(SoldierPiece(side, board, 4))
        self._pieces.add(SoldierPiece(side, board, 5))

        # place all pieces in initial positions
        for piece in self._pieces:
            self._board.place_piece(piece, piece.get_pos())

    def get_pieces(self):
        return self._pieces

    def get_general_pos(self):
        """ return the position of this player's general"""
        return self._general._pos

    def move(self, from_pos, to_pos):
        piece = self._board.get_piece_from_pos(from_pos)    # get the piece on from_pos
        if not piece:                                   # the from position is empty
            return False
        if piece.get_side() != self._side:             # the piece on the from position does not belong to this player
            return False
        # tell the piece to attempt the move, return the result

        return piece.move(to_pos)

    def can_attack(self, opp_general_pos):
        """true if this Player can attack a piece at opp_general_pos, False otherwise"""
        # if there is a legal move from any opposing piece to general_pos, return True
        for piece in self._pieces:
            if piece.is_legal(opp_general_pos):
                return True
        return False


