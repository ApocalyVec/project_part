from os import system

import numpy


class Constraints:
    def __init__(self):
        self.uin = {}
        self.uex = {}

        self.biconst = {}


    def __str__(self):
        return "Unary Inclusive: " + str(self.uin) + "\n" + \
               "Unary Exclusive: " + str(self.uex) + "\n" + \
               "Binary Constraint: " + str(self.biconst)

    def add_uin(self, const_var, const_value):
        self.uin[const_var] = const_value

    def add_uex(self, const_var, const_value):
        self.uex[const_var] = const_value

        '''
    Create a binary constraint matrix

    :param list const_vars: the values to be constrained
    :param dic values: list of values [key: index, value: variable value]
    :param int equal: constraint type: 1 = binary equals, 0 = binary not equals
        '''
    # TODO handle duplicate binary varible EXCEPTION
    # TODO should say NO ANSWER if a constraint matrix are all zeros
    def add_biconst(self, const_vars, values, equal):  # constraint type


        # TODO what if two bi_const have the same constrainting variable
        # The first value in the tuple takes the rows, and the second takes the columns
        if tuple(const_vars) in self.biconst.keys():
            print("duplicate binary constraint, killed")
            system.exit()
        else:
            if equal:
                const_matrix = self.biconst[tuple(const_vars)] = numpy.zeros(
                    shape=(len(values), len(values)), dtype=int)
            else:
                const_matrix = self.biconst[tuple(const_vars)] = numpy.ones(
                    shape=(len(values), len(values)), dtype=int)

            for i in range(len(values)):  # create constraint matrix
                for j in range(len(values)):
                    if values[i] == values[j]: # if they are the same value, they should be constrained

                        const_matrix[i, j] = equal  # 0 for not equal, 1 for equal

                    # TODO efficiency??? running this for loop everytime
                    for const_var in const_vars:
                        if const_var in self.uex.keys():  # the rows(indexed by i) corresponds to the zeroth const variable; the columns(indexed by j) corresponds to the first const variable
                            if const_vars.index(const_var) == 0 and values[i] in self.uex[const_var]:
                                const_matrix[i, j] = 0
                            if const_vars.index(const_var) == 1 and values[j] in self.uex[const_var]:
                                const_matrix[i, j] = 0

                        if const_var in self.uin.keys():
                            if const_vars.index(const_var) == 0 and values[i] not in self.uin[const_var]:
                                const_matrix[i, j] = 0
                            if const_vars.index(const_var) == 1 and values[j] not in self.uin[const_var]:
                                const_matrix[i, j] = 0

    # def add_bins(self, const_t, const_p):
    #     self.bins[const_t] = const_p
