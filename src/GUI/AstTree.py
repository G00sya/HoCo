class Node:
    def __init__(self, value='', t='DEFAULT', start_pos=0, end_pos=0):
        self.value = value
        self.type = t
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.childs = []

    def AddChild(self, child):
        self.childs.append(child)

    def Print(self, depth=0):
        indent = ' ' * depth
        if self.value:
            print(indent + '->', self.value)
        for child in self.childs:
            child.Print(depth + 1)

    def Pack(self, array):
        if self.value:
            array.append(self)
        for child in self.childs:
            child.Pack(array)
    def PrevCount(self):
        return len(self.childs)

    def Rename(self, name: str):
        if (len(name)): self.value = name

    def SetCoords(self, start_pos=0, end_pos=0):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def GetCoords(self):
        return self.start_pos, self.end_pos


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


def ConnectSame(tree, trees, operation, pos):
    if (len(trees) > 1):
        tree = Node(value=operation, t='DEFAULT', start_pos=pos, end_pos=(pos + len(operation)))
        for tr in trees:
            tree.AddChild(tr)
    return tree


def ConnectWithOps(tree, trees, ops, postions):
    if len(trees) > 1:
        tree = Node(ops[0], 'DEFAULT', start_pos=postions[0][0], end_pos=postions[0][1])
        tree.AddChild(trees[0])
        last = tree
        for i in range(1, len(trees) - 1):
            right_pos, _ = last.GetCoords()
            cur = Node(ops[i], 'DEFAULT', *postions[i])
            cur.AddChild(trees[i])
            last.AddChild(cur)
            last = cur
        last.AddChild(trees[-1])
    return tree
