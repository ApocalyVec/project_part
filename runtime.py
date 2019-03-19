class Runtime:
    def __init__(self, processors):
        self.p_dic = {}
        for p in processors:
            self.p_dic[p] = 0

    def generate_run_time(self, processors, assignment, tasks):
        """
        :return int: the total run time of tasks (variable) on the given processor (value)
        :param processors:
        :param csp:
        """
        process_time = 0
        for var in tasks:
            if assignment[var] is not None:
                if assignment[var] == processors:
                    process_time = process_time + var.tag
        return process_time

    def get_max_run_time(self, assignment, tasks):
        runtime_list = []
        for p in self.p_dic.keys():  # p: processors, t: time
            runtime_list.append(self.generate_run_time(p, assignment, tasks))

        runtime_list.sort(reverse=True)
        return runtime_list[0]