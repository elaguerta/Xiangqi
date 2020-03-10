# Author: Elaine Laguerta
# Date: 21 January 2019
# Description: Tests the library class

import unittest
from XiangqiGame import XiangqiGame

class TestGame(unittest.TestCase):

    def test_cannon(self):
        """ test cannon movement pattern"""
        game = XiangqiGame()
        # make legal moves on both sides in all 4 directions
        self.assertEqual(game.make_move('h3', 'h7'), True)  # move red cannon forward
        self.assertEqual(game.make_move('b8', 'b5'), True) # move black cannon forward
        self.assertEqual(game.make_move('b3', 'a3'), True)  # move red cannon west
        self.assertEqual(game.make_move('b5', 'i5'), True)  # move black cannon east

        # try to move diagonally
        self.assertEqual(game.make_move('a3', 'c6'), False)  # try to move red cannon diagonal

        # try to jump 1 piece without capturing
        self.assertEqual(game.make_move('h8', 'h2'), False)  # try to move black cannon to jump

        # try to capture without screen
        self.assertEqual(game.make_move('h7', 'h8'), False) # try to move red cannon to capture without jump

        # make legal capture with screen
        game.update_turn()  # red turn
        captive =  game._board.get_piece_from_pos('i1')
        self.assertEqual(game.make_move('i5', 'i1'), True) # black cannon captures red chariot with 1 jump
        self.assertEqual(captive.get_pos(), None)       # confirm capture
        self.assertEqual(game._board._piece_state[str(captive)], None)


    def test_horse(self):
        """ test horse movement pattern """
        game = XiangqiGame()

        # make legal moves
        self.assertEqual(game.make_move('h1', 'g3'), True)  # move red horse forward
        self.assertEqual(game.make_move('b10', 'a8'), True)  # move black horse forward

        # try to move when blocked
        self.assertEqual(game.make_move('g3', 'f5'), False)  # try to move red horse
        game.update_turn()
        self.assertEqual(game.make_move('a8', 'b6'), False)  #try to move black horse

        # try to move in non L pattern
        game.update_turn()
        self.assertEqual(game.make_move('b1', 'd3'), False)  # try to move red horse diagonal
        game.update_turn()
        self.assertEqual(game.make_move('h10', 'h9'), False)  # try to move black horse ortho

    def test_general(self):
        """ tests basic rules limiting general's movement"""
        game = XiangqiGame()
        # test basic movement forward and to both sides
        self.assertEqual(game.make_move('e1', 'e2'), True)  # move red general forward
        self.assertEqual(game.make_move('e10', 'e9'), True)  # move black general forward
        self.assertEqual(game.make_move('e2', 'f2'), True)  # move red general east
        self.assertEqual(game.make_move('e9', 'd9'), True)  # move black general west
        self.assertEqual(game.make_move('f2', 'g2'), False)  # try to leave castle, should return False
        game.update_turn()
        self.assertEqual(game.make_move('d9', 'c9'), False)

        # put player in check using flying general
        game = XiangqiGame()
        board = game._board
        e7 = board.get_piece_from_pos('e7')  # remove black soldier on e7
        board.clear_pos('e7')
        board.clear_piece(e7)
        e4 = board.get_piece_from_pos('e4')  # remove red soldier on e4
        board.clear_pos('e4')
        board.clear_piece(e4)

        # now both sides should be in check from flying general
        self.assertEqual(game.is_in_check('black'), True)
        self.assertEqual(game.is_in_check('red'), True)
        red_gen = board.get_piece_from_pos('e1')
        self.assertEqual(red_gen.is_flying_general('e10'), True)

    def test_advisor(self):
        """ test advisor movement pattern"""
        game = XiangqiGame()

        # make legal moves
        self.assertEqual(game.make_move('d1', 'e2'), True) # move red advisor within castle
        self.assertEqual(game.make_move('d10', 'e9'), True) # move black advisor within castle
        self.assertEqual(game.make_move('e2', 'd1'), True)  # move red advisor within castle
        self.assertEqual(game.make_move('e9', 'd10'), True)  # move black advisor within castle

        # try to move more than 1 position
        self.assertEqual(game.make_move('d1', 'f3'), False)  # move red advisor within castle, 2 spots
        game.update_turn()
        self.assertEqual(game.make_move('d10', 'f8'), False)  # move black advisor within castle, 2 spots

        # try to move outside castle
        game.update_turn()
        self.assertEqual(game.make_move('f1', 'h3'), False)  # move red advisor outside castle, 1 spots
        game.update_turn()
        self.assertEqual(game.make_move('f10', 'h8'), False)  # move black advisor outside castle, 1 spots

        # try to move ortho
        game.update_turn()
        self.assertEqual(game.make_move('f1', 'f2'), False)  # move red advisor ortho, 1 spot
        game.update_turn()
        self.assertEqual(game.make_move('f10', 'f9'), False)  # move black advisor ortho, 1 spot

    def test_elephant(self):
        """ test elephant movement pattern"""
        game = XiangqiGame()

        #test legal moves
        self.assertEqual(game.make_move('g1', 'i3'), True) # red elephant moves 2 diagonal
        self.assertEqual(game.make_move('c10', 'e8'), True) # black elephant moves 2 diagonal
        self.assertEqual(game.make_move('i3','g5' ), True) # red elephant moves 2 diagonal
        self.assertEqual(game.make_move('e8', 'g6'), True) # black elephant moves 2 diagonal
    #
        # move back and forth, legally
        self.assertEqual(game.make_move('g5', 'i3'), True)  # red elephant moves 2 diagonal
        self.assertEqual(game.make_move('g6', 'e8'), True)  # black elephant moves 2 diagonal
        self.assertEqual(game.make_move('i3', 'g5'), True)  # red elephant moves 2 diagonal
        self.assertEqual(game.make_move('e8', 'g6'), True)  # black elephant moves 2 diagonal
    #
        # try to cross river
        self.assertEqual(game.make_move('g5','e7'), False) # red tries to capture at e7 but can't cross river
        game.update_turn()
        self.assertEqual(game.make_move('g6', 'i4'), False)  # black tries to capture at i4 but can't cross river

        # try to move ortho
        game.update_turn()
        self.assertEqual(game.make_move('g5', 'g3'), False)

        # try to move more than two spaces
        game.update_turn()
        self.assertEqual(game.make_move('g6', 'd9'), False)


    def test_piece(self):
        """ test basic piece logic on chariot piece"""
        game = XiangqiGame()

        #try to jump over a soldier. Should fail.
        self.assertEqual(game.make_move('a1', 'a5'), False)

        # try to move chariot diagonally from a1 to b2. Should fail.
        self.assertEqual(game.make_move('a1', 'b2'), False)

        # try to move out of bounds in both directions. Should fail.
        self.assertEqual(game.make_move('a1', 'j1'), False)
        self.assertEqual(game.make_move('a1', 'a0'), False)
        self.assertEqual(game.make_move('a1', 'a11'), False)

        # move black chariot in "opposite" directions
        game.update_turn()          # make it black's turn
        self.assertEqual(game.make_move('a10', 'a8'), True)

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


        # if move is successful, update whose turn it is and return true
        game._game_state = 'UNFINISHED'
        game.make_move('a1', 'a2')
        self.assertEqual(game._turn, 'black')



    def test_soldier(self):
        """ tests basic rules limiting soldier's movement"""
        game = XiangqiGame()
        board = game._board

        # move by advancing one point
        self.assertEqual(game.make_move('e4', 'e5'), True) # red moves
        self.assertEqual(game.make_move('e7', 'e6'), True) # black moves

        #capture by advancing one point
        captive = board.get_piece_from_pos('e6')  # get black soldier
        self.assertEqual(game.make_move('e5', 'e6'), True) # red captures black
        # confirm capture
        self.assertEqual(captive.get_pos(), None)
        self.assertEqual(game._board._piece_state[str(captive)], None)

        # try to move horizontally having not crossed river
        self.assertEqual(game.make_move('c7', 'b7'), False) # black attempts move

        # move horizontally after crossing river
        game.make_move('c7', 'c6')  # black moves
        game.update_turn()  # red turn
        game.make_move('c6', 'c5') # black crosses river
        game.update_turn() # red turn
        self.assertEqual(game.make_move('c5', 'b5'), True) #black moves horizontally


    def test_game_state(self):
        # brief game where black is mated
        game = XiangqiGame()
        self.assertEqual(game.make_move('b3', 'e3'), True) # red moves cannon b
        self.assertEqual(game.make_move('h8', 'e8'), True) # black moves cannon h

        self.assertEqual(game.make_move('h3', 'h6'), True) # red moves cannon h
        self.assertEqual(game.make_move('b8', 'b4'), True) # black moves cannon b

        self.assertEqual(game.make_move('e3', 'e7'), True) # red cannon captures black soldier
        self.assertEqual(game.make_move('e8', 'e4'), True) # black captures red soldier

        self.assertEqual(game.make_move('h6', 'e6'), True) # red mates black, game ends on red's turn
        self.assertEqual(game.is_in_checkmate('black'), True)  # check checkmate
        self.assertEqual(game.get_game_state(), 'RED_WON')  # check game state

    def test_example(self):
        """ Example given in problem statement. """
        game = XiangqiGame()
        self.assertEqual(game.make_move('c1', 'e3'), True)
        self.assertEqual(game.is_in_check('black'), False)
        self.assertEqual(game.make_move('e7', 'e6'), True)
        self.assertEqual(game.get_game_state(), 'UNFINISHED')

if __name__ == "__main__":
    unittest.main()