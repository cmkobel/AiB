from itertools import chain

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children =  [i for i in children]

    def __iter__(self):
        yield self
        for node in chain(*map(iter, self.children)):
            yield node



    def __str__(self):
        return self.value



T = Node('root')

T.children.append(Node('child1', Node('grand-child (child of child1)')))
T.children.append(Node('child2'))   

for node in T:
    print(node)

print(T)