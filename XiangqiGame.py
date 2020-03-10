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
        return self._game_state

    def get_player(self, player):
        """return the Player represented by player string - 'red' or 'black'"""
        if player == 'red':
            return self._red_player
        if player == 'black':
            return self._black_player

    def get_turn(self):
        return self._turn

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
        if player.has_available_move(opponent):
            return False
        return True

    def is_in_checkmate(self, side):
        """ returns True if this side's Player is in checkmate. Player is in checkmate if there is no one move that can
        defend against all current checks"""

        defender = self.get_player(side)
        attacker = self.get_opponent(side)
        defending_general = defender.get_general_pos()
        attack_list = attacker.get_attacks(defending_general)
        if attack_list:
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
        if self._game_state != 'UNFINISHED':    # if the game has already been won, return False
            return False

        if from_pos == to_pos:                  # do not allow a move that does not change the board state
            return False
        if self.out_of_range(from_pos) or self.out_of_range(to_pos):    # validate that positions are within range
            return False

        # allow the turn to proceed
        turn_player = self.get_player(self._turn)
        opp = self.get_opponent(self._turn)
        try_move = turn_player.move(from_pos, to_pos, opp)     # ask this turn's Player to attempt the move
        if not try_move:                            # if not successful, return False
            return False

        # If we got to this point, move succeeded, update the game state, and return True
        self.update_game_state()
        self.update_turn()
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
                self._game_state = 'RED_WON'
            else:
                self._game_state = 'BLACK_WON'
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


class Board:
    """ Note: "loc" refers to a [rank][file] location in memory of the 2D matrix that stores the board state
    "pos" refers to a '<file><rank>' string that is passed to the Board class to request access to the corresponding
    board_state location """
    def __init__(self):
        """ initializes a blank Xiangqi Board"""
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

        self._piece_state = {}          # dictionary of piece: pos pairs. When pieces are captured, value is set to None

    def get_castle_spots(self, player):
        """
        :param player: "red" or "black"
        :return: A set of positions that comprise the castle positions for that player
        """
        if player == 'red':
            return self._red_castle_spots
        elif player == 'black':
            return self._black_castle_spots
        else:
            return False

    def get_board_state(self):
        """ returns pointer to 2D matrix that tracks board state. Positions that are not occupied are
        set to None."""
        return self._board_state

    def display_board(self, num_spaces = 2):
        delim = ' ' * num_spaces
        print( (delim * 10), "BLACK")
        print(' ', delim, ("  " + delim).join(self._files))  # print letter files in order
        for rank in reversed(self._ranks):                      #print black side first, from rank 10 to rank 1
            rank_state = self._board_state[int(rank) - 1]
            if rank == '10':
                line = rank + ' ' * (num_spaces - 1)
            else:
                line = rank + delim
            for item in rank_state:
                if item is None:
                    line += '---' + delim
                else:
                    line += repr(item)[:3] + delim # display first 3 characters of string representation, plus delim
            print(line)
        print(' ', delim, ("  " + delim).join(self._files))         # print letter files in order
        print(delim * 10, "RED")
        print()
        print()

    def place_piece(self, piece, to_pos):
        """
        Sets to_pos to be occupied by piece.
        :param item:  a Piece of any type
        :param to_pos: A position that will be occupied by the piece
        :return: Sets to_pos to be occupied by piece. No return value.
        """
        rank,file = self.get_loc_from_pos(to_pos)
        self._board_state[rank][file] = piece  # piece now occupies to_pos
        self._piece_state[str(piece)] = to_pos

    def clear_piece(self, piece):
        """ sets the piece_state for None. Used for keeping track of captures"""
        self._piece_state[str(piece)] = None

    def clear_pos(self, pos):
        """ Sets pos to None. Used for clearing a pos when a piece moves away from pos"""
        rank, file = self.get_loc_from_pos(pos)
        self._board_state[rank][file] = None  # set pos to None

    def get_loc_from_pos(self, pos):
        """ Helper method to translate pos strings to indices, to
        set and get positions in the board state"""
        rank_index = int(pos[1:]) - 1
        file_index = self._files.index(pos[0])
        return (rank_index, file_index) # return pointer to the pos location in the board_state

    def get_pos_from_loc(self, loc):
        """ Helper method to translate a (rank, file) tuple index into a position string"""
        rank_str = str(loc[0] + 1)
        file_str = str(self._files[loc[1]])
        return file_str + rank_str

    def get_piece_from_pos(self, pos):
        """ Returns the piece at pos, or None if pos is not occupied"""
        rank, file = self.get_loc_from_pos(pos)
        return self._board_state[rank][file]

    def get_general_pos(self, player):
        """ returns the position of the general on side of player"""
        return self._piece_state[ player[0] + "Ge"]

    def get_L_path(self, from_pos, to_pos):
        """ ordered list of [ (position, occupant) tuples] from from_pos to to_pos along L path.
                        Do not include current location in the list. Last item is to_pos. """
        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []

        # generate the max 8 possible L-path destinations from the start location
        # the 4 maximum intermediate locations are one unit in every ortho direction
        loc_diffs_int = [(0,-1), (0,1), (1,0), (-1,0)]# permute one unit difference in rank and file directions
        # create a list of possible intermediate locations
        int_locs = [(from_rank + rank_diff, from_file + file_diff) for rank_diff, file_diff in loc_diffs_int]
        # filter any locs that are out of range
        int_locs = [(rank, file) for rank,file in int_locs if 0 <= rank < len(self._ranks) and 0 <= file < len(self._files)]

        # a valid L path will continue along ortho trajectory set by intermediate location
        # From start to intermediate, and from intermediate to destination, both moves increase rank or file
        # by one unit. Find the corresponding intermediate position,  if any, to to_pos
        int_pos = None
        for int_rank, int_file in int_locs:
            if from_rank - int_rank == int_rank - to_rank: # both ranks increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))
            elif from_file - int_file == int_file - to_file: # both files increase or decrease by 1 unit
                int_pos = self.get_pos_from_loc((int_rank, int_file))

        if int_pos:
            try_dest = self.get_diagonal_path(int_pos, to_pos) # find a valid diagonal from intermedate to destination

        if int_pos and try_dest:
            path.append( (int_pos, self.get_piece_from_pos(int_pos)) )
            path.append(try_dest)

        return path

    def get_diagonal_path(self, from_pos, to_pos):
        """ ordered list of [ (location, occupant) tuples] from from_pos to to_pos along diagonal.
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

        flip_file = file_diff < 0
        flip_rank = rank_diff < 0

        if flip_rank:
            rank_range = range(from_rank - 1, to_rank - 1, - 1)
        else:
            rank_range = range(from_rank + 1, to_rank + 1)

        if flip_file:
            file_range = range(from_file -1, to_file - 1, -1)
        else:
            file_range = range(from_file + 1, to_file + 1)

        diag_positions = zip(rank_range, file_range)
        for rank, file in diag_positions:
            pos = self.get_pos_from_loc((rank,file))
            path.append((pos, self.get_piece_from_pos(pos)))
        return path

    def get_ortho_path(self, from_pos, to_pos):
        """ ordered list of [ (location, occupant) tuples] from from_pos to to_pos along ortho.
        Do not include current location in the list. Last item is to_pos. """

        to_rank, to_file = self.get_loc_from_pos(to_pos)
        from_rank, from_file = self.get_loc_from_pos(from_pos)
        path = []
        flip_dir = False

        if from_rank != to_rank and from_file != to_file: # return empty path if to_pos is not ortho to from_pos
            return path

        if to_rank < from_rank:
            flip_dir = True
        if to_file < from_file:
            flip_dir = True

        if from_rank == to_rank and not flip_dir:
            file_range = range(from_file + 1, to_file + 1)
        elif from_rank == to_rank and flip_dir:
            file_range = range(from_file - 1, to_file - 1, -1)
        elif from_file == to_file and not flip_dir:
            rank_range = range(from_rank + 1, to_rank + 1)
        elif from_file == to_file and flip_dir:
            rank_range = range(from_rank - 1, to_rank - 1, -1)

        if from_rank == to_rank:            # get positions along rank from [from_file +1, to_file]
            for file in file_range:
                this_pos = self.get_pos_from_loc((to_rank, file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        elif from_file == to_file:
            for rank in rank_range:
                this_pos = self.get_pos_from_loc((rank, to_file))
                occupant = self.get_piece_from_pos(this_pos)
                path.append((this_pos, occupant))
        return path

    def get_ranks(self):
        return self._ranks

    def get_files(self):
        return self._files

    def get_available_positions(self, side):
        """ returns a list of all positions that are unoccupied, or occupied by side's foe. Includes (at least)
        all possible locations that a Piece on side could occupy to on next move"""
        return_pos = []
        for file_str in self._files:
            for rank_str in self._ranks:
                occupant = self.get_piece_from_pos(file_str + rank_str)
                if occupant is None or occupant.get_side() == side:
                    return_pos.append(file_str + rank_str)
        return return_pos

class Player():

    def __init__(self, side, board):
        self._side = side   # 'black' or 'red'
        self._board = board
        self._pieces = set()

        # initialize general and save to an instance variable for easy access. add the general to the set of this
        # Player's pieces.
        self._general = (GeneralPiece(side, board))
        self._pieces.add(self._general)

        # initialize 2 Advisor Pieces
        self._pieces.add(AdvisorPiece(side, board, 1))
        self._pieces.add(AdvisorPiece(side, board, 2))

        # initialize 2 Elephant pieces
        self._pieces.add(ElephantPiece(side, board, 1))
        self._pieces.add(ElephantPiece(side, board, 2))

        # initialize 2 Horse pieces
        self._pieces.add(HorsePiece(side, board, 1))
        self._pieces.add(HorsePiece(side, board, 2))

        # initialize 2 chariot pieces
        self._pieces.add(ChariotPiece(side, board, 1))
        self._pieces.add(ChariotPiece(side, board, 2))

        # initialize 2 cannon pieces
        self._pieces.add(CannonPiece(side, board, 1))
        self._pieces.add(CannonPiece(side, board, 2))

        # initialize 5 soldiers
        self._pieces.add(SoldierPiece(side, board, 1))
        self._pieces.add(SoldierPiece(side, board, 2))
        self._pieces.add(SoldierPiece(side, board, 3))
        self._pieces.add(SoldierPiece(side, board, 4))
        self._pieces.add(SoldierPiece(side, board, 5))

        # place all pieces in initial positions
        for piece in self._pieces:
            self._board.place_piece(piece, piece.get_pos())

    def get_defense_moves(self, attack_piece, path, opp):
        """ returns a set of {(from_pos, to_pos)} moves that would defend Player's general from attack_piece along path.
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
        attackers. Returns empty set if no such move. The parameter attackers is a list
        of (attack_pieces, paths) that represent all current checks against Player """

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
        return defense_moves # defense moves contains the set of moves that can defend all checks in attackers list

    def puts_self_in_check(self, piece, to_pos ,opp):
        """ returns True of a move of piece to to_pos would put self in check"""
        from_pos = piece.get_pos()  # save piece's previous position
        try_move = piece.move(to_pos) #ask the piece to try the move

        # ask the opponent to examine results of move for attacks on this Player's general
        resulting_checks = opp.get_attacks(self.get_general_pos())

        # now tell the piece to reverse the move. try_move will be assigned the captive, if any
        if try_move:
            piece.reverse_move(from_pos, to_pos, try_move)

        if resulting_checks: # if there were any resulting checks, return True
            return True
        return False

    def get_general_pos(self):
        """ return the position of this player's general"""
        return self._general._pos

    def move(self, from_pos, to_pos, opp):
        piece = self._board.get_piece_from_pos(from_pos)    # get the piece on from_pos.

        if not piece:                                   # the from position is empty
            return False

        if piece not in self._pieces:             # the piece on the from position does not belong to this player
            return False

        if self.puts_self_in_check(piece, to_pos, opp): # the move would result in a check on this player
            return False
        # tell the piece to attempt the move, return the result
        try_move = piece.move(to_pos)
        return try_move

    def get_attacks(self, opp_general_pos, board = None):
        """returns a list of (attacker, path) tuples
         for any piece of this Player's that has a shot at the opposing general's position. Returns an empty list if
         no such attack."""
        if not board:
            board = self._board
        attackers = []
        for piece in self._pieces:
            if piece.get_pos() is not None and piece.is_legal(opp_general_pos):
                path = piece.get_path(opp_general_pos)
                attackers.append((piece,path))
        return attackers

    def has_available_move(self, opponent):
        """ returns True if this player has at least one legal move"""

       # get all possible moves for all pieces
        possible_moves = set()
        remove_moves = set()
        for piece in self._pieces:
            piece_moves = piece.get_possible_moves()
            possible_moves  = possible_moves.union(piece_moves)
        # filter any move that would place self in check
        for from_pos, to_pos in possible_moves:
            piece = self._board.get_piece_from_pos(from_pos)
            if self.puts_self_in_check(piece, to_pos, opponent):
                remove_moves.add((from_pos, to_pos))
        available_moves = possible_moves - remove_moves
        if available_moves:
            return available_moves
        return False

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

        occupant = self._board.get_piece_from_pos(to_pos)
        if occupant and occupant._side == self._side: # if the to_pos is occupied by a friend, return False
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

class AdvisorPiece(Piece):
    advisor_positions = {
        'red': ['d1', 'f1'],
        'black': ['d10', 'f10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'diagonal'  # ortho, diagonal, or L shaped
        self._path_length = 1

        # assign a position.
        self._id = id_num
        self._pos = AdvisorPiece.advisor_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ad" + str(self._id)

    def is_legal(self, to_pos):
        # advisors must remain in castle
        if to_pos not in (self._board.get_castle_spots(self._side)):
            return False
        return super().is_legal(to_pos)

class CannonPiece(Piece):
    cannon_postions = {
        'red': ['b3', 'h3'],
        'black': ['b8', 'h8']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # keep track of this chariot by assigning it an ID equal to the lenght of possible positions for this side
        # then destructively popping a position from the class and assigning it to thiis Chariot
        self._id =  id_num
        self._pos = CannonPiece.cannon_postions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ca" + str(self._id)

    def is_legal(self, to_pos):
        # cannon requires screen piece for capture, friend or foe
        # if this move would result in a capture, temporarily set jumps to 1
        occupant = self._board.get_piece_from_pos(to_pos)
        if occupant and occupant.get_side() != self._side:
            self._jumps = 1
        result = super().is_legal(to_pos)           # call super with jumps updated if necessary
        self._jumps = 0                             # reset jumps to 0
        return result

class ChariotPiece(Piece):
    chariot_postions = {
        'red': ['a1', 'i1'],
        'black': ['a10', 'i10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped

        # keep track of this chariot by assigning it an ID equal to the lenght of possible positions for this side
        # then destructively popping a position from the class and assigning it to thiis Chariot
        self._id =  id_num
        self._pos = ChariotPiece.chariot_postions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ch" + str(self._id)

class ElephantPiece(Piece):
    elephant_positions = {
        'red': ['c1', 'g1'],
        'black': ['c10', 'g10']
    }
    legal_ranks = {
        'red': {'1','2','3','4','5'},
        'black': {'10','9','8','7','6'}
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'diagonal'  # ortho, diagonal, or L shaped
        self._path_length = 2

        # assign a position.
        self._id = id_num
        self._pos = ElephantPiece.elephant_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "El" + str(self._id)

    def is_legal(self, to_pos):
        return super().is_legal(to_pos) and to_pos[1:] in ElephantPiece.legal_ranks[self._side]

class GeneralPiece(Piece):
    general_positions = {'red':'e1', 'black':'e10'}
    def __init__(self, player, board):
        super().__init__(player, board)
        self._movement = 'ortho'  #
        self._path_length = 1
        self._pos = GeneralPiece.general_positions[player]

    def __repr__(self):
        return self._side[0] + "Ge"

    def is_legal(self, to_pos):
        """ calls super().is_legal and then checks the additional parameters of the general's movement:
        the general must stay in the palace, flying general move may be executed """
        flying_general_flag = self.is_flying_general(to_pos)

        if flying_general_flag:     # if flying general is possible, temporarily lift path length restriction
            self._path_length = None
        # check Piece.is_legal, with max path length restriction lifted if flying general is possible
        if not super().is_legal(to_pos): # check with updated flying general flag
            self._path_length = 1    # reset path length
            return False

        # in the case that flying general isn't possible, check that the general remains in the castle
        if not flying_general_flag and to_pos not in (self._board.get_castle_spots(self._side)):
            self._path_length = 1
            return False

        # reset path restriction if necessary
        self._path_length = 1
        return True

    def is_flying_general(self, to_pos):
        """ helper method to is_legal. Returns True if this general's move to to_pos is a flying general move"""
        other_gen_pos = self._board.get_general_pos(self._opp)  # get the other general's position
        if other_gen_pos == to_pos and other_gen_pos[0] == self._pos[0]:  # if both generals on the same file
            path_to_gen = self.get_path(other_gen_pos)            # get ortho path to general
            if self.num_jumps(path_to_gen) == 0:        # if no intervening pieces, flying general is possible
                return True

class HorsePiece(Piece):
    horse_positions = {
        'red': ['b1', 'h1'],
        'black': ['b10', 'h10']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'L-shaped'  # ortho, diagonal, or L shaped
        self._path_length = 2   # one point ortho, one point diagonal

        # assign a position.
        self._id = id_num
        self._pos = HorsePiece.horse_positions[player][id_num - 1]

    def __repr__(self):
        return self._side[0] + "Ho" + str(self._id)

class SoldierPiece(Piece):
    soldier_positions = {
        'red': ['a4', 'c4', 'e4', 'g4', 'i4'],
        'black': ['a7', 'c7', 'e7', 'g7', 'i7']
    }

    def __init__(self, player, board, id_num):
        super().__init__(player, board)
        self._movement = 'ortho'  # ortho, diagonal, or L shaped
        self._path_length = 1
        self._crossed_river = False

        # assign a position.
        self._id = id_num
        self._pos = SoldierPiece.soldier_positions[player][id_num - 1]


    def __repr__(self):
        return self._side[0] + "So" + str(self._id)

    def is_legal(self, to_pos):
        """ calls super().is_legal and then checks the additional restrictions on the soldier's movement:
        cannot retreat, can move and capture by advancing one point, can move and capture horizontally by
        one point after crossing river"""

        # check the conditions that are checked for all pieces
        try_path = super().is_legal(to_pos)
        if not try_path:
            return False

        to_rank, to_file = self._board.get_loc_from_pos(to_pos)
        from_rank, from_file = self._board.get_loc_from_pos(self._pos)

        # if the move is a retreat, return False
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
        move_result = super().move(to_pos)        # move as usual

        # if red makes it to 6, or black makes it to 5, river was crossed. Set self._crossed_river to True
        if self._side == 'red' and to_pos[1:] == '6':
            self._crossed_river = True

        if self._side == 'black' and to_pos[1:] == '5':
            self._crossed_river = True

        return move_result