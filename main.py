import os

from Constraints import Constraints

current_section = 0
t = {}  # dictionary of tasks (variables)
p = []  # list of processors (values)
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
                p.append(arg[0])
            # elif
            elif current_section == 3:  # deadline
                deadline = int(arg[0])
            elif current_section == 4:  # unary Inclusive
                const_p = arg[1:len(arg)]
                c.add_uin(arg[0], const_p)
            elif current_section == 5:  # unary Exclusive
                const_p = arg[1:len(arg)]
                c.add_uex(arg[0], const_p)

            # elif current_section == 6:
            #     c.add_bieq(arg)
            elif current_section == 7:
                c.add_bine(arg)
            # elif current_section == 8:
            #     const_t = ()  # USING A TUPLE FOR TASK SO THAT IT IS HASHABLE
            #     const_p = []
            #     for i in arg:
            #         if i.isupper():  # it is a task if it's an upper case letter
            #             const_t = const_t + (i,)
            #         else:
            #             const_p.append(i)
            #     c.add_bins(const_t, const_p)



# def csp_solver(variables, values, constraint):



print(t)
print(p)
print(deadline)
print(c)

