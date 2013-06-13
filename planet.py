#!/usr/bin/python

import pygame
import math

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

	


class trace:
	def __init__(self, window):
		self.history=[]
		self.window=window
	def newpoint(self, pos):
		self.history.append(pos)
	def draw(self):
		for p in self.history:
			pygame.draw.circle(self.window, (0,255,0), p, 2)

size=(800,600)
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)

sun = planet([400,300], [-.5,0], [0,0], 1000000, (255,0,0), 10, window)
moon = planet([400,100], [50,0], [0,0], 10000, (255,255,255), 5, window)
planets=(sun,moon)
t=trace(window)
counter=0
while 1:
	window.fill(pygame.Color(0,0,0))
	t.draw()
	for planet in planets:
		planet.verlet_a(0.5)
	for planet in planets:
		planet.verlet_b(lambda x: multi_gravity(planet,planets), 0.5)
		planet.update_pos()
		planet.draw()

	if counter==1:
		t.newpoint((int(moon.pos[0]), int(moon.pos[1])))
		counter=0
	pygame.display.update()
	fps.tick(30)
	counter+=1
pygame.quit()



