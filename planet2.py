#!/usr/bin/python

import pygame
from pygame.locals import *
import math

import planet as p


class MovingSun(p.Planet):
    def __init__(self, pos, centerpos, vel, acc, mass, color, radius, window):
        p.Planet.__init__(self, pos, vel, acc, mass, color, radius, window)
        self.centerpos = centerpos
        self.angle = 0
        self.l = 5
        self.pos[0] = self.centerpos[0] + self.l
        self.pos[1] = self.centerpos[1]

    def rotate(self):
        self.angle += 0.03
        self.newpos[0] = self.centerpos[0] + math.cos(self.angle) * self.l
        self.newpos[1] = self.centerpos[1] + math.sin(self.angle) * self.l


def distance(p1, p2):
    sqdist = (p1.pos[0]-p2.pos[0])*(p1.pos[0]-p2.pos[0]) + (p1.pos[1]-p2.pos[1])*(p1.pos[1]-p2.pos[1])
    return math.sqrt(sqdist)

def print_energy(p1, p2, font, window):
    en = 0.5 * (p1.mass*(p1.vel[0]*p1.vel[0] + p1.vel[1]*p1.vel[1]) + p2.mass*(p2.vel[0]*p2.vel[0] + p2.vel[1]*p2.vel[1]))
    en += p1.mass * p2.mass / distance(p1, p2)
    t = font.render("{:.2f}".format(en), 1, (255, 255, 255))
    window.blit(t, (50, 50))
    print(en)


if __name__ == "__main__":
    size = (1024, 768)
    pygame.init()
    fps = pygame.time.Clock()
    window = pygame.display.set_mode(size)
    font = pygame.font.Font(None, 20)
    sun = MovingSun(pos=[400, 300], centerpos=[400, 300], vel=[0, 0], acc=[0, 0],
                    mass=10000, color=(255, 255, 0), radius=10, window=window)
    moon = p.Planet(pos=[400, 500], vel=[-5, 0], acc=[0, 0], mass=10,
                    color=(255, 255, 255), radius=5, window=window)
    planets = [sun, moon]

    counter = 0
    stop = False
    while 1:
        sun.rotate()
        moon.verlet_a(0.5)
        moon.verlet_b(p.gravity(moon, sun), 0.5)
        moon.update_pos()
        sun.update_pos()
        if counter == 10:
            window.fill(pygame.Color(0, 0, 0))
            for planet in planets:
                planet.t.newpoint((int(planet.pos[0]), int(planet.pos[1])))
                planet.t.draw()
            for planet in planets:
                planet.draw()
            print_energy(sun, moon, font, window)
            pygame.display.update()
            fps.tick(30)
            counter = 0
        counter += 1
        for ev in pygame.event.get():
            if ev.type == QUIT:
                stop = True
                break
        if stop:
            break
    pygame.quit()
