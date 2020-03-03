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

        # try to jump over a soldier. Should fail.
        self.assertEqual(game.make_move('a1', 'a5'), False)

        # try to move chariot diagonally from a1 to b2. Should fail.
        self.assertEqual(game.make_move('a1', 'b2'), False)

        # try to move out of bounds in both directions. Should fail.
        self.assertEqual(game.make_move('a1', 'j1'), False)
        self.assertEqual(game.make_move('a1', 'a0'), False)
        self.assertEqual(game.make_move('a1', 'a11'), False)

        # move black chariot in "opposite" directions
        game._turn = 'black'
        self.assertEqual(game.make_move('a10', 'a8'), True)
        self.assertEqual(game.make_move('i10', 'g10'), True)
        game._turn = 'red'

    def test_move(self):
        """ tests move logic at game level"""
        game = XiangqiGame()

        # try to move a black piece when turn is red's. Should fail.
        self.assertEqual(game.make_move('a10', 'a9'), False)

        # try to move from an empty square
        self.assertEqual(game.make_move('a2', 'a5'), False)

        # if the game is already won, move should return false
        game._game_state = 'RED_WON'
        self.assertEqual(game.make_move('a1', 'a2'), False)
        game._game_state = 'UNFINISHED'

        # if move is successful, update whose turn it is and return true
        game.make_move('a1', 'a2')
        self.assertEqual(game._turn, 'black')

    def test_general(self):
        """ tests basic rules limiting general's movement"""
        game = XiangqiGame()
        # test basic movement forward and to both sides
        self.assertEqual(game.make_move('e1', 'e2'), True)         # move red general forward
        self.assertEqual(game.make_move('e10', 'e9'), True)          # move black general forward
        self.assertEqual(game.make_move('e2', 'f2'), True)          # move red general east
        self.assertEqual(game.make_move('e9', 'd9'), True)          # move black general west
        self.assertEqual(game.make_move('f2', 'g2'), False)         # try to leave castle, should return False
        self.assertEqual(game.make_move('d9', 'c9'), False)

        # put player in check using flying general
        game = XiangqiGame()
        board = game._board
        e7 = board.get_piece_from_pos('e7') # remove black soldier on e7
        board.clear_pos('e7')
        board.clear_piece(e7)
        e4 = board.get_piece_from_pos('e4')  # remove red soldier on e4
        board.clear_pos('e4')
        board.clear_piece(e4)

        # now black should be in check from flying general
        self.assertEqual(game.is_in_check('black'), True)
        self.assertEqual(game.is_in_check('red'), False)
        red_gen = board.get_piece_from_pos('e1')
        self.assertEqual(red_gen.is_flying_general('e10'), True)

    def test_soldier(self):
        """ tests basic rules limiting soldier's movement"""
        game = XiangqiGame()
        board = game._board

        # move by advancing one point
        self.assertEqual(game.make_move('e4', 'e5'), True)
        self.assertEqual(game.make_move('e7', 'e6'), True)

        #capture by advancing one point
        captive = board.get_piece_from_pos('e6')  # black soldier
        self.assertEqual(game.make_move('e5', 'e6'), True) # red captures black
        self.assertEqual(str(captive)[0:-1], 'bSo')


        # try to move horizontally having not crossed river
        self.assertEqual(game.make_move('c7', 'b7'), False) # black attempts move

        # move horizontally after crossing river
        game.make_move('c7', 'c6')
        game.update_turn()  # red turn
        game.make_move('c6', 'c5') # black crosses river
        game.update_turn() # red turn
        self.assertEqual(game.make_move('c5', 'b5'), True) #black moves horizontally


def test_game_state(self):
        pass
        # if this move would win the game, update game state and return true


    # def test_example(self):
    #     """ Example given in problem statement. """
    #     game = XiangqiGame()
    #     move_result = game.make_move('c1', 'e3')
    #     black_in_check = game.is_in_check('black')
    #     game.make_move('e7', 'e6')
    #     state = game.get_game_state()




if __name__ == "__main__":
    unittest.main()