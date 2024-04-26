class Node:
    def __init__(self, value='', t=''):
        self.value = value
        self.type = t
        self.childs = []
    
    def AddChild(self, child):
        self.childs.append(child)

    def PrintChildrens(self, i=0 ):
        if len(self.childs) and len(self.value): print(' ' * i, self.value)
        elif len(self.value): print(' ' * i, "->", self.value)
        for c in self.childs:
            c.PrintChildrens(i + 1)
        if len(self.childs) > 1 and len(self.value) > 1: print()
        
    def PrevCount(self):
        return len(self.childs)

    def Rename(self, name: str):
        if (len(name)): self.value = name


