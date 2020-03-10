from XiangqiGame import XiangqiGame

if __name__ == "__main__":
    game = XiangqiGame()
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