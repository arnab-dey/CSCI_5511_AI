########################################################
# IMPORTS
########################################################
from utils import Problem, Node, PriorityQueue
########################################################
# SEARCH FUNCTION DEFINITIONS
########################################################
def depth_first_search(problem):
    """ This is the implementation of vanilla depth first search.
    This is adapted from book. But not being used as required for the homework. """
    # Build the frontier stack
    frontier = [Node(problem.initial)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if (problem.goal_test(node.state)):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
    return None

def depth_limited_search(problem, limit=None):
    """ This function implements the depth first search algorithm.
    If limit argument is None, it is vanilla DFS otherwise providing a valid limit
    argument performs depth limited search algorithm. """
    # Check if limit is a valid integer
    if ((None is not limit) and (limit < 0)):
        limit = None
    # Build the frontier stack
    frontier = [Node(problem.initial)]
    explored = set()
    # actions_to_goal = []
    while frontier:
        if (None is not limit):
            limit = limit-1
        node = frontier.pop()
        # if (None is not node.action):
            # actions_to_goal.append(node.action)
        if (problem.goal_test(node.state)):
            return node
        if ((None is not limit) and (0 >= limit)):
            return 'cutoff'
        explored.add(node.state)
        if (None is limit) or (limit != 0):
            # is_leaf_node = True
            # for child in node.expand(problem):
            #     if child.state not in explored and child not in frontier:
            #         frontier.extend([child])
            #         is_leaf_node = False
            frontier.extend(child for child in node.expand(problem)
                            if child.state not in explored and child not in frontier)
            # if (is_leaf_node):
            #     # We hit leaf node
            #     actions_to_goal.pop()
    return None

def depth_limited_search_recursive(problem, limit=None):
    """ This is a recursive version of depth limited search.
    This is adapted from the book. """
    # Build the frontier stack
    # frontier = [Node(problem.initial)]
    explored = set()

    def recursive_dls(node, problem, limit, explored):
        if (problem.goal_test(node.state)):
            return node, explored
        elif ((None is not limit) and (limit == 0)):
            return 'cutoff', explored
        else:
            cutoff_occured = False
            explored.add(node.state)
            for child in node.expand(problem):
                if (child.state not in explored):
                    updated_limit = None if limit is None else limit-1
                    result, explored = recursive_dls(child, problem, updated_limit, explored)
                    if ('cutoff' == result):
                        cutoff_occured = True
                    elif result is not None:
                        return result, explored
            if (cutoff_occured):
                return 'cutoff', explored
            else:
                return None, explored
    node, explored = recursive_dls(Node(problem.initial), problem, limit, explored)
    return node

def iterative_deepening(problem):
    """ This function implements iterative deepening algorithm by calling depth limited search in
    a for loop """
    max_limit = 80
    for depth in range(1, max_limit):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
    return None

def best_first_search(problem, f):
    """ This function implements best first search to be used for informed search.
    For Astar algorithm, the argument f denotes f(n) = g(n)+h(n) where n is an
    instance of Node, h(n) is a heuristic function and g(n) is a cost function. Note,
    that for our homework f(.) takes a state instead of a Node. """
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if (problem.goal_test(node.state)):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar(problem, h):
    """ This function implements astar algorithm. """
    return best_first_search(problem, lambda n: n.path_cost + h(n.state))

def visualize(encoded_state):
    """ This function prints the encoded state as 8-puzzle board for
    visualization purpose. """
    n_grid_cell = 9  # As we will be working on 3x3 puzzle grid
    n_row = 3
    # First decode it
    decoded_state = Problem.decode_state(encoded_state)
    state_list = []
    while(0 != decoded_state):
        last_digit = decoded_state % 10
        decoded_state = int(decoded_state/10)
        if (0 == last_digit):
            last_digit = '.'
        state_list.insert(0, last_digit)
    if (len(state_list) != n_grid_cell):
        state_list.insert(0, '.')
        # print('Given state is invalid')
    # else:
    print('+-------------+')
    for i in range(int(n_grid_cell/n_row)):
        print('+ ', state_list[i*n_row], ' ', state_list[i*n_row+1], ' ', state_list[i*n_row+2], ' +')
    print('+-------------+')