class Node:
    def __init__(self, value=""):
        self.value = value
        self.prev = []
    
    def AddChild(self, child):
        self.prev.append(child)

    def PrintChildrens(self, i):
        if len(self.prev) and len(self.value): print(' ' * i, self.value)
        elif len(self.value): print(' ' * i, "->", self.value)
        for c in self.prev:
            c.PrintChildrens(i + 1)
        if len(self.prev) > 1 and len(self.value) > 1: print()
        
    def PrevCount(self):
        return len(self.prev)

    def Rename(self, new_val: str):
        if (len(new_val)): self.value = new_val

