# Author: Elaine Laguerta
# Date: 11 March 2020
# Description: Portfolio project for CS162 W2020.
# Implements a two-player version of Xiangqi, Chinese chess.
# Supports checking for legal moves based on specific piece type, and disallows moves that place one's self in check.
# Supports stalemate and checkmate endgames.
# Does not implement perpetual checks or chasing endgames.

class XiangqiGame():
    """ Creates Xiangqi Games
    Language note:  'side' refers to a player side of interest, and is string that may be 'red' or 'black'.
    'player' is used to refer to Player objects."""

    def __init__(self):
        self._board = Board()  # initialize board
        self._red_player = Player('red', self._board)  # initialize red player, with this game's board
        self._black_player = Player('black', self._board)  # initialize black player, with this game's board
        self._turn = 'red'  # red goes first
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'RED_WON', or 'BLACK_WON" """
        return self._game_state

    def get_player(self, side):
        """Return the Player represented by side string: 'red' or 'black'"""
        if side == 'red':
            return self._red_player
        if side == 'black':
            return self._black_player

    def get_turn(self):
        """ Return the current turn: 'red' or 'black' """
        return self._turn

    def is_in_check(self, side):
        """ True if that side is in check, False otherwise """

        # get the position of this player's general
        player = self.get_player(side)
        general_pos = player.get_general_pos()
        # ask the opponent if they can attack the general's position
        opponent = self.get_opponent(side)
        if opponent.get_attacks(general_pos):
            return True
        return False

    def is_in_stalemate(self, side):
        """Return True if side is in stalemate"""
        player = self.get_player(side)
        opponent = self.get_opponent(side)
        if player.has_available_move(opponent):  # if side has an available move against opponent, return False
            return False
        return True

    def is_in_checkmate(self, side):
        """ returns True if this side's Player is in checkmate. Player is in checkmate if there is no one move that can
        defend against all current checks"""

        defender = self.get_player(side)
        attacker = self.get_opponent(side)
        defending_general = defender.get_general_pos()
        attack_list = attacker.get_attacks(defending_general)  # get all attacks against defending geenral

        if attack_list:  # ask defender if it can defend all checks with one move. If so, return True.
            if not defender.defend_all_checks(attack_list, attacker):
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
        if self._game_state != 'UNFINISHED':  # if the game has already been won, return False
            return False

        if from_pos == to_pos:  # do not allow a move that does not change the board state
            return False

        if self.out_of_range(from_pos) or self.out_of_range(to_pos):  # validate that positions are within range
            return False

        # allow the turn to proceed
        turn_player = self.get_player(self._turn)
        opp = self.get_opponent(self._turn)
        try_move = turn_player.move(from_pos, to_pos, opp)  # ask this turn's Player to attempt the move
        if not try_move:  # if not successful, return False
            return False

        # If we got to this point, move succeeded. Update the game state, flip the turn, and return True
        self.update_game_state()
        self.update_turn()
        return True

    def get_opponent(self, side):
        """ Returns the opponent of player"""
        if side == 'red':
            return self._black_player
        elif side == 'black':
            return self._red_player

    def update_game_state(self):
        """ Checks if there is a checkmate or stalemate and updates game state if so. Otherwise,
         does nothing. Returns True """

        # Endgame result depends on who would move next
        if self._turn == 'red':
            next_turn = 'black'
        else:
            next_turn = 'red'

        # check if most recent move has put the next player in checkmate or stalemate
        if self.is_in_checkmate(next_turn):  # if next player is in checkmate, this player won
            if self._turn == 'red':
                self._game_state = 'RED_WON'
            else:
                self._game_state = 'BLACK_WON'
            print("CHECKMATE", self._game_state)
            return

        if self.is_in_stalemate(next_turn):  # if next player is in checkmate, this player won
            # update endgame conditions
            if self._turn == 'red':
                self._game_state = 'RED_WON'
            else:
                self._game_state = 'BLACK_WON'
            print("STALEMATE", self._game_state)
            return

    def update_turn(self):
        """ Sets turn variables to next turn """
        if self._turn == 'red':
            self._turn = 'black'
        else:
            self._turn = 'red'

    def out_of_range(self, pos):
        """Returns True if pos is beyond the limits of the board"""
        rank, file = pos[1:], pos[0]
        return rank not in self._board.get_ranks() or file not in self._board.get_files()

class Player():
    """Creates Players"""
    def __init__(self, side, board):
        """ Initializes a Player with side = 'red' or 'black', and a Board object. Side and Board are passed
        by Game objects. """
        self._side = side       # 'black' or 'red'
        self._board = board     # the Board passed by the Game object
        self._pieces = set()    # a set of this Player's Pieces

        # Initialize general and save to an instance variable for easy access. Add the general to the set of this
        # Player's pieces.
        self._general = (GeneralPiece(side, board))
        self._pieces.add(self._general)

        # Create all other pieces and add them to self._pieces. Numbers are passed
        # to index each piece class's locations, and to give each piece a unique identifier.

        # initialize and add 2 Advisor Pieces
        self._pieces.add(AdvisorPiece(side, board, 1))
        self._pieces.add(AdvisorPiece(side, board, 2))

        # initialize and add 2 Elephant pieces
        self._pieces.add(ElephantPiece(side, board, 1))
        self._pieces.add(ElephantPiece(side, board, 2))

        # initialize and add 2 Horse pieces
        self._pieces.add(HorsePiece(side, board, 1))
        self._pieces.add(HorsePiece(side, board, 2))

        # initialize and add 2 chariot pieces
        self._pieces.add(ChariotPiece(side, board, 1))
        self._pieces.add(ChariotPiece(side, board, 2))

        # initialize and add 2 cannon pieces
        self._pieces.add(CannonPiece(side, board, 1))
        self._pieces.add(CannonPiece(side, board, 2))

        # initialize and add 5 soldiers
        self._pieces.add(SoldierPiece(side, board, 1))
        self._pieces.add(SoldierPiece(side, board, 2))
        self._pieces.add(SoldierPiece(side, board, 3))
        self._pieces.add(SoldierPiece(side, board, 4))
        self._pieces.add(SoldierPiece(side, board, 5))

        # place all pieces on Board at their in initialized positions
        for piece in self._pieces:
            self._board.place_piece(piece, piece.get_pos())

    def get_defense_moves(self, attack_piece, path, opp):
        """Returns a set of {(from_pos, to_pos)} moves that would defend Player's general from attack_piece along path.
        Returns the empty set if no such move.
        Attack_piece is a piece that is placing this Player's general in check. Path is the ordered list of
        [ (location, occupant) tuples] from attack piece to the other general """

        defense_moves = set()

        # See if one of Player's pieces, including general, can capture attack_piece at its current location
        for piece in self._pieces:
            if piece.is_legal(attack_piece.get_pos()):
                defense_moves.add((piece.get_pos(), attack_piece.get_pos()))

        # See if one of Player's pieces, can block this attack by occupying any position along path
        for piece in self._pieces:
            for pos, occupant in path:
                if piece.is_legal(pos):             # this piece can block or capture
                    defense_moves.add((piece.get_pos(), pos))  # add the move to the set of defense moves

        # Only Cannons have occupants along their attack path, and they have exactly one occupant along the path,
        # called the 'screen'. If the screen piece belongs to Player, Player can defend against Cannon by
        # moving the 'screen' from the path

        for pos, occupant in path:
            if occupant in self._pieces:
                # fix this later: need to add all possible legal moves for screen piece away from path
                # for now, save a tuple with from_position, 'screen piece' flag
                defense_moves = defense_moves.union(occupant.get_possible_moves())

        # filter defense moves and remove any that leave general in check
        remove_moves = set()
        for from_pos, to_pos in defense_moves:
            piece = self._board.get_piece_from_pos(from_pos)
            if self.puts_self_in_check(piece, to_pos, opp):
                remove_moves.add((from_pos, to_pos))

        # we have exhausted all possibilities of block, capture, or disabling the attack_piece. Return the resulting
        # set of moves
        return defense_moves - remove_moves

    def defend_all_checks(self, attackers, opp):
        """ Returns a set of moves that would defend Player's general from all checks in parameter
        attackers. Returns empty set if no such move.
        The parameter attackers is a list of (attack_pieces, paths) that comprises all current checks against Player"""

        # initialize set to the first set of defense moves against the first attack, then keep intersecting with each
        # subsequent set of defense moves until attackers list is exhausted
        attack_piece, path = attackers[0]
        # returns a set of defense moves against the first attack in the list

        defense_moves = self.get_defense_moves(attack_piece, path, opp)
        if defense_moves:
            for index in range(1, len(attackers)):
                attack_piece, path = attackers[index]
                # intersect the set of defense moves against this attack with the previous set
                defense_moves = defense_moves.intersection(self.get_defense_moves(attack_piece, path, opp))
        return defense_moves  # defense moves contains the set of moves that can defend all checks in attackers list



    def puts_self_in_check(self, piece, to_pos ,opp):
        """ Returns True of a move of piece to to_pos would put self in check"""

        from_pos = piece.get_pos()  # save piece's previous position
        try_move = piece.move(to_pos) #ask the piece to try the move

        # ask the opponent to examine results of move for attacks on this Player's general
        resulting_checks = opp.get_attacks(self.get_general_pos())

        # now tell the piece to reverse the move. try_move will be assigned the captive, if any
        if isinstance(try_move, Piece): # pass the captive if there was one
            piece.reverse_move(from_pos, to_pos, try_move)
        elif try_move: # if not, don't pass the captive. Reverse_move() will use a default argument of None for captive.
            piece.reverse_move(from_pos, to_pos)

        if resulting_checks: # if there were any checks resulting from the move, return True
            return True

        return False

    def get_general_pos(self):
        """ Return the position of this player's general"""
        return self._general._pos

    def move(self, from_pos, to_pos, opp):
        """ Calls Piece.move() if move is possible and move does not put Player's general in check.
        Returns the result of the call to Piece.move()"""
        piece = self._board.get_piece_from_pos(from_pos)    # get the piece on from_pos.

        if not piece:                                   # If not piece at from_pos, return False
            return False

        if piece not in self._pieces:     # the piece on the from_pos does not belong to this player, return False
            return False

        if self.puts_self_in_check(piece, to_pos, opp): # If the the move would result in a check on this player
            return False

        # Otherwise, tell the piece to attempt the move, return the result
        try_move = piece.move(to_pos)
        return try_move

    def get_attacks(self, opp_general_pos):
        """Returns a list of (attacker, path) tuples,
         for any piece of this Player's that has a shot at the opposing general's position. Returns an empty list if
         no such attack."""
        attackers = []
        for piece in self._pieces: # for each of this Player's pieces
            # if the piece has a shot at the other general
            if piece.get_pos() is not None and piece.is_legal(opp_general_pos):
                path = piece.get_path(opp_general_pos) # get the path to the opposing general
                attackers.append((piece,path)) # save this piece and the attack path
        return attackers

    def has_available_move(self, opponent):
        """ Returns a set of this Player's available moves against opponent, or False if there are no such moves.
        Available moves are any legal moves that would not result in placing this Player in check."""
        possible_moves = set()
        remove_moves = set()
        for piece in self._pieces:      # get all possible moves for all pieces
            piece_moves = piece.get_possible_moves()
            possible_moves = possible_moves.union(piece_moves)
            for from_pos, to_pos in piece_moves:   # find any move that would place self in check
                if self.puts_self_in_check(piece, to_pos, opponent):
                    remove_moves.add((from_pos, to_pos))
        possible_moves = possible_moves - remove_moves # remove the moves that would result in self check
        if possible_moves:
            return possible_moves
        return False

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

class AdvisorPiece(Piece):
    """ Creates AdvisorPieces
    Advisor_positions is a class variable, a dictionary of initial positions keyed by player color
    Two Advisor pieces are created by a call to Player.__init__(), one for each of the two positions
    per side."""
    advisor_positions = {
        'red': ['d1', 'f1'],
        'black': ['d10', 'f10']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board) # call the Piece init with side and board
        self._movement = 'diagonal'  # Advisors can move diagonally
        self._path_length = 1       # Advisors can only move one point

        # Assign a position from Advisor Piece.
        self._id = id_num      # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = AdvisorPiece.advisor_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ad" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ad" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Advisor to move to to_pos. Checks Piece.is_legal() conditions,
        with additional restriction that Advisors remain in the castle."""

        # to_pos must be a castle spot for this piece's side
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False

        # if it is a castle spot, check that all other legal conditions for Piece hold
        return super().is_legal(to_pos)

class ElephantPiece(Piece):
    """Creates ElephantPieces
                elephant_positions is a class variable, a dictionary of initial positions keyed by player color
                Two ElephantPieces are created by a call to Player.__init__()."""
    elephant_positions = {
        'red': ['c1', 'g1'],
        'black': ['c10', 'g10']
    }
    # legal_ranks is a class variable, a set of ranks that elephants may occupy keyed by player side
    # Elephants cannot cross the river.
    legal_ranks = {
        'red': {'1','2','3','4','5'},
        'black': {'10','9','8','7','6'}
    }

    def __init__(self, side, board, id_num):
        """ Initializes an Elephant Piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'diagonal'  # Elephants move diagonal
        self._path_length = 2 # Elephants move 2 points

        # assign a position from ElephantPiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = ElephantPiece.elephant_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "El" + [id_num for this specific piece].
                        This is intended to be unique for every piece in a Game """
        return self._side[0] + "El" + str(self._id)

    def is_legal(self, to_pos):
        """ call Piece.is_legal() with additional restriction that Elephants stay within their legal ranks,
        i.e. they don't cross the river."""
        return super().is_legal(to_pos) and to_pos[1:] in ElephantPiece.legal_ranks[self._side]

class HorsePiece(Piece):
    """Creates HorsePieces
            horse_positions is a class variable, a dictionary of initial positions keyed by player color
            Two HorsePieces are created by a call to Player.__init__()."""
    horse_positions = {
        'red': ['b1', 'h1'],
        'black': ['b10', 'h10']
    }

    def __init__(self, side, board, id_num):
        """Initialize a Horse piece. Side is 'red' or 'black' Side, board, and id_num are passed as arguments
        by Player. """
        super().__init__(side, board)
        self._movement = 'L-shaped'  # Horses move L-shaped
        self._path_length = 2   # L-paths are length 2: one point ortho, one point diagonal

        # assign a position from HorsePiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = HorsePiece.horse_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ho" + [id_num for this specific piece].
                This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ho" + str(self._id)

class ChariotPiece(Piece):
    """Creates ChariotPieces
        chariot_positions is a class variable, a dictionary of initial positions keyed by player color
        Two ChariotPositions are created by a call to Player.__init__()."""
    chariot_postions = {
        'red': ['a1', 'i1'],
        'black': ['a10', 'i10']
    }

    def __init__(self, side, board, id_num):
        """ Initializes a chariot piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
                passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # assign a position from ChariotPiece
        self._id =  id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = ChariotPiece.chariot_postions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ch" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ch" + str(self._id)

class CannonPiece(Piece):
    """ Creates CannonPieces
        cannon_positions is a class variable, a dictionary of initial positions keyed by player color
        Two Cannon pieces are created by a call to Player.__init__()."""
    cannon_postions = {
        'red': ['b3', 'h3'],
        'black': ['b8', 'h8']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an advisor piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho'  # Cannons move ortho

        # Assign a position from CannonPiece
        self._id =  id_num  # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = CannonPiece.cannon_postions[side][id_num - 1]  # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "Ca" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "Ca" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Cannon to move to to_pos. Checks Piece.is_legal() conditions,
        with additional support for exactly 1 jump if move to to_pos would result in a capture."""

        # cannon requires screen piece for capture, friend or foe
        # if this move would result in a capture, temporarily set jumps to 1
        occupant = self._board.get_piece_from_pos(to_pos)  # get the potential capture
        if occupant and occupant.get_side() != self._side: # if the potential capture is a foe, must have exactly 1 jump
            self._jumps = 1
        result = super().is_legal(to_pos)           # call super with jumps updated if necessary
        self._jumps = 0                             # reset jumps to 0
        return result

class SoldierPiece(Piece):
    """Creates SoliderPieces
    soldier_positions is a class variable, a dictionary of initial positions keyed by player color
    Two SoldierPieces are created by a call to Player.__init__()."""

    soldier_positions = {
        'red': ['a4', 'c4', 'e4', 'g4', 'i4'],
        'black': ['a7', 'c7', 'e7', 'g7', 'i7']
    }

    def __init__(self, side, board, id_num):
        """ Initializes an soldier piece. The side ('red' or 'black'), the Board, and the id_num of this piece are
        passed as arguments. """
        super().__init__(side, board)
        self._movement = 'ortho' # soldiers move ortho
        self._path_length = 1
        self._crossed_river = False

        # assign a position from SoldierPiece
        self._id = id_num # id_num is passed as argument, by Player, and will be 1 or 2
        self._pos = SoldierPiece.soldier_positions[side][id_num - 1] # keep track of positions used based on id number

    def __repr__(self):
        """Return an informative label for this Piece: ["r" or "b"] + "So" + [id_num for this specific piece].
        This is intended to be unique for every piece in a Game """
        return self._side[0] + "So" + str(self._id)

    def is_legal(self, to_pos):
        """Returns True if it is legal for Soldier to move to to_pos. Checks Piece.is_legal() conditions,
        with additional restrictions on the soldier's movement:
        Soldier cannot retreat, solider cannot move horizontally until it has crossed river."""

        # Check Piece.is_legal() conditions
        try_path = super().is_legal(to_pos)
        if not try_path:
            return False

        to_rank, to_file = self._board.get_loc_from_pos(to_pos)
        from_rank, from_file = self._board.get_loc_from_pos(self._pos)

        # If the move is a retreat, return False
        # red retreats along the same file from a higher rank to a lower rank
        if from_file == to_file and self._side == 'red' and to_rank < from_rank:
            return False
        # black retreats along the same file from a lower rank to a higher rank
        if from_file == to_file and self._side == 'black' and to_rank > from_rank:
            return False

        # if the move is horizontal and the Soldier has not yet crossed the river, return false
        # if the rank is the same, the move is horizontal
        if to_pos[1:] == self._pos[1:] and not self._crossed_river:
            return False

        # if we made it this far, move is legal for the Soldier. Return True
        return True

    def move(self, to_pos):
        """ Calls Piece.move(), then tags on a check for whether the soldier has crossed the river."""
        move_result = super().move(to_pos)        # move as usual

        # if red makes it to 6, or black makes it to 5, river was crossed. Set self._crossed_river to True
        if self._side == 'red' and to_pos[1:] == '6':
            self._crossed_river = True

        if self._side == 'black' and to_pos[1:] == '5':
            self._crossed_river = True

        return move_result

class Board:
    """ Creates Boards for use by XiangqiGame, Players, and Pieces
    Language notes:
        'loc' refers to a [rank][file] location in memory of the 2D matrix that stores the board state
        'pos' refers to a '<file><rank>' string used throughout the project as an alias for locations
        'side' refers to a player side of interest, and is string that may be 'red' or 'black'.
        Elsewhere in the project, 'player' is used as a parameter name for Player objects."""

    def __init__(self):
        """ Creates a Board, receives no arguments. The Board tracks the state of Pieces with two instance variables:
        self._board_state, which is keyed by location, and self._pieces, which is keyed by Piece.
        self._board_state is a 2D array where indices are [rank][file] locations, and values are Piece objects, or None.
        self._pieces is a dictionary where each key is the unique string representation of a Piece on the Board,
        and values are that Piece's current position.
        The two representations are intended to be equivalent before and after every call to Piece.move() and
        Piece.reverse_move() """

        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']    # column letters, or ranks
        self._ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']   # row numbers, or files

        # store the set of all locations that comprise the castle spots for red
        self._red_castle_spots = {'d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3'}
        # store the set of all locations that comprise the castle spots for black
        self._black_castle_spots = {'d10', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8'}

        # initialize empty board
        self._board_state = [  # board state represented as a 2D array
            [ None for file in self._files] for rank in self._ranks  # initialize all positions to None
        ]

        self._piece_state = {} # dictionary of piece: pos pairs. When pieces are captured, value is set to None

    def get_castle_spots(self, side):
        """Returns the set of all positions that comprise the castle positions for side."""
        if side == 'red':
            return self._red_castle_spots
        elif side == 'black':
            return self._black_castle_spots
        else:
            return False

    def get_board_state(self):
        """ returns pointer to the 2D array that tracks the occupants of locations on the Board."""
        return self._board_state

    def display_board(self, num_spaces = 2):
        """ Displays the board to the console."""
        delim = ' ' * num_spaces        # number of spaces between each location in a rank
        print( (delim * 9), "BLACK")   # print black label, somewhat centered
        print(' ', delim, ("  " + delim).join(self._files))  # print letter files in order
        for rank in reversed(self._ranks):                      # print black side first, from rank 10 to rank 1
            rank_state = self._board_state[int(rank) - 1]
            if rank == '10':
                line = rank + ' ' * (num_spaces - 1)
            else:
                line = rank + delim
            for piece in rank_state:
                if piece is None:
                    line += '---' + delim
                else:
                    line += repr(piece)[:3] + delim # display first 3 chars of Piece's string representation, plus delim
            print(line)
        print(' ', delim, ("  " + delim).join(self._files))         # print letter files in order
        print(delim * 9, "RED") # print red label, somewhat centered
        print() # blank line

    def place_piece(self, piece, to_pos):
        """ Updates self._board_state and self._piece_state so that to_pos is occupied by piece.
        Note that Board has no access to Pieces.
        Piece is responsible for updating its own variable tracking its current position"""
        rank,file = self.get_loc_from_pos(to_pos) # translate the to_pos string to a [rank][file] index
        self._board_state[rank][file] = piece  # piece now occupies to_pos
        self._piece_state[str(piece)] = to_pos # update piece's position in self._piece_state dictionary
        return True

    def clear_piece(self, piece):
        """ Sets self._piece_state[piece] to None. Used for keeping track of captures.
        Note that this is not symmetrical with place_piece, since it does not affect self._board_state.
        This is because capturing a piece means that its previous location will be occupied by its captor."""
        self._piece_state[str(piece)] = None

    def clear_pos(self, pos):
        """ Sets pos to None. Used for clearing a pos when a piece moves away from pos"""
        rank, file = self.get_loc_from_pos(pos)
        self._board_state[rank][file] = None  # set pos to None

    def get_loc_from_pos(self, pos):
        """ Helper method to translate pos strings to indices, in order to set and get occupants of the board state"""
        rank_index = int(pos[1:]) - 1
        file_index = self._files.index(pos[0])
        return (rank_index, file_index) # return [rank][file] tuple corresponding to pos in self._board_state

    def get_pos_from_loc(self, loc):
        """ Helper method to translate a (rank, file) tuple index into a position string"""
        rank_str = str(loc[0] + 1)
        file_str = str(self._files[loc[1]])
        return file_str + rank_str

    def get_piece_from_pos(self, pos):
        """ Returns the piece at pos, or None if pos is not occupied"""
        rank, file = self.get_loc_from_pos(pos)
        return self._board_state[rank][file]

    def get_general_pos(self, side):
        """Returns the position of the general on side. Side is a string passed as 'red' or 'black'."""
        return self._piece_state[ side[0] + "Ge"]

    def get_L_path(self, from_pos, to_pos):
        """ Returns an ordered list of [(position, occupant) tuples] from from_pos to to_pos along L path.
        Do not include current location in the list. Last item is to_pos."""
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        # Generate the max 8 possible L-path destinations from the start location. L-paths consist of 3 points:
        # a start_loc(not returned), an intermediate_loc one point orthogonal from start_loc, and a dest_loc
        # one point diagonal to intermediate_loc

        # Generate the 4 maximum intermediate locations are one unit in every ortho direction from start_loc
        loc_diffs_int = [(0,-1), (0,1), (1,0), (-1,0)] # permute one unit difference in rank and file directions
        # create a list of possible intermediate locations
        int_locs = [(from_rank + rank_diff, from_file + file_diff) for rank_diff, file_diff in loc_diffs_int]
        # filter any locs that are out of range
        int_locs = [(rank, file) for rank,file in int_locs
                    if 0 <= rank < len(self._ranks) and 0 <= file < len(self._files)]

        # A valid L path will continue to dest_loc along the ortho trajectory set by intermediate location.
        # That is, from start_loc to intermediate_loc, and from intermediate_loc to destination,
        # both moves increase in either rank or file by exactly one unit.
        # For any valid L-path, there is only one intermediate location that corresponds to destination.
        # Find the intermediate location corresponding to destination.
        int_pos = None
        for int_rank, int_file in int_locs:
            if from_rank - int_rank == int_rank - to_rank: # both ranks increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))
            elif from_file - int_file == int_file - to_file: # both files increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))

        if int_pos:
            try_dest = self.get_diagonal_path(int_pos, to_pos) # find a diagonal, if any from int to dest

        if int_pos and try_dest:           # valid diagonal found, append both to path
            path.append( (int_pos, self.get_piece_from_pos(int_pos)) )
            path += try_dest

        return path # path will be a valid L path, or empty if no valid L path

    def get_diagonal_path(self, from_pos, to_pos):
        """ Returns an ordered list of [ (location, occupant) tuples] from from_pos to to_pos along diagonal.
        Do not include current location in the list. Last item is to_pos. """
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        if from_rank == to_rank or from_file == to_file: # return empty path if positions are ortho to each other
            return path

        rank_diff = to_rank - from_rank
        file_diff = to_file - from_file
        if abs(rank_diff) != abs(file_diff): # return empty path if horizontal distance does not equal vertical distance
            return path

        # determine which direction we are iterating over the ranks and files
        flip_file = file_diff < 0
        flip_rank = rank_diff < 0

        # get the ranges over the ranks and files in the correct order of iteration
        if flip_rank:
            rank_range = range(from_rank - 1, to_rank - 1, - 1)
        else:
            rank_range = range(from_rank + 1, to_rank + 1)

        if flip_file:
            file_range = range(from_file -1, to_file - 1, -1)
        else:
            file_range = range(from_file + 1, to_file + 1)

        # generate the positions along diagonal by pairing rank range and file range
        diag_positions = zip(rank_range, file_range) # zip([0,1,2] , [0,1,2]) will give (0,0), (1,1), (2,2)
        for rank, file in diag_positions:
            pos = self.get_pos_from_loc((rank,file))
            path.append((pos, self.get_piece_from_pos(pos)))  # add the position and occupant at pos to the path
        return path

    def get_ortho_path(self, from_pos, to_pos):
        """Returns ordered list of [ (location, occupant) tuples] from from_pos to to_pos along ortho.
        Do not include current location in the list. Last item is to_pos. """

        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []
        flip_dir = False

        if from_rank != to_rank and from_file != to_file: # return empty path if to_pos is not ortho to from_pos
            return path

        # determine which direction we are iterating over the ranks and files
        if to_rank < from_rank:
            flip_dir = True
        if to_file < from_file:
            flip_dir = True

        # get the ranges over the ranks and files in the correct order of iteration
        if from_rank == to_rank and not flip_dir:
            file_range = range(from_file + 1, to_file + 1)
        elif from_rank == to_rank and flip_dir:
            file_range = range(from_file - 1, to_file - 1, -1)
        elif from_file == to_file and not flip_dir:
            rank_range = range(from_rank + 1, to_rank + 1)
        elif from_file == to_file and flip_dir:
            rank_range = range(from_rank - 1, to_rank - 1, -1)

        if from_rank == to_rank:   # keep rank constant, add all file steps in range
            for file in file_range: # get positions along rank from [from_file +1, to_file]
                this_pos = self.get_pos_from_loc((to_rank, file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant)) # add position and occupant to path

        elif from_file == to_file: # keep file constant, add all rank steps in range
            for rank in rank_range: # get positions along file from [from_rank + 1, to_rank]
                this_pos = self.get_pos_from_loc((rank, to_file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant)) # add position and occupant to path
        return path

    def get_ranks(self):
        """Returns an ordered array of the Board's rank letters, 'a' through 'i'."""
        return self._ranks

    def get_files(self):
        """Returns an ordered array of the Board's file numbers, '1' through '10'."""
        return self._files

    def get_available_positions(self, side):
        """ Returns a list of all positions that are unoccupied, or occupied by side's foe. Includes (at least)
        all possible locations that a Piece on side could occupy to on next move. Side is passed as 'red' or 'black'. """
        return_pos = []
        for file_str in self._files:
            for rank_str in self._ranks:
                occupant = self.get_piece_from_pos(file_str + rank_str)
                if occupant is None or occupant.get_side() != side:
                    return_pos.append(file_str + rank_str)
        return return_pos