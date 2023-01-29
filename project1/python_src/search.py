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
        h = state.get_legal_moves()
        # sum of y coordinates(y2)
        h = sum([x[3] for x in h])	
        return h