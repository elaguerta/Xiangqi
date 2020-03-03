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

        # add jump test here when board is complete


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
        # move red chariot at a1 to black chariot at a1. Should return black chariot. Delete test when rest of board
        # is set
        black_chariot = my_board.get_piece_from_pos('a10')
        game.make_move('a1', 'a10')

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
        # write test for flying general here

    def test_soldier(self):
        """ tests basic rules limiting soldier's movement"""
        game = XiangqiGame()
        board = game._board
        board.display_board()

        # move by advancing one point
        self.assertEqual(game.make_move('e4', 'e5'), True)
        self.assertEqual(game.make_move('e7', 'e6'), True)

        #capture by advancing one point
        piece =

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