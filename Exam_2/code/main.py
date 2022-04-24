#######################################################################
# IMPORTS
#######################################################################
import sat_interface
import random
def rand3cnf(m,n):
    """Problem 2.a
    m = no. of clauses
    n = no. of symbols """
    # Generate possible literals: use ASCII to convert to upper case letters
    population = [chr(65+i) for i in range(int(n))]
    is_not_unique_clauses = True
    # Keep a set for clauses so that not clause would be repeated
    conj = set()
    while is_not_unique_clauses:
        # Sample 3 literals without repetitions
        literals = random.sample(population, 3)
        clause = ""
        for literal in range(len(literals)):
            if (True == bool(random.randint(0, 1))):
                literals[literal] = "~" + literals[literal]
            clause += literals[literal] + (" " if literal != len(literals)-1 else "")
        conj.add(clause)
        if (len(conj) == int(m)):
            is_not_unique_clauses = False
    return list(conj)

def test_satisfiability(m_array,n_array, n_kbs=100):
    """Problem 2.b
    m_array = array containing values of m over which we need to iterate
    n_array = array containing values of n over which we need to iterate
    n_kbs = no. of random KBs we need to generate to compute the probability of satisfiability"""
    prob_satisfiability = []
    for m in m_array:
        for n in n_array:
            satisfiable_count = 0
            for kb in range(n_kbs):
                conj = rand3cnf(m, n)
                # Not printing the clauses to keep the output concise.
                # Please uncomment if you wish to see the clauses also
                # print('KB: ', kb, ' clauses = ', conj)
                print('m = ', m, ' n = ', n)
                prob = sat_interface.KB(conj)
                if (prob.is_satisfiable()):
                    print('KB: ', kb, ' is satisfiable')
                    satisfiable_count += 1
                else:
                    print('KB: ', kb, ' is not satisfiable')
            prob_satisfiability.append((m, n, '{:.2f}'.format(m/n), '{:.2f}'.format(satisfiable_count/n_kbs)))
    print('#### RESULTS ####')
    print('|  m   |  n  |  m/n  | Prob  |')
    for i in prob_satisfiability:
        print('| ', i[0], ' |', i[1], ' |', i[2], ' |', i[3], ' |')

#######################################################################
# MAIN CODE STARTS HERE
#######################################################################
m_array = [i for i in range(30, 80, 10)]
n_array = [i for i in range(10, 25, 5)]
test_satisfiability(m_array, n_array)


