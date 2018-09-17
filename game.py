#!/usr/bin/env python
import sys
import pygame
import pygame.locals
from grid import Grid
from token import Token
from magnet import Magnet

def indexToPixels(x, y):
    return (105 * x + 75, 105 * y + 75)

def pixelToIndex(x, y):
    return ((x - 50) / 105, (y - 50) / 105)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hack Four')
        self.screen = pygame.display.set_mode((725, 725), 0, 32)
        self.screen.fill((40, 40, 40))
        self.gridSurface = pygame.Surface((625, 625))
        self.clock = pygame.time.Clock()

        self.current_player = 0

        self.grid = Grid(self.gridSurface)
        self.grid.update()
        self.grids = pygame.sprite.LayeredUpdates(self.grid)

        self.tokens = pygame.sprite.LayeredUpdates()

        self.magnets = pygame.sprite.LayeredUpdates()
        magnet = Magnet(self.screen, 342, 680, 0, self.grid.gravDown)
        magnet.activate()
        self.magnets.add(magnet)
        self.magnets.add(Magnet(self.screen, 5, 342, 270, self.grid.gravLeft))
        self.magnets.add(Magnet(self.screen, 342, 5, 180, self.grid.gravUp))
        self.magnets.add(Magnet(self.screen, 680, 342, 90, self.grid.gravRight))

        self.hovertoken = [pygame.sprite.LayeredUpdates(Token(0, self.screen, 0, 0)),
                           pygame.sprite.LayeredUpdates(Token(1, self.screen, 0, 0))]

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        return

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.grid.contains(*event.pos):
                x, y = pixelToIndex(*event.pos)
                if self.grid.isOpen(x, y):
                    token = Token(self.current_player, self.gridSurface, x, y)
                    token.add(self.tokens)
                    self.grid.setToken(token, x, y)
                    self.current_player = (self.current_player + 1) % 2
            else:
                for magnet in self.magnets:
                    if magnet.contains(*event.pos) and not magnet.active:
                        for allmag in self.magnets:
                            allmag.shutdown()
                        magnet.activate()
                        self.current_player = (self.current_player + 1) % 2


    def draw(self):
        self.screen.fill((40, 40, 40))
        self.grids.draw(self.gridSurface)
        self.tokens.draw(self.gridSurface)
        self.magnets.draw(self.screen)
        self.screen.blit(self.gridSurface, (50, 50))
        if self.grid.contains(*pygame.mouse.get_pos()):
            self.hovertoken[self.current_player].draw(self.screen)
        pygame.display.update()


    def win(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    Game().mainloop()
                    self.quit()

            for path in self.wins:
                toks = [self.grid.getToken(x, y) for x, y in path]
                if all([not tok.moving() for tok in toks]):
                    [tok.win() for tok in toks]

            self.grid.update()
            self.tokens.update()
            self.screen.fill((40, 40, 40))
            self.grids.draw(self.gridSurface)
            self.tokens.draw(self.gridSurface)
            self.magnets.draw(self.screen)
            self.screen.blit(self.gridSurface, (50, 50))
            pygame.display.update()
            self.clock.tick(60)


    def mainloop(self):
        while True:
            map(self.handleEvent, pygame.event.get())
            self.grid.update()
            self.tokens.update()
            self.wins = self.grid.wins()
            if len(self.wins) > 0:
                self.win()
            self.hovertoken[self.current_player].sprites()[0].rect.topleft = pygame.mouse.get_pos()
            self.draw()
            self.clock.tick(60)


    def quit(self):
        pygame.quit()
        sys.exit()
