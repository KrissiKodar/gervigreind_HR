import collections
import heapq
import time
import copy


WHITE, BLACK, EMPTY = "W", "B", " "

class Evaluations:

    # inform the heuristics about the environment, needs to be called before the first call to eval()
    def init(self, env):
        self.env = env

    # return an estimate of the remaining cost of reaching a goal state from state s
    def eval(self, s):
        raise NotImplementedError()

######################
# 100 if win
# -100 if lose
# 0 if draw
# most advanced black piece - most advanced white piece
class SimpleEvaluation(Evaluations):
    def eval(self, state, player, winner=None):
        k = 0
        #legal_moves = self.env.get_legal_moves(state)
        height = self.env.height - 1
        
        if player == "white":
            if winner == WHITE:
                return 100
            elif winner == BLACK:
                return -100
            elif winner == 0: #draw
                return 0
            
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k += height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k -= height - idx
                    break
        else:
            if winner == WHITE:
                return -100
            elif winner == BLACK:
                return 100
            elif winner == 0: #draw
                return 0
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k -= height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k += height - idx
                    break
        return k

# same as SimpleEvaluation but counts white and black pieces
# and takes the difference of the number of pieces
class Evaluation_v1(Evaluations):
    def eval(self, state, player, winner=None):
        k = 0
        #legal_moves = self.env.get_legal_moves(state)
        height = self.env.height - 1
        
        if player == "white":
            if winner == WHITE:
                return 100
            elif winner == BLACK:
                return -100
            elif winner == 0: #draw
                return 0
            
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k += height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k -= height - idx
                    break
            # count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(WHITE)
                k -= i.count(BLACK)
        else:
            if winner == WHITE:
                return -100
            elif winner == BLACK:
                return 100
            elif winner == 0: #draw
                return 0
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k -= height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k += height - idx
                    break
            #count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(BLACK)
                k -= i.count(WHITE)
        return k


# same as SimpleEvaluation but counts attacking moves
# also wants to kill as many pieces as possible
class Evaluation_v2(Evaluations):
    def eval(self, state, player, winner=None):
        k = 0
        
        n_friendly_attacks, n_opponent_attacks = self.env.get_n_attacking_moves(state)
        
        height = self.env.height - 1
        k += n_friendly_attacks
        #k -= n_opponent_attacks

        if player == "white":
            if winner == WHITE:
                return 100
            elif winner == BLACK:
                return -100
            elif winner == 0: #draw
                return 0
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k += height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k -= height - idx
                    break
            # count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(WHITE)
                k -= i.count(BLACK)
        else:
            if winner == WHITE:
                return -100
            elif winner == BLACK:
                return 100
            elif winner == 0: #draw
                return 0
            for idx, i in enumerate(reversed(state.board)):
                if WHITE in i:
                    k -= height - idx
                    break    
            for idx, i in enumerate(state.board):
                if BLACK in i:
                    k += height - idx
                    break
            #count "WHITE" and "BLACK" in state.board
            for i in state.board:
                k += i.count(BLACK)
                k -= i.count(WHITE)
        return k



# TODO: implement more and better evaluation functions


########################################################


class SearchAlgorithm:
    evaluations = None

    def __init__(self, evaluations):
        self.evaluations = evaluations

    # searches for a goal state in the given environment, starting in the current state of the environment,
    # stores the resulting plan and keeps track of nb. of node expansions, max. size of the frontier and cost of best solution found 
    def do_search(self, env):
        raise NotImplementedError()

    # returns the plan found, the last time do_search() was executed
    def get_plan(self):
        raise NotImplementedError()

    # returns the number of node expansions of the last search that was executed
    def get_nb_node_expansionss(self):
        raise NotImplementedError()

    # returns the maximal size of the frontier of the last search that was executed
    def get_max_frontier_size(self):
        raise NotImplementedError()

    # returns the cost of the plan that was found
    def get_plan_cost(self):
        raise NotImplementedError()
    
    def get_eval(self, state, player, the_winner):
        return self.evaluations.eval(state, player, the_winner)

class MiniMax(SearchAlgorithm):

    def __init__(self, evaluation):
        super().__init__(evaluation)


    def init_evaluation(self, env, play_clock):
        self.evaluations.init(env)
        self.n_expansions = 0
        self.play_clock = play_clock
        return
    
    def minimax_search(self, game, state, depth):
        #player = state.white_turn
        value, move = self.max_value(game, state, depth)
        print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth):
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v, move = float('-inf'), float('-inf')
        self.n_expansions += 1
        for a in game.get_legal_moves(state):
            game.move(state, a)
            v2, a2 = self.min_value(game, game.current_state, depth-1)
            if v2 > v:
                v, move = v2, a
            game.undo_move(game.current_state, a)
        return v, move
    
    def min_value(self, game, state, depth):
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v, move = float('+inf'), float('+inf')
        self.n_expansions += 1
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
    
    def get_nb_state_expansions(self):
        return self.n_expansions

class AlphaBeta(SearchAlgorithm):

    def __init__(self, evaluation):
        super().__init__(evaluation)

    def init_evaluation(self, env, play_clock):
        self.evaluations.init(env)
        self.n_expansions = 0
        self.play_clock = play_clock
        return
    
    def alphabeta_search(self, game, state, depth):
        value, move = self.max_value(game, state, depth, float('-inf'), float('+inf'))
        print("VALUE: ", value)
        return move

    def max_value(self, game, state, depth, alpha, beta):
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('-inf')
        move = None
        self.n_expansions += 1
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
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('+inf')
        move = None
        self.n_expansions += 1
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
    
    def get_nb_state_expansions(self):
        return self.n_expansions

class AlphaBeta_iterative_deepening(SearchAlgorithm):

    def __init__(self, evaluation):
        super().__init__(evaluation)

    def init_evaluation(self, env, play_clock):
        self.evaluations.init(env)
        self.n_expansions = 0
        self.play_clock = play_clock
        return
    
    def alphabeta_search_iterative_deepening(self, game, state, depth):
        move_order = [[] for i in range(depth)]
        for i in range(1, depth+1):
            value, move = self.max_value(game, state, i, float('-inf'), float('+inf'), move_order, 0)
            print("move: ", move)
            print("VALUE: ", value)
            if value == 100:
                return move
        return move

    def max_value(self, game, state, depth, alpha, beta, move_order, move_order_index):
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('-inf')
        if move_order[move_order_index] == []:
            move_order[move_order_index] = game.get_legal_moves(state)
        """ print("INSIDE MAX")
        print("move_order[", move_order_index, "]: ", move_order[move_order_index])
        print("depth: ", depth)
        print() """
        self.n_expansions += 1
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
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('+inf')
        if move_order[move_order_index] == []:
            move_order[move_order_index] = game.get_legal_moves(state)
        """ print("INSIDE MIN")
        print("move_order[", move_order_index, "]: ", move_order[move_order_index])
        print("depth: ", depth)
        print() """
        self.n_expansions += 1
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
    
    
    def get_nb_state_expansions(self):
        return self.n_expansions

class AlphaBeta_iterative_deepening_new(SearchAlgorithm):

    def __init__(self, evaluation):
        super().__init__(evaluation)

    def init_evaluation(self, env, play_clock):
        self.evaluations.init(env)
        self.n_expansions = 0
        self.play_clock = play_clock
        return
    
    def alphabeta_search_iterative_deepening(self, game, state, depth):
        # this copy is only for the TimeoutError
        # that is, if the time limit is reached, then we dont have to undo all the moves
        # to get back to the original state
        game_copy = copy.deepcopy(game)
        try:
            for i in range(1, depth+1):
                t_start_iteration = time.time()
                value, move = self.max_value(game_copy, game_copy.current_state, i, float('-inf'), float('+inf'))
                t_end_iteration= time.time()
                print(f"search time: {t_end_iteration-t_start_iteration} seconds for depth {i}")
                print("move: ", move)
                print("VALUE: ", value)
                if value == 100:
                    return move
        except TimeoutError:
            print("TIMEOUT")
            print("best move yet: ", move)
            return move
        return move

    def max_value(self, game, state, depth, alpha, beta):
        if time.time() - self.t_start > self.play_clock-0.05:
            print(time.time() - self.t_start)
            raise TimeoutError
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('-inf')
        self.n_expansions += 1
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
        if time.time() - self.t_start > self.play_clock-0.05:
            print(time.time() - self.t_start)
            raise TimeoutError
        game_over, winner = game.is_terminal(state)    
        if game_over:
            return super().get_eval(state, self.player, winner), None
        if depth == 0:
            return super().get_eval(state, self.player, winner), None
        v = float('+inf')
        self.n_expansions += 1
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
        self.t_start = time.time()
        return self.alphabeta_search_iterative_deepening(env, env.current_state, depth)
    
    
    def get_nb_state_expansions(self):
        return self.n_expansions


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