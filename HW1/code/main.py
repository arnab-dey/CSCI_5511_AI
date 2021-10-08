########################################################
# IMPORTS
########################################################
import search
import sys
import time
########################################################
# MAIN CODE STARTS HERE
########################################################
# First check if there is an argument
initial_state = 120843765  # Default initial state
goal_state = 123804765  # Goal state given in the problem
if (len(sys.argv) < 2):
    print('Initial state not provided. Setting to default...')
else:
    if (len(sys.argv[1]) > 9):
        print('Invalid initial state. Setting to default...')
    else:
        initial_state = int(sys.argv[1])
print('The initial state is')
search.visualize(search.Problem.encode_state(initial_state))
print('The goal state is')
search.visualize(search.Problem.encode_state(goal_state))
########################################################
# ITERATIVE DEEPENING
########################################################
# Create the problem
problem = search.Problem(initial=initial_state, goal=goal_state)
# Run iterative deepening
print('###############################')
print('# Starting iterative deepening...')
print('###############################')
start = time.monotonic()
node = search.iterative_deepening(problem)
elapsed_time = time.monotonic()-start
# Print solution
if (None is node):
    print('No solution found')
else:
    print('Total moves = ', len(node.solution()))
    print('Moves to reach the goal state using iterative deepening:')
    print(node.solution())
print('Time taken = ', elapsed_time, ' sec')
print('###############################')
########################################################
# ASTAR WITH NUM_WRONG_TILES
########################################################
print('###############################')
print('# Starting ASTAR with num_wrong_tiles...')
print('###############################')
start = time.monotonic()
node = search.astar(problem, problem.num_wrong_tiles)
elapsed_time = time.monotonic()-start
# Print solution
if (None is node):
    print('No solution found')
else:
    print('Total moves = ', len(node.solution()))
    print('Moves to reach the goal state using astar with num wrong tiles:')
    print(node.solution())
print('Time taken = ', elapsed_time, ' sec')
print('###############################')
########################################################
# ASTAR WITH MANHATTAN DISTANCE
########################################################
print('###############################')
print('# Starting ASTAR with manhattan distance...')
print('###############################')
start = time.monotonic()
node = search.astar(problem, problem.manhattan_distance)
elapsed_time = time.monotonic()-start
# Print solution
if (None is node):
    print('No solution found')
else:
    print('Total moves = ', len(node.solution()))
    print('Moves to reach the goal state using astar with manhattan distance:')
    print(node.solution())
print('Time taken = ', elapsed_time, ' sec')
print('###############################')