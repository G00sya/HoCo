class Node:
    def __init__(self, value='', t=''):
        self.value = value
        self.type = t
        self.childs = []
    
    def AddChild(self, child):
        self.childs.append(child)

    def Print(self, depth=0):
        indent = ' ' * depth
        if self.value:
            print(indent + '->', self.value)
        for child in self.childs:
            child.Print(depth + 1)
        
    def PrevCount(self):
        return len(self.childs)

    def Rename(self, name: str):
        if (len(name)): self.value = name

class ASTree:
    def __init__(self):
        self.root = None

    def AddNode(self, value='', t=''):
        new_node = Node(value, t)
        if not self.root:
            self.root = new_node
        else:
            self.root.AddChild(new_node)

    def AddNode(self, new_node):
        if not self.root:
            self.root = new_node
        else:
            self.root.AddChild(new_node)

    def PrintTree(self):
        if self.root:
            self.root.Print()

    def GetRoot(self):
        return self.root

