# Author: Elaine Laguerta
# Date: 21 January 2019
# Description: Tests the library class

import unittest
from XiangqiGame import XiangqiGame
from Board import Board

class TestGame(unittest.TestCase):

    def test_board (self):
        """ test Board class"""
        my_board = Board()
        self.assertEqual(my_board.get_castle_spots('red'), {'d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3'})
        self.assertEqual(my_board.get_castle_spots('black'), {'d10', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8'})
        self.assertEqual(my_board.get_river_bank('red'), '5')
        self.assertEqual(my_board.get_river_bank('black'), '6')
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