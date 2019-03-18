'''
    apply Arc Consistency to the given list of variables
    :param list variables: list variables to be checked
    :param Constraint constraint: constraint object against which to check arc consistency
    :return None, it modifies the domain of the given variable to be arc consistent
'''
import queue


# TODO arcs should not have duplicate arcs
def ac_3(constraint, values):
    arcs = queue.Queue()

    # put arcs in the queue
    for a in constraint.get_all_arcs():
        arcs.put(a)

    while not arcs.empty():
        arc = arcs.get()
        if revise(arc[0], arc[1], constraint, values):  # revising the domain of arc[0]
            if not arc[0].domain:
                # pass
                return False
            for propagating_arc in constraint.get_arc(arc[0]):
                arcs.put(propagating_arc)

    return True
'''
    revise the domain of x
    :param Variable x, y 
    :return bool eantrue iff we revised the domain of x
'''
def revise(x, y, constraint, values):
    pruning_value = []
    biconst = constraint.get_biconst(x, y)

    for value in x.domain:

        # check the unary constraint first
        uex = constraint.get_uex(x)
        uin = constraint.get_uin(x)

        if uex:
            if value in constraint.get_uex(x):
                pruning_value.append(value)
        if uin:
            if value not in constraint.get_uin(x):
                pruning_value.append(value)

        # now check the binary constraints
        if biconst is not None:
            prune = False
            i = values.index(value)

            for j in range(len(values)):
                if values[j] in y.domain:  # if the value is still in y's domain
                    prune = prune or biconst[i, j]

            if not prune:
                pruning_value.append(value)

    for pv in pruning_value:
        x.prune_value(pv)

    return not not pruning_value
