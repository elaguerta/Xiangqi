from Board import Board
from Player import Player

class XiangqiGame():
    def __init__(self):
        self._board = Board()                               # initialize board
        self._red_player = Player('red', self._board)       # initialize red player, with this game's board
        self._black_player = Player('black', self._board)   # initialize black player, with this game's board
        self._turn = 'red'         # red goes first
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'RED_WON', or 'BLACK_WON" """
        pass

    def get_player(self, player):
        """return the Player represented by player string - 'red' or 'black'"""
        if player == 'red':
            return self._red_player
        if player == 'black':
            return self._black_player

    def is_in_check(self, side):
        """
        Determines if color side is in check.
        :param side: 'red' or 'black'
        :return: True if that side is in check, False otherwise
        """
        # get the position of this player's general
        player = self.get_player(side)
        general_pos = player.get_general_pos()
        # ask the opponent if they can attack the general's position
        opponent = self.get_opponent(side)
        return opponent.can_attack(general_pos)

    def is_in_checkmate(self, player):
        """ returns True if player is in checkmate. Player is in checkmate if there is no one move that can defend against
        all current checks"""
        pass

    def defend_check(self, player, attack_piece, path):
        """ returns a (from_pos, to_pos) move that would defend player from attack piece. Returns False if no such move.
        Attack_piece is a piece that is placing the other general in check.
        Path is the ordered list of [ (location, occupant) tuples]
        from attack piece to the other general """

        defending_pieces = self.get_pieces(player)
        target = attack_piece.get_pos()

        # See if one of player's pieces can block this path
        # by occupying any position along path, including capture of the attack_piece at its current location
        for piece in defending_pieces:
            for pos, occupant in path:
                if piece.is_legal(pos):             # this piece can block or capture
                    return (piece.get_pos(), pos)   # return this piece's position and the position of block or capture

        # If attack piece is a cannon, there is the additional possibility of moving the piece that
        # acts as shield, if it belongs to player
        for pos, occupant in path:
            if occupant.get_side() == player:
                return True

        # we have exhausted all possibilities of block, capture, or disabling the attack_piece. Return False.
        return False

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
        try_move = self.get_player(self._turn).move(from_pos, to_pos)     # ask this turn's Player to attempt the move

        if not try_move:                            # if not successful, return False
            return False

        # If we got to this point, move succeeded, update the turn, update the game state, and return True
        self.update_turn()
        self.update_game_state()
        return True

    def get_pieces(self, player):
        """ returns subset of self._pieces that are on the side of player"""
        return {piece for piece in self._pieces if piece._side == player}

    def get_opponent(self, player):
        """ returns the opponent of player"""
        if player == 'red':
            return self._black_player
        elif player == 'black':
            return self._red_player

    def update_game_state(self):
        """ checks if there is a checkmate or stalemate and updates game state if so. Otherwise,
         does nothing """
        pass

    def update_turn(self):
        """ sets turn variables to next turn """
        if self._turn == 'red':
            self._turn = 'black'
        else:
            self._turn = 'red'

    def out_of_range(self, pos):
        """returns True if pos is beyond the limits of the board"""
        rank, file = pos[1:], pos[0]
        return rank not in self._board.get_ranks() or file not in self._board.get_files()