import collections
import heapq

class Heuristics:

    # inform the heuristics about the environment, needs to be called before the first call to eval()
    def init(self, env):
        self.env = env

    # return an estimate of the remaining cost of reaching a goal state from state s
    def eval(self, s):
        raise NotImplementedError()

######################

class SimpleHeuristics(Heuristics):
    # bla bla bla bla!!!
    def eval(self, state):
        k = 0
        h = self.env.get_legal_moves(state)
        # this is a ist of tuples
        height = self.env.height - 1
        # if last value of each tuple is greter than half of height increment k by 1
        # if it is equal to height then increment k by 100
        for i in h:	
            if i[3] >= height/2:
                k += 1
            elif i[3] == height:
                k += 100	
        return k

########################################################

class SearchAlgorithm:
    heuristics = None

    def __init__(self, heuristics):
        self.heuristics = heuristics

    # searches for a goal state in the given environment, starting in the current state of the environment,
    # stores the resulting plan and keeps track of nb. of node expansions, max. size of the frontier and cost of best solution found 
    def do_search(self, env):
        raise NotImplementedError()

    # returns the plan found, the last time do_search() was executed
    def get_plan(self):
        raise NotImplementedError()

    # returns the number of node expansions of the last search that was executed
    def get_nb_node_expansions(self):
        raise NotImplementedError()

    # returns the maximal size of the frontier of the last search that was executed
    def get_max_frontier_size(self):
        raise NotImplementedError()

    # returns the cost of the plan that was found
    def get_plan_cost(self):
        raise NotImplementedError()



class MiniMax(SearchAlgorithm):

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def EXPAND(self, problem, node, heuristic_function):
            return

    def init_heuristic(self, env):
        self.heuristics.init(env)
        return
    
    def minimax_search(self, game, state, depth):
        #player = state.white_turn
        value, move = self.max_value(game, state, depth)
        return move

    def max_value(self, game, state, depth):
        if game.is_terminal(state):
            return self.get_eval(state), None
        v, move = float('-inf'), float('-inf')
        for a in game.get_legal_moves(state):
            v2, a2 = self.min_value(game, game.move(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move
    
    def min_value(self, game, state, depth):
        if game.is_terminal(state):
            return self.get_eval(state), None
        v, move = float('+inf'), float('+inf')
        for a in game.get_legal_moves(state):
            v2, a2 = self.max_value(game, game.move(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    def do_search(self, env):
        self.depth_counter = 0
        return
    
    
    def get_plan(self):
        return

    def get_nb_node_expansions(self):
        return

    def get_max_frontier_size(self):
        return

    def get_plan_cost(self):
        return

    def get_eval(self, state):
        return self.heuristics.eval(state)