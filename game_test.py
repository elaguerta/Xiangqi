# Author: Elaine Laguerta
# Date: 21 January 2019
# Description: Tests the library class

import unittest
import XiangqiGame

class TestGame(unittest.TestCase):
    def test_1:
        """ Example given in problem statement. """
        game = XiangqiGame()
        move_result = game.make_move('c1', 'e3')
        black_in_check = game.is_in_check('black')
        game.make_move('e7', 'e6')
        state = game.get_game_state()




if __name__ == "__main__":
    unittest.main()