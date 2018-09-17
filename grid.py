#!/usr/bin/env python
import sys
import token
import pygame


class Grid(pygame.sprite.Sprite):
    def __init__(self, screen, size=6, surfacesize=625):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.grid = [[None for i in range(size)] for j in range(size)]
        self.pusher = [self._gravity]
        self.surfacesize = 625

        self.image = pygame.Surface((self.surfacesize, self.surfacesize), pygame.SRCALPHA)
        self.image.fill((40, 40, 40))
        square = pygame.Surface((100, 100), pygame.SRCALPHA)
        square.blit(pygame.transform.scale(pygame.image.load("images/a2.png"), (50, 50)), (0, 0))
        square.blit(pygame.transform.scale(pygame.image.load("images/a3.png"), (50, 50)), (50, 0))
        square.blit(pygame.transform.scale(pygame.image.load("images/a1.png"), (50, 50)), (0, 50))
        square.blit(pygame.transform.scale(pygame.image.load("images/a4.png"), (50, 50)), (50, 50))


        for x in range(0, 600, 105):
            for y in range(0, 600, 105):
                self.image.blit(square, (x, y))

            #pygame.draw.rect(self.image, (255, 255, 255), (coord, 0, 5, self.surfacesize))
            #pygame.draw.rect(self.image, (255, 255, 255), (0, coord, self.surfacesize, 5))


        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def wins(self):
        winning_paths = []
        for i in range(self.size):
            for j in range(self.size):
                paths = [[(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)],
                         [(i, j), (i, j + 1), (i, j + 2), (i, j + 3)],
                         [(i, j), (i - 1, j + 1), (i - 2, j + 2), (i - 3, j + 3)],
                         [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]]
                for path in paths:
                    if 0 <= path[-1][0] < self.size and 0 <= path[-1][1] < self.size:
                        toks = [self.grid[i2][j2] for i2, j2 in path]
                        if not None in toks:
                            color = toks[0].playerID
                            if all([tok.playerID == color for tok in toks]):
                                winning_paths.append(path)
        return winning_paths

    def update(self):
        return

    def display(self):
        return

    def isOpen(self, x, y):
        return self.grid[x][y] is None

    def setToken(self, token, x, y):
        assert self.grid[x][y] is None
        self.display()
        self.grid[x][y] = token
        self.display()

    def getToken(self, x, y):
        return self.grid[x][y]

    def update(self):
        for meth in self.pusher:
            meth()

    def _rotate_left(self):
        copy = [[None for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] is not None:
                    self.grid[i][j].setDestinationByIndex(self.size - j - 1, i)
                    copy[self.size - j - 1][i] = self.grid[i][j]
        self.grid = [[copy[i][j] for j in range(self.size)] for i in range(self.size)]

    def _rotate_right(self):
        copy = [[None for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] is not None:
                    self.grid[i][j].setDestinationByIndex(j, self.size - i - 1)
                    copy[j][self.size - i - 1] = self.grid[i][j]
        self.grid = [[copy[i][j] for j in range(self.size)] for i in range(self.size)]

    def gravLeft(self):
        self.pusher = [self._rotate_right, self._gravity, self._rotate_left]

    def gravRight(self):
        self.pusher = [self._rotate_left, self._gravity, self._rotate_right]

    def gravUp(self):
        self.pusher = [self._rotate_right, self._rotate_right, self._gravity, self._rotate_left, self._rotate_left]

    def gravDown(self):
        self.pusher = [self._gravity]

    def _gravity(self):
        for j in range(self.size - 2, -1, -1):
            for i in range(self.size):
                if self.grid[i][j] is None:
                    continue
                new_height = j
                while new_height + 1 < self.size and self.grid[i][new_height + 1] is None:
                    new_height += 1
                if new_height != j:
                    self.grid[i][j].setDestinationByIndex(i, new_height)
                    self.grid[i][new_height] = self.grid[i][j]
                    self.grid[i][j] = None

    def contains(self, x, y):
        return self.rect.collidepoint(x - 50, y - 50)


def main():
    return

if __name__ == "__main__":
    main()
