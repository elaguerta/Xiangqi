from GeneralPiece import GeneralPiece
from ElephantPiece import ElephantPiece
from ChariotPiece import ChariotPiece
from SoldierPiece import SoldierPiece
from Piece import Piece

class Player():

    def __init__(self, side, board):
        self._side = side   # 'black' or 'red'
        self._board = board
        self._pieces = set()

        # initialize general and save to an instance variable for easy access. add the general to the set of this
        # Player's pieces.
        self._general = (GeneralPiece(side, board))
        self._pieces.add(self._general)

        # initialize 2 Elephant pieces
        self._pieces.add(ElephantPiece(side, board, 1))
        self._pieces.add(ElephantPiece(side, board, 2))

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

    def get_defense_moves(self, attack_piece, path):
        """ returns a set of {(from_pos, to_pos)} moves that would defend Player's general from attack_piece along path.
        Returns the empty set if no such move.
        Attack_piece is a piece that is placing this Player's general in check. Path is the ordered list of
        [ (location, occupant) tuples] from attack piece to the other general """
        defense_moves = {}

        # See if one of Player's pieces can capture attack_piece at its current location
        for piece in self._pieces:
            if piece.is_legal(attack_piece.get_pos()):
                defense_moves.add((piece.get_pos(), attack_piece.get_pos()))

        # See if one of Player's pieces can block this attack by occupying any position along path
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
                # for now, save a tuple with from_position, 'screen piece' flag, and the path from the cannon
                defense_moves.add((occupant.get_pos, 'screen_piece', path))
        # we have exhausted all possibilities of block, capture, or disabling the attack_piece. Return the resulting
        # set of moves
        return defense_moves

    def defend_all_checks(self, attackers):
        """ Returns a set of moves that would defend Player's general from all checks in parameter
        attackers. Returns empty set if no such move. The parameter attackers is a list
        of (attack_pieces, paths) that represent all current checks against Player """

        # initialize set to the first set of defense moves against the first attack, then keep intersecting with each
        # subsequent set of defense moves until attackers list is exhausted

        attack_piece, path = attackers[0]
        # returns a set of defense moves against the first attack in the list
        defense_moves = self.get_defense_moves(attack_piece, path)


        for index in range(1, len(attackers)):
            attack_piece, path = attackers[index]
            # intersect the set of defense moves against this attack with the previous set
            defense_moves = defense_moves.intersection(self.get_defense_moves(attack_piece, path))

        return defense_moves # defense moves contains the set of moves that can defend all checks in attackers list

    def puts_self_in_check(self, piece, to_pos ,opp):
        """ returns True of a move of piece to to_pos would put self in check"""
        from_pos = piece.get_pos()  # save piece's previous position
        try_move = piece.move(to_pos) #ask the piece to try the move
        if not try_move:
            return False
        # ask the opponent to examine results of move for attacks on this Player's general
        resulting_checks = opp.get_attacks(self.get_general_pos())
        # now tell the piece to reverse the move. try_move will be assigned the captive, if any
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
            print("puts self in check")
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

        possible_moves = self._board.get_available_positions(self._side)
        for piece in self._pieces:
            if piece.get_pos() is not None: # if piece has not been captured
                for pos in possible_moves:  # search through possible moves
                    # if piece can legally move to pos and and would not put self in check, Player
                    # has at least one available move. Return the move.
                    if piece.is_legal(pos) and not self.puts_self_in_check(piece, pos, opponent):
                        return (piece.get_pos(), pos)
        # if no such move, return False
        return False

