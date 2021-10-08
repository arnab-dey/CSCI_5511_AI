########################################################
# IMPORTS
########################################################
import search
import utils
########################################################
# MAIN CODE STARTS HERE
########################################################
########################################################
# Variables
########################################################
n_queens = 8  # Total number of queens
n_init_states = 1000  # Number of random initial states to generate
itr_sa = 0
sol_count_sa = 0
itr_fc = 0
sol_count_fc = 0
itr_sim_ann = 0
sol_count_sim_ann = 0
itr = 0
########################################################
# Generate initial states
########################################################
initial_states = utils.generate_n_queens_states(n_queens, n_init_states)
# Run the search algorithms for each of the random initial states
for s in range(len(initial_states)):
    queens_problem = search.N_queens_problem(n_queens, initial_states[s])
    # Hill climb steepest ascent
    sol_sa, itr = search.hillclimb_sa(queens_problem)
    if (True == queens_problem.goal_test(sol_sa)):
        itr_sa += itr
        sol_count_sa += 1
    # Hill climb first choice
    sol_fc, itr = search.hillclimb_fc(queens_problem)
    if (True == queens_problem.goal_test(sol_fc)):
        itr_fc += itr
        sol_count_fc += 1
    # Simulated annealing
    sol_sim_ann, itr = search.sim_anneal(queens_problem)
    if (True == queens_problem.goal_test(sol_sim_ann)):
        itr_sim_ann += itr
        sol_count_sim_ann += 1
########################################################
# HILL CLIMB SA STATS
########################################################
print('############################')
print('# HILL CLIMB SA STATS')
print('############################')
print('SA: Accuracy = ', sol_count_sa*100/n_init_states, ' %')
if (sol_count_sa != 0):
    print('SA: average steps = ', itr_sa/sol_count_sa)
########################################################
# HILL CLIMB FC STATS
########################################################
print('############################')
print('# HILL CLIMB FC STATS')
print('############################')
print('FC: Accuracy = ', sol_count_fc*100/n_init_states, ' %')
if (sol_count_fc != 0):
    print('Hill climb FC average = ', itr_fc/sol_count_fc)
########################################################
# SIMULATED ANNEALING STATS
########################################################
print('############################')
print('# SIMULATED ANNEALING STATS')
print('############################')
print('SIM ANN: Accuracy = ', sol_count_sim_ann*100/n_init_states, ' %')
if (sol_count_sim_ann != 0):
    print('Hill climb SIM ANN average = ', itr_sim_ann/sol_count_sim_ann)
