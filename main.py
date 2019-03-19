import os
import copy

from runtimecsp import RuntimeCsp
from Variable import Variable
from Solver import ac_3
from Solver import backtrack
from Solver import initialize_assignment

current_section = 0
# TODO deadling is a particular to this CSP
# t = []  # list of tasks (variables)
p = []  # list of processors (values)
i = 0  # index used to tag values (processors): for matrix search
csp = RuntimeCsp()  # constraint class
deadline = 0  # default value of deadline


filePath = str(input("Please enter a file path. Then press enter... "
                     "(Please note the Program will NOT validate the input file)"))
print('reading ' + filePath)
assert os.path.exists(filePath), "File not found at " + filePath + ", Exiting..."

with open(filePath) as input_file:
    for line in input_file:
        if line[0:5] == "#####":  # this line is comment
            current_section += 1
        else:
            arg = line.rstrip().split(" ")
            if current_section == 1:  # reading tasks
                new_task = Variable(arg[0], int(arg[1]))
                csp.add_var_to_graph(new_task)
            elif current_section == 2:  # reading processors
                # csp.add_value_to_all_variable_domain()
                p.append(arg[0])
                csp.add_value(arg[0])
            elif current_section == 3:  # deadline
                csp.make_runtime()
                deadline = int(arg[0])
                csp.set_deadline(deadline)
            elif current_section == 4:  # unary Inclusive
                const_p = arg[1:len(arg)]
                csp.add_uin(arg[0], const_p)
            elif current_section == 5:  # unary Exclusive
                const_p = arg[1:len(arg)]
                csp.add_uex(arg[0], const_p)

            elif current_section == 6:
                csp.add_biconst(arg, 1)
            elif current_section == 7:  # binary not equal
                csp.add_biconst(arg, 0)

            elif current_section == 8:
                const_var = []
                const_value = []

                for i in arg:  # separate the arguments into tasks and processors (values and variables)
                    if i.isupper():  # it is a task if it's an upper case letter
                        const_var.append(i)
                    else:
                        const_value.append(i)

                csp.add_bins(const_var, const_value)


# c.const_graph.print_all_vertices()
print(deadline)
print(csp)
csp.const_graph.print_all_vertices()

if not ac_3(csp):
    print("CSP is AC3 INCONSISTENT, killed")
print("Variables and their domain after applying Arc Consistency: ")
csp.print_all_variable()

assignment = {}  # represent the assignment of variabels [Key: Variable, Value: value (str)]

initialize_assignment(assignment, csp)

if backtrack(assignment, csp) is not None:
    print("CSP Answer is: ")
    for var, value in assignment.items():
        print(var.name + ": " + value)
    csp.print_process_time(assignment)
else:
    print("CSP is UNSOLVABLE, killed")



