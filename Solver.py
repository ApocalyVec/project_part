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
            for propagating_arc in csp.get_arc(arc[0]):
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
def backtrack(csp):
    if csp.is_assignment_complete():
        return
    # for value in
