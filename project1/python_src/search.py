import collections
import heapq

WHITE, BLACK, EMPTY = "W", "B", " "

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
    def eval(self, state, player):
        k = 0
        legal_moves = self.env.get_legal_moves(state)
        height = self.env.height - 1
        # if last value of each tuple is greter than half of height increment k by 1
        # if it is equal to height then increment k by 100
        if player == "white":
            # +100 if winning
            if WHITE in state.board[height]:
                k += 100
            if BLACK in state.board[0]:
                k -= 100
            len_moves = len(legal_moves)
            k += len_moves
            if len_moves == 0:
                k -= 100
            # count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(WHITE)
                k -= i.count(BLACK)
        else:
            if WHITE in state.board[height]:
                k -= 100
            if BLACK in state.board[0]:
                k += 100
            len_moves = len(legal_moves)
            k += len_moves
            if len_moves == 0:
                k -= 100
            # count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(BLACK)
                k -= i.count(WHITE)
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
        print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v, move = float('-inf'), float('-inf')
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.min_value(game, game.current_state, depth-1)
            if v2 > v:
                v, move = v2, a
            game.undo_move(game.current_state, a)
        return v, move
    
    def min_value(self, game, state, depth):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v, move = float('+inf'), float('+inf')
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.max_value(game, game.current_state, depth-1)
            if v2 < v:
                v, move = v2, a
            game.undo_move(game.current_state, a)
        return v, move

    def do_search(self, env, player, depth):
        self.player = player
        return self.minimax_search(env, env.current_state, depth)
    
    def get_plan(self):
        return

    def get_nb_node_expansions(self):
        return

    def get_max_frontier_size(self):
        return

    def get_plan_cost(self):
        return

    def get_eval(self, state, player):
        return self.heuristics.eval(state, player)

class AlphaBeta(SearchAlgorithm):

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def EXPAND(self, problem, node, heuristic_function):
            return

    def init_heuristic(self, env):
        self.heuristics.init(env)
        return
    
    def alphabeta_search(self, game, state, depth):
        value, move = self.max_value(game, state, depth, float('-inf'), float('+inf'))
        print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth, alpha, beta):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('-inf')
        move = None
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.min_value(game, game.current_state, depth-1, alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            game.undo_move(game.current_state, a)
            if v >= beta:
                return v, move
        return v, move
    
    def min_value(self, game, state, depth, alpha, beta):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('+inf')
        move = None
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.max_value(game, game.current_state, depth-1, alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            game.undo_move(game.current_state, a)
            if v <= alpha:
                return v, move
        return v, move

    def do_search(self, env, player, depth):
        self.player = player
        return self.alphabeta_search(env, env.current_state, depth)
    
    def get_plan(self):
        return

    def get_nb_node_expansions(self):
        return

    def get_max_frontier_size(self):
        return

    def get_plan_cost(self):
        return

    def get_eval(self, state, player):
        return self.heuristics.eval(state, player)

class AlphaBeta_iterative_deepening(SearchAlgorithm):

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def EXPAND(self, problem, node, heuristic_function):
            return

    def init_heuristic(self, env):
        self.heuristics.init(env)
        return
    
    def alphabeta_search_iterative_deepening(self, game, state, depth):
        move_order = [[] for i in range(depth)]
        for i in range(1, depth+1):
            value, move = self.max_value(game, state, i, float('-inf'), float('+inf'), move_order, 0)
            print("move: ", move)
            print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth, alpha, beta, move_order, move_order_index):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('-inf')
        if move_order[move_order_index] == []:
            move_order[move_order_index] = game.get_legal_moves(state)
        print("INSIDE MAX")
        print("move_order[", move_order_index, "]: ", move_order[move_order_index])
        print("depth: ", depth)
        print()
        for a in move_order[move_order_index]:
            game.move(state, a)
            v2, a2 = self.min_value(game, game.current_state, depth-1, alpha, beta, move_order, move_order_index+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
                # move a in move_order[move_order_index] to the back
                move_order[move_order_index].remove(a)	
                move_order[move_order_index].append(a)
                
            game.undo_move(game.current_state, a)
            if v >= beta:
                return v, move
        return v, move
    
    def min_value(self, game, state, depth, alpha, beta, move_order, move_order_index):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('+inf')
        if move_order[move_order_index] == []:
            move_order[move_order_index] = game.get_legal_moves(state)
        print("INSIDE MIN")
        print("move_order[", move_order_index, "]: ", move_order[move_order_index])
        print("depth: ", depth)
        print()
        for a in move_order[move_order_index]:
            game.move(state, a)
            v2, a2 = self.max_value(game, game.current_state, depth-1, alpha, beta, move_order, move_order_index+1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
                # move a in move_order[move_order_index] to the front
                move_order[move_order_index].remove(a)	
                move_order[move_order_index].insert(0, a)	
            game.undo_move(game.current_state, a)
            if v <= alpha:
                return v, move
        return v, move

    def do_search(self, env, player, depth):
        self.player = player
        return self.alphabeta_search_iterative_deepening(env, env.current_state, depth)
    
    
    def get_plan(self):
        return

    def get_nb_node_expansions(self):
        return

    def get_max_frontier_size(self):
        return

    def get_plan_cost(self):
        return

    def get_eval(self, state, player):
        return self.heuristics.eval(state, player)


class AlphaBeta_iterative_deepening_new(SearchAlgorithm):

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def EXPAND(self, problem, node, heuristic_function):
            return

    def init_heuristic(self, env):
        self.heuristics.init(env)
        return
    
    def alphabeta_search_iterative_deepening(self, game, state, depth):
        for i in range(1, depth+1):
            value, move = self.max_value(game, state, i, float('-inf'), float('+inf'))
            print("move: ", move)
            print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth, alpha, beta):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('-inf')

        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.min_value(game, game.current_state, depth-1, alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)           
            game.undo_move(game.current_state, a)
            if v >= beta:
                return v, move
        return v, move
    
    def min_value(self, game, state, depth, alpha, beta):
        if game.is_terminal(state) or depth == 0:
            return self.get_eval(state, self.player), None
        v = float('+inf')
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.max_value(game, game.current_state, depth-1, alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)	
            game.undo_move(game.current_state, a)
            if v <= alpha:
                return v, move
        return v, move

    def do_search(self, env, player, depth):
        self.player = player
        return self.alphabeta_search_iterative_deepening(env, env.current_state, depth)
    
    
    def get_plan(self):
        return

    def get_nb_node_expansions(self):
        return

    def get_max_frontier_size(self):
        return

    def get_plan_cost(self):
        return

    def get_eval(self, state, player):
        return self.heuristics.eval(state, player)



if __name__ == "__main__":
    def A(L):
        L.append(1)
        B(L)
        return L
    def B(L):
        L.append(5)
        return L
    # make bb a list of 5 empty lists
    bb = [1,2,3,4,5]
    bb.remove(3)	
    #bb.append(3)	
    bb.insert(0, 3)
    print(bb)