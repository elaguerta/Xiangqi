class Piece:
    def __init__(self, player, board):
        self._board = board
        self._side = player
        self._movement = None           # ortho, diagonal, or L shaped
        self._path_length = None    # depends on piece, default is unlimited
        self._jumps = 0                 # number of other pieces allowed to jump. Only cannon jumps - exactly 1 - piece.
        # save the opposing side as an instance variable
        if self._side == 'red':
            self._opp = 'black'
        else:
            self._opp = 'red'

    def get_path(self, to_pos):
        """ ordered list of [ (location, occupant) tuples] from current pos to to_pos along bearing.
        Do not include current location in the list. Last item is to_pos.
        False if no such path along bearing"""
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
        """ returns number of pieces that would be jumped along path"""
        jumps = 0
        for position,occupant in path[0:-1]:        # look at every step except the last step in the path
            if occupant:
                jumps +=1
        return jumps

    def get_pos(self):
        """ returns current pos"""
        return self._pos

    def set_pos(self, pos):
        self._pos = pos
        return True

    def is_legal(self, to_pos):
        """ returns a legal path for the piece to move to to_pos, given the current state of the board,
        false otherwise"""
        if self._pos == to_pos:             # do not allow moves that would not change the game state
            return False

        if self._pos == None:           # do not allow captured pieces to move
            return False

        try_path = self.get_path(to_pos)

        if not try_path:                            # return False if no path to to_pos
            return False

        if self._path_length:  # return False if path length is longer than the piece can move
            if len(try_path) > self._path_length:
                return False
        # return False if pieces jumped along path do not obey the piece's restrictions
        if self.num_jumps(try_path) != self._jumps:
            return False
        return True

    def move(self, to_pos):
        """
        Moves a piece to to_pos if move is legal for this piece. If move is not legal, returns False.
        :param piece:  a Piece of any type
        :param to_pos: A position to move it to
        :return: Sets self._board at to_pos to be occupied by piece. Updates self._pos to to_pos.
        Sets self._board at the piece's previous position to None.
        """
        if not self.is_legal(to_pos):
            return False

        captive = self._board.get_piece_from_pos(to_pos)    # get the piece that would be captured by this move
        if captive and captive.get_side() == self._side:    # if the to_pos is occupied by a friend, return False
            return False

        # otherwise, make the move and return true
        prev_pos = self._pos
        if prev_pos:  # tell the board to clear the piece's current position
            self._board.clear_pos(prev_pos)
        self._board.place_piece(self, to_pos)           # tell the board that to_pos is occupied by this piece
        self._pos = to_pos                              # update this piece's self.
        if captive:
            self._board.clear_piece(captive)                # clear the captured piece from the board
            captive.set_pos(None)                       # captive sets its current position to None
            return captive                                  # return the captive if any
        return True

    def reverse_move(self, from_pos, to_pos, captive = None):
        """ Reverses a move. Piece's current location must be to_pos. Puts captive, if any, on to_pos.
        Puts piece on from_pos. Reversal is assumed to be legal."""
        # restore captive, if any

        if isinstance(captive, Piece):
            self._board.place_piece(captive, to_pos)
            captive.set_pos(to_pos)
        else:
            self._board.clear_pos(to_pos)

        self._board.place_piece(self, from_pos)
        self._pos = from_pos
        return True

    def get_possible_moves(self):
        """ gets all possible moves available to Piece"""
        possible_pos = self._board.get_available_positions(self._side)
        moves = set()

        if self._pos is not None:  # if piece has not been captured
            for pos in possible_pos:  # search through possible moves
                # if piece can legally move to pos, add move to possible moves
                if self.is_legal(pos):
                    moves.add((self._pos, pos))
        # if no such move, return False
        return moves


    def get_side(self):
        return self._side

    def get_jumps(self):
        return self._jumps

