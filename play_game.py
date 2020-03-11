from XiangqiGame import XiangqiGame
from XiangqiGame_single_module import XiangqiGame
from Board import Board
from Player import Player
from GeneralPiece import GeneralPiece
from ElephantPiece import ElephantPiece
from ChariotPiece import ChariotPiece
from SoldierPiece import SoldierPiece
from AdvisorPiece import AdvisorPiece
from HorsePiece import HorsePiece
from CannonPiece import CannonPiece


if __name__ == "__main__":
    game = XiangqiGame()
    board = game._board
    red_pieces = game.get_player("red")._pieces
    black_pieces = game.get_player("black")._pieces

    # initialize empty board
    board._board_state = [  # board state represented as a 2D array
        [None for file in board._files] for rank in board._ranks  # initialize all positions to None
    ]

    board._piece_state = {}  # dictionary of piece: pos pairs. When pieces are captured, value is set to None

    for piece in black_pieces:
        piece.set_pos(None)

    for piece in red_pieces:
        piece.set_pos(None)

    for piece in black_pieces:
        if str(piece) == "bGe":
            piece.set_pos('d10')
            board.place_piece(piece, 'd10')  # black general on d9
        elif str(piece) == "bEl1":
            piece.set_pos('c6')
            board.place_piece(piece, 'c6')  # black advisor on d10


    for piece in red_pieces:
        if isinstance(piece, GeneralPiece):
            piece.set_pos('e2')
            board.place_piece(piece, 'e2')
        if str(piece) == "rHo1":
            piece.set_pos('f8')
            board.place_piece(piece, 'f8')  # black general on d9


    while game.get_game_state() == 'UNFINISHED':
        game._board.display_board()
        turn_player = game.get_turn()
        print(turn_player,"'s turn")
        if game.is_in_check(turn_player):
            print(turn_player, " is in check")
        if game.is_in_checkmate(turn_player):
            print(turn_player, " is in checkmate")
        if game.is_in_stalemate(turn_player):
            print(turn_player, " is in stalemate")
        try_move = None
        from_pos = input("Enter a location to move from: ").strip()
        to_pos = input("Enter a location to move to: ").strip()
        try_move = game.make_move(from_pos, to_pos)
        print(try_move)
        while not try_move:
            print("Move not valid. Try again.")
            from_pos = input("Enter a location to move from: ").strip()
            to_pos = input("Enter a location to move to: ").strip()
            try_move = game.make_move(from_pos, to_pos)
    print(game.get_game_state())