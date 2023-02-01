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

    def do_search(self, env):
        self.heuristics.init(env)
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