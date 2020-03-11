class Piece:
    """Creates Pieces. Superclass to all Piece types."""

    def __init__(self, side, board):
        self._board = board        # a Board object, passed by the Piece's Player
        self._side = side          # 'red' or 'black', passed by Player
        self._movement = None      # ortho, diagonal, or L shaped. This is tracked by children classes.
        self._path_length = None   # Updated by children classes depending on the Piece type.
        self._jumps = 0            # number of other pieces allowed to jump. Updated by CannonPiece when capturing.

        # save the opposing side as an instance variable, for convenience
        if self._side == 'red':
            self._opp = 'black'
        else:
            self._opp = 'red'

    def get_path(self, to_pos):
        """ Returns an ordered list of [ (location, occupant) tuples] from current pos to to_pos along
        self._movement pattern. Do not include current location in the list. Last item is to_pos.
        False if no such path to to_pos via self._movement pattern."""
        try_ortho = self._board.get_ortho_path(self._pos, to_pos)
        try_diag = self._board.get_diagonal_path(self._pos, to_pos)
        try_L_shaped = self._board.get_L_path(self._pos, to_pos)

        if self._movement == 'L-shaped' and try_L_shaped:
            return try_L_shaped
        if self._movement == 'ortho' and try_ortho:
            return try_ortho
        elif self._movement == 'diagonal' and try_diag:
            return try_diag
        else:
            return False

    def num_jumps(self, path):
        """Returns number of pieces that would be jumped along path"""
        jumps = 0
        for position,occupant in path[0:-1]: # look at every step except the last step in the path
            if occupant:     # Board returns the Piece at position, or None if position is not occupied
                jumps +=1
        return jumps

    def get_pos(self):
        """ Returns current pos"""
        return self._pos

    def set_pos(self, pos):
        """Set's piece's pos """
        self._pos = pos

    def is_legal(self, to_pos):
        """ Returns or True if the move to to_pos is legal based on Piece-level info.
        Returns False otherwise. Note that Pieces do not screen for illegal moves that result in check.
        Player() screens moves for any that would result in a check. """

        if self._pos == to_pos:             # do not allow moves that would not change the game state
            return False

        if self._pos == None:           # do not allow captured pieces to move
            return False

        occupant = self._board.get_piece_from_pos(to_pos)
        if occupant and occupant._side == self._side: # if the to_pos is occupied by a friend, return False
            return False

        try_path = self.get_path(to_pos)
        if not try_path:                            # return False if no path to to_pos
            return False

        if self._path_length:  # return False if path length is longer than the piece can move
            if len(try_path) > self._path_length:
                return False

        # return False if pieces jumped along path do not obey the piece's jump restrictions
        if self.num_jumps(try_path) != self._jumps:
            return False

        return True

    def move(self, to_pos):
        """ Moves a piece to to_pos if move is legal for this piece.
        Returns:
            If move is not legal, returns False.
            If move is legal and results in a capture, returns piece captured.
            If move is legal and does not result in a capture, returns True
        Side effects:
            Sets self._pos to to_pos.
            If captive, sets captive._pos to None.
            Sets self._board at to_pos to be occupied by piece.
            Sets self._board at the piece's previous position to None.

        Note that Pieces do not screen for illegal moves that result in check.
        Player screens moves for any that would result in a check.
        """

        if not self.is_legal(to_pos):  # Check piece-level conditions
            return False

        captive = self._board.get_piece_from_pos(to_pos)    # get the piece, if any, that would be captured by this move

        self._board.clear_pos(self._pos)                # tell Board to clear the Piece's old position
        self._board.place_piece(self, to_pos)           # tell the board that to_pos is occupied by this piece
        self._pos = to_pos                              # update this piece's position.

        if captive:
            self._board.clear_piece(captive)            # clear the captured piece from the board
            captive.set_pos(None)                       # captive sets its current position to None
            return captive                              # return the captive Piece if any

        # return True if move successful and no captive
        return True

    def reverse_move(self, from_pos, to_pos, captive = None):
        """ Reverses a move.
        Assumptions:
            Piece's current location must be to_pos.
            Captive, if any, is the Piece that was captured by the move.
            Move to be reversed was a legal move.
        Returns:
            Nothing
        Side effects:
            If captive, sets Board at to_pos to be occupied by captive and sets captive's position to to_pos.
            Sets Board at from_pos to this Piece.
            Updates this Piece's self._pos to from_pos """

        if isinstance(captive, Piece): # restore captive, if any
            self._board.place_piece(captive, to_pos)
            captive.set_pos(to_pos)
        else: # if no captive, tell Board to clear to_pos
            self._board.clear_pos(to_pos)

        self._board.place_piece(self, from_pos) # place this Piece on from_pos
        self._pos = from_pos # update this Piece's pos

    def get_possible_moves(self):
        """ Returns the set of all possible moves available to Piece.
        Includes moves legal at the Piece level. Does not filter for moves that would result in check for this side.
        Player is responsible for filtering moves that would result in check. """

        # get all positions that are empty or occupied by opponent
        possible_pos = self._board.get_available_positions(self._side)
        moves = set()
        if self._pos is not None:  # if this Piece has not been captured
            for pos in possible_pos:  # search through possible moves
                if self.is_legal(pos):  # if piece can legally move to pos, add move to possible moves
                    moves.add((self._pos, pos))
        # return the set of possible moves legal at the Piece level.
        # if no such moves, will return the empty set.
        return moves


    def get_side(self):
        """ Returns this Piece's side: 'red', or 'black'. """
        return self._side

    def get_jumps(self):
        """ Returns the number of jumps legal for this Piece."""
        return self._jumps

