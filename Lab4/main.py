"""Run the Grant Desk game. Arrow keys move the tray, Space expedites."""
import argparse
import sys
import pygame
from baseline import BaselineDesk
from game import Card, Desk, WIDTH, HEIGHT, TRAY_W, TRAY_Y, CARD_W, CARD_H


class Display:
    def __init__(self, surface):
        self.screen = surface
        self.small = pygame.font.SysFont("segoeui", 18)
        self.bold = pygame.font.SysFont("segoeui", 18, bold=True)
        self.large = pygame.font.SysFont("georgia", 32)

    def label(self, text, xy, font=None, color="#223B38"):
        self.screen.blit((font or self.small).render(text, True, color), xy)

    def draw(self, desk):
        s = self.screen
        s.fill("#F4F1EA")
        pygame.draw.rect(s, "#153B35", (0, 0, WIDTH, 84))
        self.label("Grant Desk", (24, 8), self.large, "#F6F1E6")
        self.label("Research office intake", (26, 51), color="#CCDCD4")
        self.label(f"Grants   {desk.filed['Grant']}      Papers   {desk.filed['Paper']}      Missed   {desk.missed}/5",
                   (464, 28), self.bold, "#FAF4DA")
        for x in range(12, WIDTH, 119):
            pygame.draw.line(s, "#E3DFD6", (x, 98), (x, 449))
        for card in desk.cards:
            box = pygame.Rect(card.x, card.y, CARD_W, CARD_H)
            fill = "#D3E7DA" if card.kind == "Grant" else "#F5D8B0"
            pygame.draw.rect(s, fill, box, border_radius=6)
            pygame.draw.rect(s, "#56716B", box, width=1, border_radius=6)
            self.label(card.kind, (box.x + 14, box.y + 6), self.bold)
        color = "#BD6A28" if desk.boost else "#23705B"
        pygame.draw.rect(s, color, (desk.x, TRAY_Y, TRAY_W, 16), border_radius=5)
        self.label("INTAKE", (desk.x + 32, TRAY_Y + 17), self.bold, color)
        pygame.draw.rect(s, "#E4EAE4", (0, 466, WIDTH, 54))
        self.label("Left / Right   Move tray       Space   Expedite       R   Restart", (24, 480))
        status = "EXPEDITE ACTIVE" if desk.boost else ("Cooling down" if desk.cooldown else "Expedite ready")
        self.label(status, (645, 480), self.bold, color)
        if desk.missed >= 5:
            pygame.draw.rect(s, "#153B35", (210, 196, 420, 96), border_radius=10)
            self.label("Intake closed", (242, 205), self.large, "#FFFFFF")
            self.label("Press R for a new shift.", (244, 252), color="#D8E5DD")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--record", action="store_true",
                        help="write 10 seconds of scripted RGB frames to stdout")
    args = parser.parse_args()
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grant Desk")
    display = Display(screen)
    make_desk = BaselineDesk if args.baseline else Desk
    desk = make_desk(9 if args.record else None)
    clock = pygame.time.Clock()
    frame = 0
    if args.record:
        desk.cards = [Card(desk.x + 8, 100, "Grant"), Card(desk.x + 20, 100, "Paper")]
        desk.until_spawn = 1.4
    while True:
        dt = 1 / 30 if args.record else min(clock.tick(60) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                desk.expedite()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                desk = make_desk()
        if args.record:
            direction = 0 if frame < 94 else (1 if 94 <= frame < 132 else -1 if 155 <= frame < 201 else 0)
            if frame == 95:
                desk.expedite()
        else:
            keys = pygame.key.get_pressed()
            direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        display.draw(desk)
        pygame.display.flip()
        if args.record:
            sys.stdout.buffer.write(pygame.image.tostring(screen, "RGB"))
            frame += 1
            if frame == 300:
                return
        desk.step(dt, direction)


if __name__ == "__main__":
    main()
