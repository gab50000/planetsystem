#!/usr/bin/python

import planet as p
import pygame, math

class moving_sun(p.planet):
	def __init__(self, pos, centerpos, vel, acc, mass, color, radius, window):
		p.planet.__init__(self,pos, vel, acc, mass, color, radius, window)
		self.centerpos=centerpos
		self.angle=0
		self.l= 5	
		self.pos[0]=self.centerpos[0]+self.l
		self.pos[1]=self.centerpos[1]
	
	def rotate(self):
		self.angle+=0.03
		self.newpos[0]=self.centerpos[0]+math.cos(self.angle)*self.l
		self.newpos[1]=self.centerpos[1]+math.sin(self.angle)*self.l

size=(1024,768)
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)

sun = moving_sun([400,300], [400,300], [0,0], [0,0], 10000, (255,255,0), 10, window)
moon = p.planet([400,500], [-5,0], [0,0], 10, (255,255,255), 5, window)
planets=[sun,moon]

counter=0
while 1:
	sun.rotate()
	moon.verlet_a(0.5)
	moon.verlet_b(p.gravity(moon,sun), 0.5)
	moon.update_pos()
	sun.update_pos()
	if counter==10:	
		window.fill(pygame.Color(0,0,0))
		for planet in planets:
			planet.t.newpoint((int(planet.pos[0]), int(planet.pos[1])))
			planet.t.draw()
		for planet in planets:
			planet.draw()
		pygame.display.update()
		fps.tick(30)

		counter=0
	counter+=1
pygame.quit()
