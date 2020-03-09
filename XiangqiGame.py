from Board import Board
from Player import Player
from Piece import Piece

class XiangqiGame():
    def __init__(self):
        self._board = Board()                               # initialize board
        self._red_player = Player('red', self._board)       # initialize red player, with this game's board
        self._black_player = Player('black', self._board)   # initialize black player, with this game's board
        self._turn = 'red'         # red goes first
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'RED_WON', or 'BLACK_WON" """
        return self._game_state

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
        if opponent.get_attacks(general_pos):
            return True
        return False

    def is_in_stalemate(self, side):
        player = self.get_player(side)
        opponent = self.get_opponent(side)
        if not player.has_available_move(opponent):
            return True
        return False

    def is_in_checkmate(self, side):
        """ returns True if this side's Player is in checkmate. Player is in checkmate if there is no one move that can
        defend against all current checks"""
        defender = self.get_player(side)
        attacker = self.get_opponent(side)
        defending_general = defender.get_general_pos()
        attack_list = attacker.get_attacks(defending_general)
        if attack_list:
            if not defender.defend_all_checks(attack_list):
                return True
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
        turn_player = self.get_player(self._turn)
        opp = self.get_opponent(self._turn)
        if self._game_state != 'UNFINISHED':    # if the game has already been won, return False
            return False
        if from_pos == to_pos:                  # do not allow a move that does not change the board state
            return False
        if self.out_of_range(from_pos) or self.out_of_range(to_pos):    # validate that positions are within range
            return False
        try_move = turn_player.move(from_pos, to_pos, opp)     # ask this turn's Player to attempt the move

        if not try_move:                            # if not successful, return False
            return False

        # If we got to this point, move succeeded, update the turn, update the game state, and return True
        self.update_turn()
        self.update_game_state()
        return True

    def get_opponent(self, player):
        """ returns the opponent of player"""
        if player == 'red':
            return self._black_player
        elif player == 'black':
            return self._red_player

    def update_game_state(self):
        """ checks if there is a checkmate or stalemate and updates game state if so. Otherwise,
         does nothing. Returns True """
        if self._turn == 'red':
            next_turn = 'black'
        else:
            next_turn = 'red'

        # check if most recent move has put the next player in checkmate or stalemate
        if self.is_in_checkmate(next_turn) or self.is_in_stalemate(next_turn):
            # update endgame conditions
            if self._turn == 'red':
                self._game_state = 'BLACK_WON'
            else:
                self._game_state = 'RED_WON'
        return True


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