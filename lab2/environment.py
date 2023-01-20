from enum import IntEnum
import random
import itertools

##############

class Orientation(IntEnum):
  NORTH = 0
  EAST = 1
  SOUTH = 2
  WEST = 3

  # this allows things like: Orientation.NORTH + 1 == Orientation.EAST
  def __add__(self, i):
    orientations = list(Orientation)
    return orientations[(int(self) + i) % 4]

  def __sub__(self, i):
    orientations = list(Orientation)
    return orientations[(int(self) - i) % 4]

##############

class State:
  # Note, that you do not necessarily have to use this class if you find a
  # different data structure more useful as state representation.

  # TODO: add other attributes that store necessary information about a state of the environment
  #       Only information that can change over time should be kept here.
  #turned_on = False

  def __init__(self, turned_on = False, position = (0,0), dirts_left = (), orientation = Orientation.NORTH):
  # TODO: add other attributes that store necessary information about a state of the environment
    self.turned_on = turned_on
    self.position = position
    self.dirts_left = dirts_left
    self.orientation = orientation

  def __str__(self):
    # TODO: modify as needed
    return f"State(turned_on={self.turned_on}, position={self.position}, dirts_left={self.dirts_left}, orientation={self.orientation})"

  def __hash__(self):
    # TODO: modify as needed
   return hash((self.turned_on, self.position, self.dirts_left, self.orientation))

  def __eq__(self, other):
    # TODO: modify as needed
    # are the attributes of this state the same as the attributes of the other state?
    #return self.turned_on == other.turned_on and self.position == other.position and self.dirts_left == other.dirts_left and self.orientation == other.orientation
    return hash(self) == hash(other) 

##############

class Environment:
  # TODO: add other attributes that store necessary information about the environment
  #       Information that is independent of the state of the environment should be here.

  def __init__(self, width=0, height=0, nb_dirts=0):
    self._width = width
    self._height = height
    # TODO: randomly initialize an environment of the given size
    # That is, the starting position, orientation and position of the dirty cells should be (somewhat) random.
    # for example as shown here:
    # generate all possible positions
    self.all_positions = list(itertools.product(range(1, self._width+1), range(1, self._height+1))) # list of tuples
    # randomly choose a home location
    self.home = random.choice(self.all_positions) # tuple
    # randomly choose locations for dirt
    self.dirts = random.sample(self.all_positions, nb_dirts) # list

  def get_initial_state(self):
    # TODO: return the initial state of the environment
    return State(False, self.home, tuple(self.dirts), Orientation.NORTH) # immutable for hash

  def move(self, state):
    # return position after moving forward
    x = state.position[0]
    y = state.position[1]
    if Orientation.NORTH == state.orientation:
      return (x, y+1)
    elif Orientation.EAST == state.orientation:
      return (x+1, y)
    elif Orientation.SOUTH == state.orientation:
      return (x, y-1)
    elif Orientation.WEST == state.orientation:
      return (x-1, y)
  
  def get_legal_actions(self, state):
    actions = []
    # TODO: check conditions to avoid useless actions
    if not state.turned_on:
      actions.append("TURN_ON")
    else:
      if state.position == self.home: # should be only possible when agent has returned home
        actions.append("TURN_OFF")
      if state.position in self.dirts: 
        actions.append("SUCK")
      if self.move(state) in self.all_positions: # should be only possible when next position is inside the grid (avoid bumping in walls)
        actions.append("GO")
      actions.append("TURN_LEFT")
      actions.append("TURN_RIGHT")
    return actions

  def get_next_state(self, state, action):
    # TODO: add missing actions
    if action == "TURN_ON":
      return State(True, state.position, state.dirts_left, state.orientation)
    elif action == "TURN_OFF":
      return State(False, state.position, state.dirts_left, state.orientation)
    elif action == "TURN_LEFT":
      return State(state.turned_on, state.position, state.dirts_left, state.orientation-1)
    elif action == "TURN_RIGHT":
      return State(state.turned_on, state.position, state.dirts_left, state.orientation+1)
    elif action == "GO":
      return State(state.turned_on, self.move(state), state.dirts_left, state.orientation)
    elif action == "SUCK":
      new_dirts_left = tuple(filter(lambda x: x != state.position, state.dirts_left))
      return State(state.turned_on, state.position, new_dirts_left, state.orientation)
    else:
      raise Exception("Unknown action %s" % str(action))

  def get_cost(self, state, action):
    # TODO: return correct cost of each action
    if action == "TURN_OFF":
      D = len(self.dirts)
      if state.position == self.home:
        return 1 + 50*D
      else:
        return 100 + 50*D
    if action == "SUCK":
      if state.position not in self.dirts:
        return 5
      else:
        return 1
    # all other actions have cost 1
    return 1
  
  def is_goal_state(self, state):
    # TODO: correctly implement the goal test
    # if the agent is at home and there are no more dirty cells, the goal is reached
    if state.position == self.home and len(state.dirts_left) == 0 and not state.turned_on:
      return True
    #return not state.turned_on

##############

def expected_number_of_states(width, height, nb_dirts):
  # TODO: return a reasonable upper bound on number of possible states
  n_grid_cells = width * height
  expected_n_states = 4*n_grid_cells*(2**nb_dirts)+4*2**nb_dirts
  #expected_n_states = (n_grid_cells+1)*(2**(nb_dirts+2)) # shorter version
  return expected_n_states
