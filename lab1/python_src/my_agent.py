from agent import Agent
from enum import IntEnum
from copy import deepcopy


class Orientation(IntEnum):
	NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

class Point:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __str__(self):
		"""for debugging"""
		return "Point({},{})".format(self.x, self.y)

	def __eq__(self, other):
		"""to check if position == home """
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		"""to add position to visited set"""
		return hash(str(self))

	def move(self, orientation, step=1):
		""" Updates position """
		# turn the match into if statements
		if orientation == Orientation.NORTH:
			self.y += step
		elif orientation == Orientation.EAST:
			self.x += step
		elif orientation == Orientation.SOUTH:
			self.y -= step
		elif orientation == Orientation.WEST:
			self.x -= step


class MyAgent(Agent):
	def __init__(self):
		self.position = Point()
		self.home = Point()
		self.orientation = Orientation.NORTH
		self.turned_on = False
		self.visited = {self.home}
		self.n_bumps = 0
		self.cont = 0
		self.r_l = 0 
		self.change_main = False
		self.begin_zig_zag = False

	# this method is called when the environment has reached a terminal state
	# override it to reset the agent
	def cleanup(self, percepts):
		self.orientation = Orientation.NORTH
		self.turned_on = False
		self.visited = {self.home}
		self.n_bumps = 0
		self.cont = 0
		self.r_l = 0 
		self.change_main = False
		self.begin_zig_zag = False
  
	def turn_on(self):
		self.turned_on = True
		return "TURN_ON"

	def turn_off(self):
		self.turned_on = False
		return "TURN_OFF"

	def turn_right(self):
		self.orientation = (self.orientation + 1) % 4
		return "TURN_RIGHT"

	def turn_left(self):
		self.orientation = (self.orientation - 1) % 4
		return "TURN_LEFT"

	def go(self):
		self.position.move(self.orientation)
		self.visited.add(deepcopy(self.position))
		return "GO"

	def undo_move(self):
		self.visited.remove(self.position)
		self.position.move(self.orientation, -1)
		#return "GO"

	def suck(self):
		return "SUCK"


	def zig_zag(self, percepts):
		if self.cont == 0:
				self.cont += 1
				return self.go()
		elif self.cont == 1:
			self.cont += 1
			self.r_l += 1
			# if self.r_l is odd turn right
			if self.r_l % 2 == 1:
				self.change_main = True
				return self.turn_right()
			else :
				self.change_main = False
				return self.turn_left()

		if "BUMP" in percepts:
			self.undo_move()
			self.cont = 0
			if self.change_main:
				return self.turn_left()
			return self.turn_right()
		# if percept is empty go
		if not percepts:
			# print the debug info for position
			print("position: " + str(self.position))
			return self.go()

	#def home(self):
	#	return "GO"

	
 	# this method is called on each time step of the environment
	# it needs to return the action the agent wants to execute as as string
	def next_action(self, percepts):
		print("percepts: " + str(percepts))
		# print size of visited
		print("size of visited: " + str(len(self.visited)))
  
		#if len(self.visited) >= 25:
		#	# return home

		if not self.turned_on:
			return self.turn_on()
		
		if "DIRT" in percepts:
			return self.suck()

		if self.n_bumps == 3:
			self.begin_zig_zag = True

		if self.begin_zig_zag:
			#if len(self.visited) >= 25:
			#	return home()
			return self.zig_zag(percepts)
			

		if "BUMP" in percepts:
			self.n_bumps += 1
			self.undo_move()
			if self.change_main:
				return self.turn_left()
			return self.turn_right()
		
  		# if percept is empty go
		if not percepts:
			# print the debug infor for position
			print("position: " + str(self.position))
			return self.go()
		

		


