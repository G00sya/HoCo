class Node:
    def __init__(self, value=""):
        self.value = value
        self.prev = []
    
    def AddChild(self, child):
        self.prev.append(child)

    def PrintChildrens(self):
        for c in self.prev:
            if not c.PredCount():
                print(c.value)
            else:
                c.PrintChildrens()
        
    def PredCount(self):
        return len(self.prev)
    
def f():
    print(1)
