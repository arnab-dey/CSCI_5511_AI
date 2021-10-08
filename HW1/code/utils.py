########################################################
# IMPORTS
########################################################
import heapq
########################################################
# CLASS DEFINITIONS
########################################################
########################################################
# AIMA books version of Priority queue.
########################################################
class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

########################################################
# Problem class contains the 8-puzzle problem itself
# It has methods for state representation, actions,
# result of action and heuristic functions required
# for informed search
########################################################
class Problem:
    def __init__(self, initial, goal):
        """ Initial and goal states are NOT encoded """
        self.initial = self.encode_state(initial)
        self.goal = self.encode_state(goal)

    @staticmethod
    def encode_state(decoded_state):
        """ This function encodes the states represented by the flattened
        version of the 8-puzzle matrix to a single integer. It uses number representation
        with base 9. For example, for the board state,
        +-------
        + 1 2 . +
        + 8 4 3 +
        + 7 6 5 +
        the original state is 120843765. The encoding is done as follows:
        encoded_state = 1x9^8 + 2x9^7 + 0x9^6 + 8x9^5 + 4x9^4 + 3x9^3 + 7x9^2 + 6x9^1 + 5x9^0"""
        encoded_state = 0
        base = 1
        while (0 != decoded_state):
            encoded_state += (decoded_state % 9) * base
            decoded_state = int(decoded_state / 9)
            base *= 10
        return encoded_state

    @staticmethod
    def decode_state(encoded_state):
        """ This function decodes the states represented by an integer
        and returns flattened version of 8 puzzle matrix. For example,
        120843765 is returned if the encoded state corresponds to
        +-------
        + 1 2 . +
        + 8 4 3 +
        + 7 6 5 +
        """
        decoded_state = 0
        base = 1
        while (encoded_state):
            last_digit = encoded_state % 10
            encoded_state = int(encoded_state / 10)
            decoded_state += last_digit * base
            base *= 9
        return decoded_state

    def goal_test(self, state):
        """ This function checks if goal is reached """
        return self.goal == state

    def actions(self, state):
        """ This function returns the possible actions from a given state
        U = Move a tile up into the blank position
        D = Move a tile down into the blank position
        L = Move a tile to left into the blank position
        R = Move a tile to right into the blank position. """
        return ['U', 'D', 'L', 'R']

    def result(self, state, action):
        """ This function executes the given action at a given state and returns next state
        as a result of this action. It takes encoded state and returns the encoded next state """
        # first decode state
        decoded_state = self.decode_state(state)
        str_decoded_state = str(decoded_state)
        if (len(str_decoded_state) < 9):
            str_decoded_state = '0'+str_decoded_state
        blank_pos = str_decoded_state.index('0')
        str_next_state = str_decoded_state
        if (action == 'U'):
            if (blank_pos <= 5):
                str_next_state = str_decoded_state[0:blank_pos]+str_decoded_state[blank_pos+3]\
                                 +str_decoded_state[blank_pos+1:blank_pos+3]+'0'\
                                 +str_decoded_state[blank_pos+4:]
        elif (action == 'D'):
            if (blank_pos >= 3):
                str_next_state = str_decoded_state[0:blank_pos-3] + '0' + str_decoded_state[blank_pos-2:blank_pos] \
                                 + str_decoded_state[blank_pos-3] + str_decoded_state[blank_pos + 1:]
        elif (action == 'L'):
            if (blank_pos != 2 and blank_pos != 5 and blank_pos != 8):
                str_next_state = str_decoded_state[0:blank_pos] + str_decoded_state[blank_pos+1] \
                                + '0' + str_decoded_state[blank_pos+2:]
        else:
            if (blank_pos != 0 and blank_pos != 3 and blank_pos != 6):
                str_next_state = str_decoded_state[0:blank_pos-1] + '0' + str_decoded_state[blank_pos-1] \
                                 + str_decoded_state[blank_pos + 1:]
        encoded_next_state = self.encode_state(int(str_next_state))
        return encoded_next_state

    def path_cost(self, c, state1, action, state2):
        """ This function returns the path cost to reach to state2 from state2 executing the given action
        For this assignment I am using equal path cost of 1 """
        return c+1

    def num_wrong_tiles(self, state):
        """ This is a heuristic function that can be used for informed search. This function returns
        how many tiles in the 8-puzzle are misplaced when compared to the goal state """
        n_wrong_tiles = 0
        str_node_state = str(Problem.decode_state(state))
        if (len(str_node_state) < 9):
            str_node_state = '0'+str_node_state
        str_goal_state = str(Problem.decode_state(self.goal))
        if (len(str_goal_state) < 9):
            str_goal_state = '0'+str_goal_state
        for i in range(len(str_node_state)):
            if str_goal_state[i] != str_node_state[i]:
                n_wrong_tiles += 1
        return n_wrong_tiles

    def manhattan_distance(self, state):
        """ This is a heuristic function that can be used for informed search. This function returns
        the summed up Manhattan distance for each tile in given state to its position in the goal state."""
        # First set coordinates in 2D
        coordinates = {0: (0, 0), 1: (1, 0), 2: (2, 0),
                       3: (0, 1), 4: (1, 1), 5: (2, 1),
                       6: (0, 2), 7: (1, 2), 8: (2, 2)}
        distance = 0
        str_state = str(self.decode_state(state))
        if (len(str_state) < 9):
            str_state = '0'+str_state
        str_goal = str(self.decode_state(self.goal))
        if (len(str_goal) < 9):
            str_goal = '0'+str_goal
        for i in str_goal:
            x_s, y_s = coordinates[str_state.index(i)]
            x_g, y_g = coordinates[str_goal.index(i)]
            distance += abs(x_s-x_g)+abs(y_s-y_g)
        return distance
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
            next_node = Node(next_state, self, action, problem.path_cost(self.path_cost,self.state,action,next_state))
        return next_node

    def expand(self, problem):
        """ This function returns a list of all child nodes created by executing all possible actions
        from a given state """
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

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