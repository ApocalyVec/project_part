import math
import queue
from os import system


def inference(var, value, csp):
    """
    inference using ac_3
    :param Variable var:
    :param String value:
    :param Csp csp:
    :return: Boolean; False if a var's domain results in empty
    """
    arcs = queue.Queue()
    for c in csp.get_arcs(var):
        arcs.put(c)

    while not arcs.empty():
        arc = arcs.get()
        # if inference_revise()

    return True

def inference_revise(value, x, y, csp):
    """
    return the list of value that needs to be pruned from x's domain given that the value assigned to x is @param value
    :param value:
    :param x:
    :param y:
    :param csp:

    :usage: this function is called by revise which is called by ac_3
    """
    pruning_value = []
    biconst = csp.get_biconst(x, y)

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
    #TODO prune_value needs not to be a list
    for pv in pruning_value:
        x.prune_value(pv)

    return not not pruning_value


# TODO arcs should not have duplicate arcs
def ac_3(csp):
    """
    apply Arc Consistency to the given list of variables
    :param Csp csp: constraint object against which to check arc consistency
    :return None, it modifies the domain of the given variable to be arc consistent
    """
    arcs = queue.Queue()

    # put arcs in the queue
    for a in csp.get_all_arcs():
        arcs.put(a)

    while not arcs.empty():
        arc = arcs.get()
        if revise(arc[0], arc[1], csp):  # revising the domain of arc[0]
            if not arc[0].domain:
                return False
            for propagating_arc in csp.get_arcs(arc[0]):
                arcs.put(propagating_arc)

    return True

# def revise(x, y, csp):
#     """
#         revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
#         :param x Variable
#         :param y Variable
#         :return bool true iff we revised the domain of x
#     """
#     pruning_value = []
#     biconst = csp.get_biconst(x, y)
#
#     for value in x.domain:
#
#         # check the unary constraint first,
#         # The binary constraint covers the unary constraint
#         uex = csp.get_uex(x)
#         uin = csp.get_uin(x)
#
#         if uex:
#             if value in csp.get_uex(x):
#                 pruning_value.append(value)
#         if uin:
#             if value not in csp.get_uin(x):
#                 pruning_value.append(value)
#
#         # now check the binary constraints
#         if biconst is not None:
#             prune = False
#             i = csp.get_index_of_value(value)
#
#             for j in range(csp.get_values_len()):
#                 if csp.get_value_by_index(j) in y.domain:  # if the value is still in y's domain
#                     prune = prune or biconst[i, j]
#
#             if not prune:
#                 pruning_value.append(value)
#
#     for pv in pruning_value:
#         x.prune_value(pv)
#
#     return not not pruning_value  # return true if revised

def revise(x, y, csp):
    """
        revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
        :param x Variable
        :param y Variable
        :return bool true iff we revised the domain of x
    """
    rtn = False
    for value in x.domain:
        revised = inference_revise(value, x, y, csp)
        rtn = rtn or revised

    return not not rtn  # return true if revised


def backtrack(assignment, csp):
    """
    NOTE that the Constraint object keeps all the variables. Thus it also keeps all the assignment to variables
    :param assignment:
    :param csp:
    :return:
    """
    if is_assignment_complete(assignment): return assignment
    var = select_unassigned_var(assignment, csp)
    for value in ordered_domain(var, assignment, csp):
        if check_value_consistency(var, value, assignment, csp):
            assignment[var] = value

            if inference(var, value, csp):  # if inference left any variable's domain to be empty
                result = backtrack(assignment, csp)  # recursion call
                if result is not None:
                    return result

            assignment[var] = None  # remove this assignment

    return None


def ordered_domain(var, assignment, csp):
    """
    order the domain of a variable by the rule of least constraining value
    :param var:
    :param assignment:
    :param csp:
    :return:
    """
    return var.domain


def naive_select_unassigned_var(assignment, csp):
    '''
    naive select_unassigned_var
    :param Constraint csp
    '''
    for var in csp.get_all_variables():
        if assignment[var] is None:
            return var


def select_unassigned_var(assignment, csp):
    '''
    clever select_unassigned_var
    implementing minimum remaining-values (MRV) / most constrained variable / fail-first
    :param csp Constraint
    :param assignment Dictionary
    '''
    # make a list to order all the variables
    var_list = []
    min_domain_len = math.inf
    for var in csp.get_all_variables():
        if assignment[var] is None:
            var_list.append(var)
            if len(var.domain) < min_domain_len:  # update the min domain length
                min_domain_len = len(var.domain)

    min_var_list = []  # the list that keeps the most constrained variables
    for var in var_list:
        if len(var.domain) == min_domain_len:
            min_var_list.append(var)

    if len(min_var_list) == 1:  # just return the variable if there's one most constrained variable
        return min_var_list[0]
    elif len(min_var_list) > 1:  # break tie using Degree Heuristic
        min_var_list.sort(key=lambda x: (len(csp.get_connecting_vars(x))), reverse=True)
        return min_var_list[0]
    else:
        print("Solver: select_unassigned_var: bad var list")
        system.exit()


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
