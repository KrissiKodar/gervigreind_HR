from agent import Agent
from environment import Environment
import random
from search import *

import time
# my main agent class

class MyAgent(Agent):
    search_algorithm = None
    
    def __init__(self, search_algorithm) -> None:
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0
        self.env = None
        self.search_algorithm = search_algorithm
    

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here
        self.env = Environment(width, height)
        
        self.search_algorithm.init_heuristic(self.env) # initialize the search algorithm
        
        self.depth = 5 # set the depth of the search algorithm
 
    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            last_action = (x - 1 for x in last_action)
            self.env.move(self.env.current_state, last_action)
            #print()
            #print(self.env.current_state)
            #print()
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move
            
            #x1, y1, x2, y2 = self.get_best_move()
            print()
            print(self.env.current_state)
            print()
            t_start = time.time()
            ultra_move, n_expansions = self.search_algorithm.do_search(self.env, self.role, self.depth)
            t_end = time.time()
            time_for_move = t_end - t_start
            print("Move calculation time_for_move: ", time_for_move)
            print("ultimate move: ", ultra_move)
            print("moves: ", self.env.get_legal_moves(self.env.current_state))
            print("n_expansions: ", n_expansions)
            if time_for_move != 0: print("n_expansion_per_second: ", n_expansions/(time_for_move))
            x1, y1, x2, y2 = ultra_move[0], ultra_move[1], ultra_move[2], ultra_move[3]
            return "(move " + " ".join(map(str, [x1+1, y1+1, x2+1, y2+1])) + ")"
        else:
            return "noop"





class RandomLegalAgent(Agent):
    search_algorithm = None
    
    def __init__(self, search_algorithm) -> None:
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0
        self.env = None
        self.search_algorithm = search_algorithm
    

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here
        
        self.env = Environment(width, height)
        self.search_algorithm.do_search(self.env)

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'

            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            # -1 because the environment is 0-indexed and the server is 1-indexed
            last_action = (x - 1 for x in last_action)
            self.env.move(self.env.current_state, last_action)
            print()
            print(self.env.current_state)
            print()
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move

            moves = self.env.get_legal_moves(self.env.current_state)
            # pick random move
            x1, y1, x2, y2 = random.choice(moves)
            print("moves: ", moves)
            print("current eval: ", self.search_algorithm.get_eval(self.env.current_state))
            print("my move: ", x1, y1, x2, y2)
            
            return "(move " + " ".join(map(str, [x1+1, y1+1 , x2+1, y2+1])) + ")"
        else:
            return "noop"