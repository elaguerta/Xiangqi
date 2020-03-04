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

    def get_defense_moves(self, attack_piece, path):
        """ returns a set of {(from_pos, to_pos)} moves that would defend Player's general from attack_piece along path.
        Returns the empty set if no such move.
        Attack_piece is a piece that is placing this Player's general in check. Path is the ordered list of
        [ (location, occupant) tuples] from attack piece to the other general """
        defense_moves = {}
        target = attack_piece.get_pos()

        # See if one of Player's pieces can block this attack
        # by occupying any position along path, including capture of the attack_piece at its current location
        for piece in self._pieces:
            for pos, occupant in path:
                if piece.is_legal(pos):             # this piece can block or capture
                    defense_moves.add((piece.get_pos(), pos))  # add the move to the set of defense moves

        # Only Cannons have occupants along their attack path, and they have exactly one occupant along the path,
        # called the 'screen'. If the screen piece belongs to Player, Player can defend against Cannon by
        # moving the 'screen' from the path
        for pos, occupant in path:
            if occupant.get_side() == player:
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
        defense_moves = self.get_defense_moves(attack_piece, path)

        for index in range(1, len(attackers)):
            attack_piece, path = attackers[index]
            defense_moves = defense_moves.intersection(self.get_defense_moves(attack_piece, path))

        return defense_moves


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

    def get_attacks(self, opp_general_pos):
        """returns a list of (attacker, path) tuples
         for any piece of this Player's that has a shot at the opposing general's position. Returns an empty list if
         no such attack."""
        attackers = []
        for piece in self._pieces:
            if piece.is_legal(opp_general_pos):
                path = piece.get_path(opp_general_pos)
                attackers.append((piece,path))
        return attackers


