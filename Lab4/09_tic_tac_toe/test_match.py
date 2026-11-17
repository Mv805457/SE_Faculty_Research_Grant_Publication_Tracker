"""Exercise the course starter's four required changes."""
import copy
import unittest
from unittest.mock import patch
import pygame
from game.game_engine import GameEngine
from game.rules import check_winner


class MatchTests(unittest.TestCase):
    def test_eight_lines_for_both_symbols(self):
        lines = [[(r,c) for c in range(3)] for r in range(3)]
        lines += [[(r,c) for r in range(3)] for c in range(3)]
        lines += [[(r,r) for r in range(3)], [(r,2-r) for r in range(3)]]
        for line in lines:
            for symbol in "XO":
                board = [[None]*3 for _ in range(3)]
                for r,c in line:
                    board[r][c] = symbol
                self.assertEqual(check_winner(board),symbol)

    def test_last_cell_win_and_single_score(self):
        e=GameEngine()
        e.board=[list("XOX"),list("OXO"),["O","X",None]]
        e.handle_click((300,400))
        self.assertEqual((e.winner,e.scores["X"]),("X",1))
        e.handle_click((300,400))
        self.assertEqual(e.scores["X"],1)

    def test_full_draw(self):
        e=GameEngine()
        e.board=[list("XOX"),list("XOO"),["O","X",None]]
        e.handle_click((300,400))
        self.assertTrue(e.round_over)
        self.assertEqual(e.scores["Draw"],1)

    def test_occupied_cell_and_postwin_click(self):
        e=GameEngine()
        e.board[0][0]="O"
        e.handle_click((60,160))
        self.assertEqual((e.board[0][0],e.current_player),("O","X"))
        e.board=[["X","X",None],["O","O",None],[None,None,None]]
        e.handle_click((300,160))
        snapshot=copy.deepcopy(e.board)
        e.handle_click((60,400))
        self.assertEqual(e.board,snapshot)

    @patch("game.game_engine.choose_move",return_value=(1,1))
    def test_restarts_and_o_opener(self,choose):
        e=GameEngine()
        e.scores["X"]=2
        e.handle_keydown(pygame.K_o)
        self.assertIsNone(e.board[1][1])
        e.handle_keydown(pygame.K_r)
        self.assertEqual((e.scores["X"],e.board[1][1],e.current_player),(2,"O","X"))
        e.handle_keydown(pygame.K_x)
        e.handle_keydown(pygame.K_m)
        self.assertEqual(sum(e.scores.values()),0)
        self.assertTrue(all(c is None for row in e.board for c in row))
        choose.assert_called_once()
