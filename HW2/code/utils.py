########################################################
# IMPORTS
########################################################
import random
########################################################
# FUNCTION DEFINITIONS
########################################################
def generate_n_queens_states(n_queens=8, n_states=100):
    random_states = []
    for state in range(n_states):
        s = tuple(random.randint(0, n_queens-1) for q in range(n_queens))
        random_states.append(s)
    return random_states

def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items

def argmax_random_tie(neighbors, key=lambda x: x):
    return max(shuffled(neighbors), key=key)

def argmin_random_tie(neighbors, key=lambda x: x):
    return min(shuffled(neighbors), key=key)
