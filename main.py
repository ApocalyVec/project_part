import os

from Constraints import Constraints

current_section = 0
# TODO deadling is a particular to this CSP
t = {}  # dictionary of tasks (variables) [key: variable name, value: deadline]
p = {}  # list of processors (values) [key: index, value: variable value]
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
                t[arg[0]] = int(arg[1])
            elif current_section == 2:  # reading processors
                p[i] = arg[0]
                i += 1
            # elif
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


# def csp_solver(variables, values, constraint):



print(t)
print(p)
print(deadline)
print(c)

