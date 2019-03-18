import queue

'''
    apply Arc Consistency to the given list of variables
    :param Constraint constraint: constraint object against which to check arc consistency
    :param list values: list of values
    :return None, it modifies the domain of the given variable to be arc consistent
'''
# TODO arcs should not have duplicate arcs
def ac_3(csp):
    arcs = queue.Queue()

    # put arcs in the queue
    for a in csp.get_all_arcs():
        arcs.put(a)

    while not arcs.empty():
        arc = arcs.get()
        if revise(arc[0], arc[1], csp):  # revising the domain of arc[0]
            if not arc[0].domain:
                # pass
                return False
            for propagating_arc in csp.get_arcs(arc[0]):
                arcs.put(propagating_arc)

    return True


'''
    revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
    :param Variable x, y 
    :return bool eantrue iff we revised the domain of x
'''
def revise(x, y, csp):
    pruning_value = []
    biconst = csp.get_biconst(x, y)

    for value in x.domain:

        # check the unary constraint first,
        # The binary constraint covers the unary constraint
        uex = csp.get_uex(x)
        uin = csp.get_uin(x)

        if uex:
            if value in csp.get_uex(x):
                pruning_value.append(value)
        if uin:
            if value not in csp.get_uin(x):
                pruning_value.append(value)

        # now check the binary constraints
        if biconst is not None:
            prune = False
            i = csp.get_index_of_value(value)

            for j in range(csp.get_values_len()):
                if csp.get_value_by_index(j) in y.domain:  # if the value is still in y's domain
                    prune = prune or biconst[i, j]

            if not prune:
                pruning_value.append(value)

    for pv in pruning_value:
        x.prune_value(pv)

    return not not pruning_value


'''
NOTE that the Constraint object keeps all the variables. Thus it also keeps all the assignment to variables
'''
def backtrack(assignment, csp):
    if is_assignment_complete(assignment): return assignment
    var = select_unassigned_var(assignment, csp)
    for value in ordered_domain(var, assignment, csp):
        if check_value_consistency(var, value, assignment, csp):
            assignment[var] = value
            result = backtrack(assignment, csp)  # recursion call
            if result is not None:
                return result
            else:
                assignment[var] = None  # remove this assignment

    return None

def ordered_domain(var, assignment, csp):
    return var.domain


def select_unassigned_var(assignment, csp):
    for var in csp.get_all_variables():
        if assignment[var] is None:
            return var


def is_assignment_complete(assignment):
    rtn = True
    for key, value in assignment.items():
        if value is None:
            rtn = rtn and False
        else:
            rtn = rtn and True
    return rtn


def initialize_assignment(assignment, csp):
    for var in csp.get_all_variables():
        assignment[var] = None


def check_value_consistency(var, value, assignment, csp):

    uex = csp.get_uex(var)
    uin = csp.get_uin(var)

    if uex:  # if the uex exists for this variable
        if value in uex:
            return False
    if uin:  # if the uex exists for this variable
        if value not in uin:
            return False

    connecting_var = csp.get_connecting_vars(var)

    # TODO the following part checks the binary constraints,
    # TODO it is very similar to what happended in revise function use in ac3
    rtn = True  # only using in this part
    if connecting_var is not None:  # if the variable has connections
        i = csp.get_index_of_value(value)  # get the index of the value being checked

        for c in connecting_var:
            const_matrix = csp.get_biconst(var, c)  # note that by doing this, var is the y axis, c is the x axis
            for j in range(csp.get_values_len()):
                if csp.get_value_by_index(j) in c.domain:
                    rtn = rtn or const_matrix[i, j]

    return rtn

