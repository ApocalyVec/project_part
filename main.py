import os
import copy

from Constraints import Constraints
from Variable import Variable
from Solver import ac_3

current_section = 0
# TODO deadling is a particular to this CSP
# t = []  # list of tasks (variables)
p = []  # list of processors (values)
i = 0  # index used to tag values (processors): for matrix search
c = Constraints()  # constraint class
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
                c.add_var_to_graph(new_task)
            elif current_section == 2:  # reading processors
                c.add_value_to_all_variable_domain(arg[0])
                p.append(arg[0])
            elif current_section == 3:  # deadline
                deadline = int(arg[0])
            elif current_section == 4:  # unary Inclusive
                const_p = arg[1:len(arg)]
                c.add_uin(arg[0], const_p)
            elif current_section == 5:  # unary Exclusive
                const_p = arg[1:len(arg)]
                c.add_uex(arg[0], const_p)

            elif current_section == 6:
                c.add_biconst(arg, p, 1)
            elif current_section == 7:  # binary not equal
                c.add_biconst(arg, p, 0)

            elif current_section == 8:
                const_var = []
                const_value = []

                for i in arg:  # separate the arguments into tasks and processors (values and variables)
                    if i.isupper():  # it is a task if it's an upper case letter
                        const_var.append(i)
                    else:
                        const_value.append(i)

                c.add_bins(const_var, const_value, p)


# c.const_graph.print_all_vertices()
print(p)
print(deadline)
print(c)
c.const_graph.print_all_vertices()

if not ac_3(c, p):
    print("unsolvable, killed")
print("Variables and their domain after applying Arc Consistency: ")
c.print_all_variable()