from agent import Agent
from environment import Environment
import random
from search import *
import numpy as np

import time



# my main agent class !!!!!!!!!!
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
        
        self.search_algorithm.init_evaluation(self.env, self.play_clock) # initialize the search algorithm
        self.depth = 100 # set the depth to arbitrary high value (as we have time limit)
        self.total_time = 0
        self.state_expansion_list = []
        self.total_expansions = 0
        self.n_moves = 0
        
 
    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            #print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            last_action = (x - 1 for x in last_action)
            self.env.move(self.env.current_state, last_action)

        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            self.n_moves += 1
            # TODO: 2. run alpha-beta search to determine the best move
            

            t_move_start = time.time() 
            
            # ultra move is the output of the search algorithm!       
            ultra_move = self.search_algorithm.do_search(self.env, self.role, self.depth)
            
            n_expansions = self.search_algorithm.get_nb_state_expansions()
            t_end = time.time()
            time_for_move = t_end - t_move_start
            self.total_time += time_for_move
            
            # some print statements for seeing the progress of the agent
            # and for debugging
            
            #print("Time for move calculation", time_for_move, " s")
            #print("Total time calculating", self.total_time, " s")
            #print("ultimate move: ", ultra_move)
            #print("moves: ", self.env.get_legal_moves(self.env.current_state))
            self.total_expansions += n_expansions
            self.state_expansion_list.append(n_expansions)
            #print("state expansion list: ", self.state_expansion_list)
            #print("total state expansions so far: ", self.total_expansions)
            #print("average state expansions per search: ", np.mean(self.state_expansion_list))
            #print("average state expansions per second: ", np.mean(self.state_expansion_list)/time_for_move)
            #if self.total_time != 0: print("n_expansion_per_second: ", n_expansions/(self.total_time))
            #print()
            
            # send the move to the environment
            x1, y1, x2, y2 = ultra_move[0]+1, ultra_move[1]+1, ultra_move[2]+1, ultra_move[3]+1
            return "(move " + " ".join(map(str, [x1, y1, x2, y2])) + ")"
        else:
            self.n_moves += 1
            return "noop"
    
    def cleanup(self, last_move):
        # Code below was for documenting the matches between the different evaluation functions
        
        #print("--------------------------------------------------")
        #board_size = str(self.width) + "x" + str(self.height)
        #print("Board size: ", board_size)
        #
        #evaluation_used = str(self.search_algorithm)
        #print("evaluation used: ", evaluation_used )
        #print("role: ", self.role)
        #print("play clock: ", self.play_clock)
        #
        #av_n_state_expansions = str(np.round(np.mean(self.state_expansion_list, 0)))
        #print("average number of state expansions per search: ", av_n_state_expansions)
        #state_ex_per_sec = 0
        #if self.total_time != 0:
        #    state_ex_per_sec = str(np.round(self.total_expansions/self.total_time,1))
        #    print("State expansions per second: ", state_ex_per_sec)
        #print("total moves to finish: ", self.n_moves)
        #print("total runtime: ", self.total_time)
        ## if index 3 in last_move is 1, then black won
        #if last_move[3] == 1:
        #    winner = "black"
        #else:
        #    winner = "white"
        #print("--------------------------------------------------")
        ## put the results in results.txt, in a table like format
        #if str(self.search_algorithm) == "SimpleEvaluation":
        #    f = open("SimpleEvaluation_results.txt", "a")
        #if str(self.search_algorithm) == "TSE":
        #    f = open("TSE.txt", "a")
        #if str(self.search_algorithm) == "AMTSE":
        #    f = open("AMTSE.txt", "a")
        #if str(self.search_algorithm) == "AB_ID_TT":
        #    f = open("transposition.txt", "a")
        #
        #f.write(evaluation_used + " " + board_size + " " + str(self.role) + " " + str(self.play_clock) + " " + 
        #        av_n_state_expansions  + " " + state_ex_per_sec + " " + 
        #        str(self.n_moves) + " " + str(np.round(self.total_time,2)) + " " + winner + "\n")
        #f.close()

        return








# The agent below was exclusively used for testing everything in the beginning
# and making sure the agent was only doing legal moves
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