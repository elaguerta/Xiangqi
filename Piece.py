class Piece:
    def __init__(self, board, player, pos):
        self._board = board
        self._side = player
        self._pos = pos
        self._movement = None           # ortho, diagonal, or L shaped
        self._max_path_length = None    # depends on piece, default is unlimited
        self._jumps = 0                 # number of other pieces allowed to jump. Only cannon jumps - exactly 1 - piece.
        # save the opposing side as an instance variable
        if self._side == 'red':
            self._opp = 'black'
        else:
            self._opp = 'red'

    def get_path(self, bearing, to_pos):
        """ ordered list of [ (location, occupant) tuples] from current pos to to_pos along bearing.
        Do not include current location in the list. Last item is to_pos.
        False if no such path along bearing"""
        to_rank, to_file = (to_pos[1:], to_pos[0])
        from_rank, from_file = (self._pos[1:], self._pos[0])
        if bearing == 'ortho' and (to_rank != from_rank and to_file != from_file):
            return False
        else:
            return self._board.get_ortho_path(self._pos, to_pos)

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

    def is_legal(self, to_pos):
        """ returns True if it is legal for the piece to move to to_pos, given the current state of the board,
        false otherwise"""
        if self._pos == to_pos:             # do not allow moves that would not change the game state
            return False

        try_path = self.get_path(self._movement, to_pos)

        if not try_path:                            # return False if no path to to_pos
            return False

        if self._max_path_length:  # return False if path length is longer than the piece can move
            if len(try_path) > self._max_path_length:
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
        prev_pos = self._pos
        if prev_pos:                                    # tell the board to clear the piece's current position
            self._board.clear_pos(prev_pos)
        captive = self._board.get_piece_from_pos(to_pos)    # get the piece that would be captured by this move
        if captive and captive.get_side() == self._side:    # if the to_pos is occupied by a friend, return False
            return False
        self._board.place_piece(self, to_pos)           # tell the board that to_pos is occupied by this piece
        self._pos = to_pos                              # update this piece's self._pos
        self._board.clear_piece(captive)                # clear the captured piece from the board
        return True

    def get_side(self):
        return self._side

    def get_pos(self):
        return self._pos

    def get_jumps(self):
        return self._jumps

