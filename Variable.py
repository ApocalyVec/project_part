
class Variable:

    def __init__(self):
        self.name = None
        self.value = None
        self.domain = []
        self.tag = None
        '''
        Create a Variable
    
        :param string name: name of the variable
        :param int equal: constraint type: 1 = binary equals, 0 = binary not equals
         
        var value: value to which this variable will be assigned
        '''
    def __init__(self, name):
        self.name = name
        self.value = None
        self.domain = []
        self.tag = None

        '''
        Create a Variable
    
        :param string name: name of the variable
        :param var tag: additional information of the variable (i.e. deadline for tasks)
        
        var value: value to which this variable will be assigned
        '''
    def __init__(self, name, tag):
        self.name = name
        self.value = None
        self.domain = []
        self.tag = tag

    #     '''
    #     Create a Variable
    #
    #     :param string name: name of the variable
    #     :param list domain: list of values that the variable can take
    #
    #     var value: value to which this variable will be assigned
    #     '''
    # def __init__(self, name, domain):
    #     self.name = name
    #     self.value = None
    #     self.tag = None
    #     self.domain = domain
    #
    #     '''
    #     Create a Variable
    #
    #     :param string name: name of the variable
    #     :param var tag: additional information of the variable (i.e. deadline for tasks)
    #     :param list domain: list of values that the variable can take
    #
    #     var value: value to which this variable will be assigned
    #     '''
    # def __init__(self, name, tag, domain):
    #     self.name = name
    #     self.value = None
    #     self.tag = tag
    #     self.domain = domain

    def __str__(self):
        return str(self.name) + ": " + str(self.value) + ", tag: " + str(self.tag) + str(self.domain)

    def set_value(self, value):
        self.value = value

        '''
        set the domain the variable
        :param dictionary domain: values [key: index, value: variable value]
        '''
    def set_domain(self, domain):
        self.domain = domain

        '''
        remove a value from the variable's domain
        :param string value: the value to be removed
        '''
    def prune_value(self, value):
        if value in self.domain:
            self.domain.remove(value)
        '''
        check a variable's assignment against constraints
        :param Constraint const: the constraint against which to check the value assignment
        :return boolean: true if the assignment is good, and false otherwise
        '''
    # def check_const(self, const):
