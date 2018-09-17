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

WIDTH, HEIGHT = (725, 725)
pygame.init()
pygame.display.set_caption('Hack 4')
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
screen.fill((40, 40, 40))
gridSurface = pygame.Surface((625, 625))
clock = pygame.time.Clock()

current_player = 0

grid = Grid(gridSurface)
grid.update()
grids = pygame.sprite.LayeredUpdates(grid)

tokens = pygame.sprite.LayeredUpdates()

magnets = pygame.sprite.LayeredUpdates()
magnet = Magnet(screen, 342, 680, 0, grid.gravDown)
magnet.activate()
magnets.add(magnet)
for x, y, rot, func in [(5, 342, 270, grid.gravLeft), (342, 5, 180, grid.gravUp), (680, 342, 90, grid.gravRight)]:
    magnets.add(Magnet(screen, x, y, rot, func))

hovertoken = [pygame.sprite.LayeredUpdates(Token(0, screen, 0, 0)), pygame.sprite.LayeredUpdates(Token(1, screen, 0, 0))]

def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #elif event.type == pygame.KEYUP:
            #keymap = {pygame.K_LEFT: grid.gravLeft, pygame.K_RIGHT: grid.gravRight,
                    #pygame.K_UP: grid.gravUp, pygame.K_DOWN: grid.gravDown, pygame.K_SPACE: pause}
            #if event.key in keymap:
                #keymap[event.key]()
            #current_player = (current_player + 1) % 2

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if grid.contains(*event.pos):
                x, y = pixelToIndex(*event.pos)
                if grid.isOpen(x, y):
                    token = Token(current_player, gridSurface, x, y)
                    token.add(tokens)
                    grid.setToken(token, x, y)
                    current_player = (current_player + 1) % 2
            else:
                for magnet in magnets:
                    if magnet.contains(*event.pos) and not magnet.active:
                        for allmag in magnets:
                            allmag.shutdown()
                        magnet.activate()
                        current_player = (current_player + 1) % 2

    grid.update()
    tokens.update()
    wins = grid.wins()
    if len(wins) > 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for path in wins:
                toks = [grid.getToken(x, y) for x, y in path]
                if all([not tok.moving() for tok in toks]):
                    [tok.win() for tok in toks]

            grid.update()
            tokens.update()
            screen.fill((40, 40, 40))
            grids.draw(gridSurface)
            tokens.draw(gridSurface)
            magnets.draw(screen)
            screen.blit(gridSurface, (50, 50))
            pygame.display.update()
            clock.tick(60)

    hovertoken[0].sprites()[0].rect.topleft = pygame.mouse.get_pos()
    hovertoken[1].sprites()[0].rect.topleft = pygame.mouse.get_pos()

    screen.fill((40, 40, 40))
    grids.draw(gridSurface)
    tokens.draw(gridSurface)
    magnets.draw(screen)
    screen.blit(gridSurface, (50, 50))
    if grid.contains(*pygame.mouse.get_pos()):
        hovertoken[current_player].draw(screen)


    pygame.display.update()

    clock.tick(60)
