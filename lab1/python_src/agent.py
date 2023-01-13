import random
from enum import IntEnum
from copy import deepcopy

#############

"""Agent acting in some environment"""
class Agent(object):

  def __init__(self):
    return

  # this method is called on the start of the new environment
  # override it to initialise the agent
  def start(self):
    print("start called")
    return

  # this method is called on each time step of the environment
  # it needs to return the action the agent wants to execute as as string
  def next_action(self, percepts):
    print("next_action called")
    return "NOOP"

  # this method is called when the environment has reached a terminal state
  # override it to reset the agent
  def cleanup(self, percepts):
    print("cleanup called")
    return

#############

"""A random Agent for the VacuumCleaner world

 RandomAgent sends actions uniformly at random. In particular, it does not check
 whether an action is actually useful or legal in the current state.
 """
class RandomAgent(Agent):

  def next_action(self, percepts):
    print("perceiving: " + str(percepts))
    actions = ["TURN_ON", "TURN_OFF", "TURN_RIGHT", "TURN_LEFT", "GO", "SUCK"]
    action = random.choice(actions)
    print("selected action: " + action)
    return action

#############

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
		self.z_1 = (0,0)
		self.z_2 = (0,0)
		self.side_L = 0
		self.n_goes= 0
		self.go_home = False
		self.final_turn = False

	# this method is called when the environment has reached a terminal state
	# override it to reset the agent
	def cleanup(self, percepts):
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
		self.z_1 = (0,0)
		self.z_2 = (0,0)
		self.side_L = 0
		self.n_goes = 0
		self.go_home = False
		self.final_turn = False
		print("cleanup called")

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
		self.visited.remove(deepcopy(self.position))
		self.position.move(self.orientation, -1)
		#return "GO"

	def suck(self):
		return "SUCK"

	# this is my first zig zag
	# it used too many bumps, so the total steps were too high
	# so I made zig_zag_v2 which uses the x and y coordinates to know when to turn
	# and it is much better
	def zig_zag(self, percepts):
		if self.cont == 0:
			self.cont += 1
			return self.go()
		elif "BUMP" in percepts:
			self.undo_move()
			self.cont = 0
			if self.change_main:
				return self.turn_left()
			return self.turn_right()
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
		# if percept is empty go
		if not percepts:
			return self.go()

	def zig_zag_v2(self, percepts):
		if self.cont == 0:
			self.cont += 1
			self.n_goes += 1
			return self.go()
		if self.cont == 1:
			self.cont += 1
			self.r_l += 1
			# if self.r_l is odd turn right
			if self.r_l % 2 == 1:
				return self.turn_right()
			else :
				return self.turn_left()
		if self.n_goes == self.side_L*(self.side_L+1):
			self.go_home = True
			# if self.side_L + 1 is odd turn left else turn right
			if (self.side_L + 1) % 2 == 1:
				return self.turn_left()
			else:
				return self.turn_right()
		if not percepts:
			print("z_1: " + str(self.z_1))
			print("z_2: " + str(self.z_2))
			if self.position.y == self.z_1[1] and not self.change_main:
				self.cont = 0
				self.change_main = True
				return self.turn_left()
			elif self.position.y == self.z_2[1] and self.change_main:
				self.cont = 0
				self.change_main = False
				return self.turn_right()
			self.n_goes += 1
			return self.go()
			
	def clean_all(self, percepts):
		if not self.turned_on and not self.go_home:
			return self.turn_on()
		
		if "DIRT" in percepts:
			return self.suck()
 
		if self.n_bumps == 3:
			self.n_bumps = 4
			self.begin_zig_zag = True
			self.z_2 = (self.position.x, self.position.y)
			self.side_L = abs(self.z_2[1] - self.z_1[1])

		if self.begin_zig_zag:
			return self.zig_zag_v2(percepts)

		if "BUMP" in percepts:
			self.n_bumps += 1
			self.undo_move()
			if self.n_bumps == 2:
				self.z_1 = (self.position.x, self.position.y)
			return self.turn_right()
		# if percept is empty go
		if not percepts:
			return self.go()


	def going_home(self, percepts):
		# go forward until x or y is 0
		# then turn to the left
		# then go forward until x and y are 0 and turn off
		print("GOING HOME")
		if self.position.x == 0 and self.position.y == 0:
			return self.turn_off()

		if (self.position.x == 0 or self.position.y == 0) and self.final_turn == False:
			self.final_turn = True
			if (self.side_L % 2 + 1) == 1:
				return self.turn_left()
			else:
				return self.turn_right()
		# if percept is empty go
		if not percepts:
			return self.go()


 	# this method is called on each time step of the environment
	# it needs to return the action the agent wants to execute as as string
	def next_action(self, percepts):
		print("percepts: " + str(percepts))
		print("is home: " + str(self.position == self.home))
		print("position: " + str(self.position))
		print("size of visited: " + str(len(self.visited)))
		print("side_L: " + str(self.side_L))

		#if len(self.visited) >= 25:
		#	# return home
		if not self.go_home:
			return self.clean_all(percepts)
		return self.going_home(percepts)