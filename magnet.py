#!/usr/bin/env python
import pygame
import numpy

def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
    arr = numpy.array([[[avg, avg, avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

class Magnet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, rot, func):
        pygame.sprite.Sprite.__init__(self)
        self.func = func
        self.screen = screen
        self.size = 40
        self.active = False
        img = "magnet.png"
        
        self.activeimage = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(img), (self.size, self.size)), rot)
        self.inactiveimage = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("magnet_grayscale.png"), (self.size, self.size)), rot)
        self.image = self.inactiveimage

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        return

    def activate(self):
        self.active = True
        self.image  = self.activeimage
        self.func()

    def shutdown(self):
        self.active = False
        self.image = self.inactiveimage

    def toggle(self):
        if self.active:
            self.shutdown()
        else:
            self.activate()

    def contains(self, x, y):
        return self.rect.collidepoint(x, y)


def main():
    return

if __name__ == "__main__":
    main()
