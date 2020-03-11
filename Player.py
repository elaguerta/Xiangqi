from GeneralPiece import GeneralPiece
from ElephantPiece import ElephantPiece
from ChariotPiece import ChariotPiece
from SoldierPiece import SoldierPiece
from AdvisorPiece import AdvisorPiece
from HorsePiece import HorsePiece
from CannonPiece import CannonPiece
from Piece import Piece

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


