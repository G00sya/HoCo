class Node:
    def __init__(self, name='', value='', t=''):
        self.name = name
        self.value = value
        self.type = t
        self.prev = []
    
    def AddChild(self, child):
        self.prev.append(child)

    def PrintChildrens(self, i=0 ):
        if len(self.prev) and len(self.name): print(' ' * i, self.name)
        elif len(self.name): print(' ' * i, "->", self.name)
        for c in self.prev:
            c.PrintChildrens(i + 1)
        if len(self.prev) > 1 and len(self.name) > 1: print()
        
    def PrevCount(self):
        return len(self.prev)

    def Rename(self, name: str):
        if (len(name)): self.name = name

class Tree:
    def __init__():
        self.head = Node()


