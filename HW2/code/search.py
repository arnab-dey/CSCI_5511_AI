########################################################
# IMPORTS
########################################################
from utils import argmax_random_tie, argmin_random_tie
import random
import numpy as np
import sys
########################################################
# CLASS DEFINITIONS
########################################################
class N_queens_problem:
    def __init__(self, N, initial, goal=None):
        self.N = N
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """ This function returns all possible actions for all queens.
        Returns list of tuples where each tuple = (row where queen Q can be moved next, Q)"""
        act = []
        for q in range(self.N):
            for r in range(self.N):
                if r != state[q]:
                    act.append(tuple([r, q]))
        return act

    def random_action(self, state):
        """ This function randomly selects an action """
        queen = random.randint(0, self.N-1)  # Choose a random queen to move
        move = random.choice([i for i in range(self.N) if i != state[queen]])
        return [tuple([move, queen])]

    def conflict(self, row_1, col_1, row_2, col_2):
        """ Returns True if there is any conflict """
        return (row_1 == row_2 or  # same row
                col_1 == col_2 or  # same column
                row_1 - col_1 == row_2 - col_2 or  # same \ diagonal
                row_1 + col_1 == row_2 + col_2)  # same / diagonal

    def conflicted(self, state, row, col):
        """ Checks if placing a queen at the row and col in the board
        results into conflict with any queens currently on the board"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def h(self, state):
        """ Returns total number of conflicts """
        n_conflicts = 0
        for (r_1, c_1) in enumerate(state):
            for (r_2, c_2) in enumerate(state):
                if (r_1, c_1) != (r_2, c_2):
                    n_conflicts += self.conflict(r_1, c_1, r_2, c_2)
        return n_conflicts

    def goal_test(self, state):
        if state[-1] == -1:
            return False
        else:
            return not any(self.conflicted(state, state[c], c)
                           for c in range(len(state)))

    def result(self, state, q_row_pair):
        """ Returns new state after placing a queen at the location
        given in the tuple q_row_pair """
        col = q_row_pair[1]
        new = list(state[:])
        new[col] = q_row_pair[0]
        return tuple(new)

    def value(self, state):
        """ Returns number of conflicts """
        return self.h(state)

    def visualize(self, state):
        """ To visualize the board """
        for place in range(self.N):
            for q in range(self.N):
                if (place == state[q]):
                    print('Q', end=' ')
                else:
                    print('0', end=' ')
            print()

########################################################
# Node class contains the implementation of each node
# of the search graphs. Contains methods to create
# child nodes, keep track of paths from root node
########################################################
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def child_node(self, problem, action):
        """ This function creates a child node for the given problem by executing the given action """
        next_state = problem.result(self.state, action)
        next_node = None
        if (None is not next_state):
            next_node = Node(next_state, self, action)
        return next_node

    def expand(self, problem):
        """ This function returns a list of all child nodes created by executing all possible actions
        from a given state """
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def random_expand(self, problem):
        """ This function returns a list of all child nodes created by executing all possible actions
        from a given state """
        return [self.child_node(problem, action) for action in problem.random_action(self.state)]

    def path(self):
        """ Return a list of nodes forming the path from the root to this node. """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def solution(self):
        """ Return the sequence of actions to go from the root to this node. """
        return [node.action for node in self.path()[1:]]

    def __lt__(self, node):
        # return self.decode_state(self.state) < self.decode_state(node.state)
        return self.path_cost < node.path_cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
########################################################
# SEARCH FUNCTION DEFINITIONS
########################################################
def hillclimb_sa(problem):
    """ This function implements steepest ascent hill climb search """
    # Get the initial node
    current = Node(problem.initial)
    n_iteration = 0
    while True:
        if (True == problem.goal_test(current.state)):
            return current.state, n_iteration
        n_iteration += 1
        neighbors = current.expand(problem)
        if not neighbors:
            break
        # Select neighbor that have minimum number of attacked queens
        neighbor = argmin_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) >= problem.value(current.state):
            break
        current = neighbor
    return current.state, n_iteration

def hillclimb_fc(problem):
    """ This function implements first choice hill climbing """
    def get_random_better_successor(n_queens, current):
        """ This function implements a version of code to
        generate random successor. It shuffles Queens to choose and
        also shuffles available rows to move them. We iterate over this shuffled queens and rows.
        This function guarantees to find a best state if there is any"""
        queens = np.arange(n_queens)
        random.shuffle(queens)
        is_better_state_found = False
        is_any_better_state = False
        better_state = current.state
        for q in queens:
            if (True == is_better_state_found):
                break
            rows = [x for x in range(n_queens)]
            rows.pop(current.state[q])
            random.shuffle(rows)
            for row in rows:
                next_state = problem.result(current.state, tuple([row, q]))
                if problem.value(next_state) < problem.value(current.state):
                    is_better_state_found = True
                    is_any_better_state = True
                    better_state = next_state
                    break
        if (False == is_any_better_state):
            return current
        return Node(better_state)
    def get_random_successor_2(state):
        """ This is another implementation to get a random successor.
        It first generates all possible successors and then randomly chooses one.
        This cannot guarantee to find a better state even if there is any.
        Ideally we need to put a upper bound on how many time we wish to retry
        successor generation until we find a better one."""
        neighbors = current.expand(problem)
        if not neighbors:
            return current
        next_choice = random.choice(neighbors)
        return next_choice
    n_rounds = sys.maxsize
    rounds = 0
    # Get the initial node
    current = Node(problem.initial)
    n_retry = 200  # Max number of trials in generating a neighbor better than current node
    retry = 0
    while True:
        if problem.goal_test(current.state):
            return current.state, rounds
        if (rounds >= n_rounds):
            return current.state, rounds
        next_choice = current.random_expand(problem)[0]
        if problem.value(next_choice.state) >= problem.value(current.state):
            retry += 1
            if (retry > n_retry):
                return current.state, rounds
            continue
        current = next_choice
        retry = 0
        rounds += 1

def sim_anneal(problem):
    """ This function implements simulated annealing search"""
    def schedule(T):
        """ This schedule function implements a gradually decaying function
        given by 20*e^(-0.005*t)"""
        reduction_factor = 0.005
        gain = 20
        return gain*np.exp(-reduction_factor*T)
    def probability(delta_e, T):
        """ This function returns a probability by implementing the function
        e^(delta_e/T) and comparing it with samples from
        uniform probability distribution between [0,1]"""
        exp = np.exp(delta_e/T)
        return np.random.uniform() < exp
    """ Actual function starts from here """
    current = Node(problem.initial)
    rounds = 0
    for t in range(sys.maxsize):
        if (True == problem.goal_test(current.state)):
            return current.state, rounds
        # Get the current temperature
        T = schedule(t)
        eps = 1e-4  # To avoid division by zero
        if (0 == T) or (eps >= T):
            return current.state, rounds
        # Randomly generate one successor
        next_choice = current.random_expand(problem)[0]
        if not next_choice:
            return current.state, rounds
        # Calculate change in energy
        delta_e = problem.value(current.state)-problem.value(next_choice.state)
        # Make move
        if ((delta_e > 0) or (probability(delta_e, T))):
            current = next_choice
        rounds += 1

