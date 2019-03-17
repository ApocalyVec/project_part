from os import system


class Constraints:
    def __init__(self):
        self.uin = {}
        self.uex = {}

        self.bicont = {}


    def __str__(self):
        return "Unary Inclusive: " + str(self.uin) + "\n" + \
               "Unary Exclusive: " + str(self.uex) + "\n" + \
               "Binary Equal: " + str(self.bieq) + "\n" + \
               "Binary Not Equal: " + str(self.bine) + "\n" + \
               "Binary Not Simultaneous: " + str(self.bins)

    def add_uin(self, task, const_p):
        self.uin[task] = const_p

    def add_uex(self, task, const_p):
        self.uex[task] = const_p



    # def add_bieq(self, tasks):
    #     self.bieq.append(tasks)

    # const_t must be a list

    def add_bine(self, const_t):
        # TODO what if two bi_const have the same constrainting variable
        if tuple(const_t) in self.bicont.keys():
            print("duplicate binary constraint, abort")
            system.exit()
        else:
            self.bicont[tuple(const_t)] = []


        # self.bine.append(const_t)


    # def add_bins(self, const_t, const_p):
    #     self.bins[const_t] = const_p

