"""Reproducible early prototype for the before recording."""
from game import Desk, CARD_W, HEIGHT, TRAY_W


class BaselineDesk(Desk):
    def catches(self, card):
        # The early prototype only compares horizontal coordinates.
        return card.x < self.x + TRAY_W and card.x + CARD_W > self.x

    def file_cards(self):
        # Removing the current card can skip the next adjacent card.
        for card in self.cards:
            if self.catches(card):
                self.filed[card.kind] += 1
                self.cards.remove(card)
            elif card.y > HEIGHT:
                self.missed += 1
                self.cards.remove(card)
