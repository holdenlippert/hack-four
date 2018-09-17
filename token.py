#!/usr/bin/env python
import pygame


def indexToPixels(x, y):
    return (105 * x + 25, 105 * y + 25)


class Token(pygame.sprite.Sprite):
    def __init__(self, playerID, screen, idx, idy):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.size = 50
        self.speed = 10
        self.playerID = playerID
        img = "token_blue.png" if playerID == 1 else "token_red.png"

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image = pygame.transform.scale(pygame.image.load(img), (self.size, self.size))
        #self.image.fill(self.color)

        self.yellow = pygame.transform.scale(pygame.image.load("token_yellow.png"), (self.size - 8, self.size - 8))
        self.winimage = pygame.transform.scale(pygame.image.load(img), (self.size, self.size))
        self.winimage.blit(self.yellow, (4, 4))



        self.rect = self.image.get_rect()
        self.setLocationByIndex(idx, idy)
        self.destination = (idx, idy)

    def setLocationByIndex(self, idx, idy):
        px, py = indexToPixels(idx, idy)
        self.rect.x = px
        self.rect.y = py

    def setDestinationByIndex(self, idx, idy):
        self.destination = (idx, idy)

    def update(self):
        destpx, destpy = indexToPixels(*self.destination)
        if self.rect.left < destpx:
            self.rect.left = min(destpx, self.rect.left + self.speed)
        elif self.rect.left > destpx:
            self.rect.left = max(destpx, self.rect.left - self.speed)

        if self.rect.top < destpy:
            self.rect.top = min(destpy, self.rect.top + self.speed)
        elif self.rect.top > destpy:
            self.rect.top = max(destpy, self.rect.top - self.speed)

    def win(self):
        self.image = self.winimage

    def moving(self):
        return self.rect.topleft != indexToPixels(*self.destination)

def main():
    return

if __name__ == "__main__":
    main()
