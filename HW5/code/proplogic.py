#######################################################################
# IMPORTS
#######################################################################
import sat_interface
def tt2():
    """Variables are as follows:
    A: Amy is a truth-teller
    B: Bob is a truth-teller
    C: Cal is a truth-teller.
    Amy says, "Cal and I are truthful.": can be converted to A <-> A & C.
    Corresponding CNF is (~A | C).
    Bob says, "Cal is a liar." : can be converted to B <-> ~C.
    Corresponding CNF is (C | B) & (~B ∨ ~C).
    Cal says, "Bob speaks the truth or Amy lies." : can be converted to C <-> B | ~A.
    Corresponding CNF is (~B | C) & (A | C) & (~C | B | ~A)."""
    clauses_cnf = ["~A C",
                   "C B",
                   "~B ~C",
                   "~B C",
                   "A C",
                   "~C B ~A"]
    tt2_prob = sat_interface.KB(clauses_cnf)
    if (tt2_prob.is_satisfiable()):
        print('TT2 is satisfiable')
    else:
        print('TT2 is not satisfiable')
    if (False == tt2_prob.test_literal("A")):
        print('Amy is a liar')
    if (False == tt2_prob.test_literal("~A")):
        print('Amy is a truth-teller')
    if (False == tt2_prob.test_literal("B")):
        print('Bob is a liar')
    if (False == tt2_prob.test_literal("~B")):
        print('Bob is a truth-teller')
    if (False == tt2_prob.test_literal("C")):
        print('Cal is a liar')
    if (False == tt2_prob.test_literal("~C")):
        print('Cal is a truth-teller')

def tt3():
    """ Variables are as follows:
    A: Amy is a truth-teller
    B: Bob is a truth-teller
    C: Cal is a truth-teller.
    Amy says, "Cal is not honest." can be converted to A <-> ~C.
    Corresponding CNF is (C | A) & (~A | ~C).
    Bob says, "Amy and Cal never lie." can be converted to B <-> A & C.
    Corresponding CNF is (~A | ~C | B) & (~B | A) & (~B | C).
    Cal says, "Bob is correct". can be converted to C <-> A & C.
    Corresponding CNF is (~C | A). """
    clauses_cnf = ["C A",
                   "~A ~C",
                   "~A ~C B",
                   "~B A",
                   "~B C",
                   "~C A"]
    tt3_prob = sat_interface.KB(clauses_cnf)
    if (tt3_prob.is_satisfiable()):
        print('TT3 is satisfiable')
    else:
        print('TT3 is not satisfiable')
    if (False == tt3_prob.test_literal("A")):
        print('Amy is a liar')
    if (False == tt3_prob.test_literal("~A")):
        print('Amy is a truth-teller')
    if (False == tt3_prob.test_literal("B")):
        print('Bob is a liar')
    if (False == tt3_prob.test_literal("~B")):
        print('Bob is a truth-teller')
    if (False == tt3_prob.test_literal("C")):
        print('Cal is a liar')
    if (False == tt3_prob.test_literal("~C")):
        print('Cal is a truth-teller')

def salt():
    """Variables are as follows:
    P: Caterpillar is telling the truth.
    Q: Lizard is telling the truth.
    R: Cat is telling the truth.
    C: Caterpillar ate the salt.
    B: Lizard ate the salt.
    H: Cat ate the salt.
    ###
    CATERPILLAR: Bill the Lizard ate the salt. : can be converted to P <-> B.
    Corresponding CNF is (~B | P) & (~P | B).
    BILL THE LIZARD: That is true! : can be converted to Q <-> B.
    Corresponding CNF is (~B | Q) & (~Q | B).
    CHESHIRE CAT: I never ate the salt. : can be converted to R <-> ~H.
    Corresponding CNF is (H | R) & (~R | ~H).
    Either Caterpillar or Lizard or Cat ate the salt. : can be converted to the following:
    C <-> ~B & ~H; B <-> ~C & ~H; H <-> ~C & ~B. Corresponding CNF are:
    (B | H | C) & (~C | ~B) & (~C | ~H).
    (C | H | B) & (~B | ~C) & (~B | ~H).
    (C | B | H) & (~H | ~C) & (~H | ~B).
    At least one of them tells the truth. : can be converted to (P | Q | R).
    At least one of them lies. : can be converted to (~P | ~Q | ~R).
    """
    clauses_cnf = ["~B P", "~P B", "~B Q", "~Q B", "H R", "~R ~H", "B H C", "~C ~B", "~C ~H",
                   "C H B", "~B ~C", "~B ~H", "C B H", "~H ~C", "~H ~B",
                   "P Q R", "~P ~Q ~R"]

    salt_prob = sat_interface.KB(clauses_cnf)
    if (salt_prob.is_satisfiable()):
        print('Salt is satisfiable')
    else:
        print('Salt is not satisfiable')
    if (False == salt_prob.test_literal("C")):
        print('Caterpillar did not eat the salt')
    if (False == salt_prob.test_literal("~C")):
        print('Caterpillar ate the salt')
    if (False == salt_prob.test_literal("B")):
        print('Lizard did not eat the salt')
    if (False == salt_prob.test_literal("~B")):
        print('Lizard ate the salt')
    if (False == salt_prob.test_literal("H")):
        print('Cat did not eat the salt')
    if (False == salt_prob.test_literal("~H")):
        print('Cat ate the salt')

def golf():
    """Variables are as follows:
    A: First always tells truth.
    B: Middle always tells truth.
    C: Last always tells truth.
    Also, it is given that Tom, the best golfer of the three, always tells the truth.
    Dick sometimes tells the truth, while Harry, the worst golfer, never does. Hence, the statements are:
    The first man in line says, "The guy in the middle is Harry." : can be converted to A <-> ~B.
    Corresponding CNF is (B | A) & (~A | ~B).
    The man in the middle says, "I’m Dick." : It gives empty clause.
    The last man says, "The guy in the middle is Tom." : Can be converted to C <-> B.
    Corresponding CNF is (~B | C) & (~C | B).
    Now, only one always tells truth. : can be converted to A <-> ~B & ~C; B <-> ~A & ~C; C <-> ~A &~B.
    Corresponding CNF are:
    (B | C | A) & (~A | ~B) & (~A | ~C).
    (A | C | B) & (~B | ~A) & (~B | ~C).
    (A | B | C) & (~C | ~A) & (~C | ~B)"""
    clauses_cnf = ["B A", "~A ~B",
                   "~B C", "~C B",
                   "B C A", "~A ~B", "~A ~C",
                   "A C B", "~B ~A", "~B ~C",
                   "A B C", "~C ~A", "~C ~B"]
    golf_prob = sat_interface.KB(clauses_cnf)
    if (golf_prob.is_satisfiable()):
        print('Golf is satisfiable')
    else:
        print('Golf is not satisfiable')
    if (False == golf_prob.test_literal("A")):
        print('First does not tell truth')
    if (False == golf_prob.test_literal("~A")):
        print('First always tells truth. So, first is Tom')
    if (False == golf_prob.test_literal("B")):
        print('Middle does not tell truth. It can be either Harry or Dick')
    if (False == golf_prob.test_literal("~B")):
        print('Middle always tells truth. So, middle is Tom')
    if (False == golf_prob.test_literal("C")):
        print('Last does not tell truth. It can be either Harry or Dick')
    if (False == golf_prob.test_literal("~C")):
        print('Last always tells truth. So, last is Tom')
    if (False == golf_prob.test_literal("~A")) and (False == golf_prob.test_literal("B")):
        print('As first is Tom and Tom always tells truth, middle is Harry and last is Dick')
