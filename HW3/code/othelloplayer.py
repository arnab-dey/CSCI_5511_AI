########################################################
# IMPORTS
########################################################
import othellogame as og
import random
import numpy as np
import copy
########################################################
# RANDOM AGENT
########################################################
static_weights = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]]
def utility(state, player, is_mobility_reqd=False):
    """This function calculates the utility value of a state.
    I am using coin parity, static weights, corner captured and terminal state by default.
    If mobility is required to be included, it can be enabled by setting the is_mobility_reqd
    argument True"""
    n_player_coins = 0
    n_opponent_coins = 0
    player_static_weight = 0
    n_player_corner = 0
    n_opponent_corner = 0
    n_player_mobility = 0
    n_opponent_mobility = 0
    K = 100
    # First get the color
    player_color = player.get_color()
    corners = [(0, 0), (0, og.SIZE - 1), (og.SIZE - 1, 0), (og.SIZE - 1, og.SIZE - 1)]
    eqv_opponent_state = og.OthelloState(state.other, state.current, copy.deepcopy(state.board_array))
    for i in range(og.SIZE):
        for j in range(og.SIZE):
            if state.board_array[j][i] == player_color:
                n_player_coins += 1
                player_static_weight += static_weights[j][i]
                if (j,i) in corners:
                    n_player_corner += 1
            elif state.board_array[j][i] != og.EMPTY:
                n_opponent_coins += 1
                player_static_weight -= static_weights[j][i]
                if (j,i) in corners:
                    n_opponent_corner += 1
            if (True == is_mobility_reqd):
                if None is not og.result(state, (i,j)):
                    n_player_mobility += 1
                if None is not og.result(eqv_opponent_state, (i,j)):
                    n_opponent_mobility += 1
    # Calculate coin parity
    coin_parity = K*(n_player_coins-n_opponent_coins)/(n_player_coins+n_opponent_coins)
    # Calculate corner utility
    corner_utility = 0
    if (n_player_corner + n_opponent_corner != 0):
        corner_utility = K * (n_player_corner - n_opponent_corner) / (n_player_corner + n_opponent_corner)
    # Calculate mobility utility
    mobility_utility = 0
    if (n_player_mobility+n_opponent_mobility != 0):
        mobility_utility = K*(n_player_mobility-n_opponent_mobility)/(n_player_mobility+n_opponent_mobility)
    # Check terminal state utility
    terminal_utility = 0
    if (og.terminal_test(state)):
        if (n_player_coins > n_opponent_coins):
            terminal_utility = 1000
        else:
            terminal_utility = -1000
    # Now return weighted utility value
    total_utility = (3*coin_parity+1*mobility_utility+2*corner_utility)/600+player_static_weight+terminal_utility
    return total_utility

class RandomPlayer(og.OthelloPlayerTemplate):
    """ This is a random player that randomly chooses one of
    the available legal moves"""
    def make_move(self, state):
        legals = og.actions(state)
        return random.choice(legals)

class MinimaxPlayer(og.OthelloPlayerTemplate):
    """This is a player that executes minimax algorithm"""
    def __init__(self, mycolor, depth_limit):
        super().__init__(mycolor)
        self.depth_limit = depth_limit

    def cutoff_test(self, state, depth):
        cutoff = False
        if (depth > self.depth_limit) or (og.terminal_test(state)):
            cutoff = True
        return cutoff

    def max_value(self, state, depth):
        if (self.cutoff_test(state, depth)):
            return utility(state, self)
        v = -np.inf
        legal_actions, legal_states = og.get_legal_actions_state(state)
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = max(v, self.min_value(s, depth+1))
        return v

    def min_value(self, state, depth):
        if (self.cutoff_test(state, depth)):
            return utility(state, self)
        v = np.inf
        legal_actions, legal_states = og.get_legal_actions_state(state)
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = min(v, self.max_value(s, depth+1))
        return v

    def make_move(self, state):
        legal_actions, legal_states = og.get_legal_actions_state(state)
        best_score = -np.inf
        best_action = None
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = self.min_value(s, 1)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action

class AlphabetaPlayer(og.OthelloPlayerTemplate):
    """This is a player that executes Alpha-Beta pruning"""
    def __init__(self, mycolor, depth_limit):
        super().__init__(mycolor)
        self.depth_limit = depth_limit

    def cutoff_test(self, state, depth):
        cutoff = False
        if (depth > self.depth_limit) or (og.terminal_test(state)):
            cutoff = True
        return cutoff

    def max_value(self, state, alpha, beta, depth):
        if self.cutoff_test(state, depth):
            return utility(state, self)
        v = -np.inf
        legal_actions, legal_states = og.get_legal_actions_state(state)
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = max(v, self.min_value(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if self.cutoff_test(state, depth):
            return utility(state, self)
        v = np.inf
        legal_actions, legal_states = og.get_legal_actions_state(state)
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = min(v, self.max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alpha_beta_depth_limited(self, state):
        best_score = -np.inf
        beta = np.inf
        best_action = None
        legal_actions, legal_states = og.get_legal_actions_state(state)
        for i, (a,s) in enumerate(zip(legal_actions,legal_states)):
            v = self.min_value(s, best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action

    def make_move(self, state):
        return self.alpha_beta_depth_limited(state)
