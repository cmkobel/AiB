from itertools import chain

class Node: # A tree node
    def __init__(self, weight = 0, name = "no_name", children = [], parent = None):
        self.weight = weight
        self.name = name
        #self.value = value # tuple: (weight, name)
        self.children = [i for i in children]
        self.parent = parent

    def __str__(self):
        return str((self.weight, self.name))
    
    def __repr__(self):
        return str(self)

    def long_repr(self):
        return f'Node with weight: {self.weight}, name: {self.name}{", parent: " + self.parent.name if self.parent != None else ""}{", children: " + str(self.children) if len(self.children) > 0 else ""}\n'




    def display(self, tabs = 0):
        """ return value based instead """

        # Add your own name.
        rv = '\t' * tabs + \
             str(self.weight) + ' ' +  self.name + \
             f' {"(" + self.parent.name + ")" if self.parent != None else ""}' + \
             '\n'

        # Add the name of your children.
        for i in self.children:
            rv += '\t' * tabs + i.display(tabs + 1)

        return rv







    def __iter__(self):
        """ Implement the iterator protocol. """
        for node in chain(*map(iter, self.children)):
            yield node
        yield self