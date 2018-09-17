# Jeg ved ikke helt om jeg skal lave dette til en slags main controller ting, eller om det er bedre bare at have en enkelt fil som holder styr på det hele.

class Parent():
    """docstring for Parent"""
    def __init__(self, arg):
        self.arg = arg
        print(f'parent says: {self.arg}')


p = Parent('this is some input for parent')


class Child(Parent):
    """child of the parent"""
    def __init__(self, child_arg):
    
        super(Child, self).__init__(child_arg)


c = Child('this is some input for child')