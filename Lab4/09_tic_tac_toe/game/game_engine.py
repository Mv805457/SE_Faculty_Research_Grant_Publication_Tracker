"""Control one human-versus-computer match, with scores across rounds."""
import pygame
from game import renderer
from game.ai import choose_move
from game.rules import check_winner, is_board_full


class GameEngine:
    def __init__(self):
        self.next_starter = "X"
        self.reset_match()

    def reset_match(self):
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.new_round()

    def new_round(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.next_starter
        self.round_over = False
        self.winner = None
        self._computer_turn()

    def _play(self, row, col):
        if self.round_over or self.board[row][col] is not None:
            return False
        self.board[row][col] = self.current_player
        self.winner = check_winner(self.board)
        if self.winner or is_board_full(self.board):
            self.round_over = True
            self.scores[self.winner or "Draw"] += 1
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def _computer_turn(self):
        if self.current_player == "O" and not self.round_over:
            move = choose_move(self.board)
            if move is not None:
                self._play(*move)

    def handle_click(self, pos):
        cell = renderer.board_pos_to_cell(pos)
        if cell is not None and self.current_player == "X" and self._play(*cell):
            self._computer_turn()

    def handle_keydown(self, key):
        if key in (pygame.K_x, pygame.K_o):
            self.next_starter = "X" if key == pygame.K_x else "O"
        elif key == pygame.K_r:
            self.new_round()
        elif key == pygame.K_m:
            self.reset_match()

    def draw(self, surface, font):
        renderer.draw_board(surface, self.board)
        score = "    ".join(f"{name}: {count}" for name, count in self.scores.items())
        renderer.draw_text(surface, font, score, (10, 5))
        renderer.draw_text(surface, font, "X/O: next starter  " + self.next_starter, (10, 34))
        renderer.draw_text(surface, font, "R: new round   M: reset match", (10, 63))
        status = "Your turn (X)"
        if self.round_over:
            status = f"{self.winner} wins!" if self.winner else "Draw!"
        renderer.draw_text(surface, font, status, (10, 465))
