#!/usr/bin/python

import pygame
import math
import random
from collections import deque

class planet:
	def __init__(self, pos, vel, acc, mass, color, radius, window):
		self.pos=pos
		self.newpos=[0,0]
		self.vel=vel
		self.acc=acc
		self.mass=mass
		self.color=color
		self.radius=radius
		self.window=window
		self.t=trace(self.window, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

	def verlet_a(self, dt):
		self.newpos[0] = self.pos[0] + self.vel[0]*dt + 0.5 * self.acc[0]*dt*dt 
		self.newpos[1] = self.pos[1] + self.vel[1]*dt + 0.5 * self.acc[1]*dt*dt 
	def verlet_b(self, forcefunc, dt):
		force=forcefunc(self)

		self.vel[0] = self.vel[0] + 0.5*(self.acc[0] + force[0]/self.mass)*dt
		self.vel[1] = self.vel[1] + 0.5*(self.acc[1] + force[1]/self.mass)*dt

		self.acc[0] = force[0]/self.mass
		self.acc[1] = force[1]/self.mass

	def update_pos(self):
		self.pos=self.newpos

	def draw(self):
		pygame.draw.circle(self.window, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class trace:
	def __init__(self, window, color):
		self.history=deque([])
		self.window=window
		self.color=color
	def newpoint(self, pos):
		self.history.append(pos)
		if len(self.history) > 1000:
			self.history.popleft()

	def draw(self):
		for p in self.history:
			pygame.draw.circle(self.window, self.color, p, 2)

def gravity(planet1, planet2):
	dr = (planet2.newpos[0]-planet1.newpos[0], planet2.newpos[1]-planet1.newpos[1])
	lensqdr_rez=1./(dr[0]*dr[0]+dr[1]*dr[1])
	lendr_rez=math.sqrt(lensqdr_rez)
	g = planet1.mass * planet2.mass * lensqdr_rez 

	return (g*dr[0]*lendr_rez, g*dr[1]*lendr_rez) 

def multi_gravity(planet1, planetlist):
	gravsum=[0,0]
	for planet2 in planetlist:
		if planet1!=planet2:
			grav=gravity(planet1,planet2)
			gravsum[0]+=grav[0]
			gravsum[1]+=grav[1]
	return gravsum

	



size=(800,600)
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)

sun = planet([400,300], [-0.02,0], [0,0], 1000, (255,0,0), 10, window)
moon = planet([400,500], [-1,0], [0,0], 10, (255,255,255), 5, window)
moon2 = planet([400,20], [1,0], [0,0], 10, (255,255,255), 5, window)
planets=[sun,moon, moon2]
planets.append(planet([100,300], [0,1], [0,0], 10, (255,255,255), 5, window))
planets.append(planet([700,300], [0,-1], [0,0], 10, (255,255,255), 5, window))

t1=trace(window, (0,255,0))
t2=trace(window, (255,0,255))
counter=0
while 1:
	for planet in planets:
		planet.verlet_a(1)
	for planet in planets:
		planet.verlet_b(lambda x: multi_gravity(planet,planets), 1)
		planet.update_pos()
	if counter==5:
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



