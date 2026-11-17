"""Grant Desk: a small arcade exercise for the research office."""
from dataclasses import dataclass
import random

WIDTH, HEIGHT = 840, 520
TRAY_Y, TRAY_W = 420, 120
CARD_W, CARD_H = 84, 38


@dataclass
class Card:
    x: float
    y: float
    kind: str


class Desk:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.x = (WIDTH - TRAY_W) / 2
        self.cards = []
        self.filed = {"Grant": 0, "Paper": 0}
        self.missed = 0
        self.boost = 0.0
        self.cooldown = 0.0
        self.until_spawn = 0.3
        self.last_lane = None

    def expedite(self):
        if self.cooldown <= 0 and self.missed < 5:
            self.boost = 1.6
            self.cooldown = 4.0

    def spawn(self):
        lanes = [i for i in range(7) if i != self.last_lane]
        lane = self.rng.choice(lanes)
        self.last_lane = lane
        x = 12 + lane * 119 + self.rng.randint(0, 24)
        self.cards.append(Card(x, 98, self.rng.choice(["Grant", "Paper"])))

    def catches(self, card):
        return (card.x < self.x + TRAY_W and card.x + CARD_W > self.x
                and card.y < TRAY_Y + 15 and card.y + CARD_H >= TRAY_Y)

    def file_cards(self):
        pending = []
        for card in self.cards:
            if self.catches(card):
                self.filed[card.kind] += 1
            elif card.y > HEIGHT:
                self.missed += 1
            else:
                pending.append(card)
        self.cards = pending

    def step(self, dt, direction=0):
        if self.missed >= 5:
            return
        self.x = min(WIDTH - TRAY_W, max(0, self.x + direction * dt *
                                        (510 if self.boost > 0 else 290)))
        self.boost = max(0.0, self.boost - dt)
        self.cooldown = max(0.0, self.cooldown - dt)
        self.until_spawn -= dt
        if self.until_spawn <= 0 and len(self.cards) < 5:
            self.spawn()
            self.until_spawn = self.rng.uniform(0.70, 1.25)
        for card in self.cards:
            card.y += 136 * dt
        self.file_cards()
