# Author: Elaine Laguerta
# Date: 21 January 2019
# Description: Tests the library class

import unittest
from XiangqiGame import XiangqiGame
from Board import Board
from ChariotPiece import ChariotPiece

class TestGame(unittest.TestCase):

    def test_piece(self):
        """ test basic piece logic on chariot piece"""
        game = XiangqiGame()
        my_board = game._board

        # place an additional chariot on a2 and try to move the a1 chariot to a4. Should fail.
        my_board.place_piece(ChariotPiece(my_board, 'red', 'a2'), 'a2')
        self.assertEqual(game.make_move('a1', 'a4'), False)
        my_board.clear_pos('a2')

        # try to move chariot diagonally from a1 to b2. Should fail.
        self.assertEqual(game.make_move('a1', 'b2'), False)

        # try to move out of bounds in both directions. Should fail.
        self.assertEqual(game.make_move('a1', 'j1'), False)
        self.assertEqual(game.make_move('a1', 'a0'), False)
        self.assertEqual(game.make_move('a1', 'a11'), False)

        # try to move a black piece when turn is red's. Should fail.
        self.assertEqual(game.make_move('a10', 'a9'), False)

        # try to move from an empty square
        self.assertEqual(game.make_move('a2', 'a5'), False)


        # move red chariot at a1 to black chariot at a1. Should return black chariot. Delete test when rest of board
        # is set
        black_chariot = my_board.get_piece_from_pos('a10')
        self.assertEqual(game.make_move('a1', 'a10'), black_chariot)
        my_board.display_board()


    # def test_example(self):
    #     """ Example given in problem statement. """
    #     game = XiangqiGame()
    #     move_result = game.make_move('c1', 'e3')
    #     black_in_check = game.is_in_check('black')
    #     game.make_move('e7', 'e6')
    #     state = game.get_game_state()




if __name__ == "__main__":
    unittest.main()