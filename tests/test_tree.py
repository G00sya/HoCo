import sys
sys.path.insert(1, '../../HoCo')
sys.path.insert(2, '../parser_src')

from parser_src.AstTree import Node
from parser_src.Parser import Parser
from parser_src.Scanner import Scanner

def TreesEqual(lhs : Node, rhs: Node):
    if lhs.value != rhs.value:
        return False
    
    if len(lhs.childs) != len(rhs.childs):
        return False

    for i in range(len(lhs.childs)):
        lhs_child = lhs.childs[i]
        rhs_child = rhs.childs[i]
        if not TreesEqual(lhs_child, rhs_child):
            return false

    return True

def test_SmallTree():
    small = open('small.txt', 'r')
    code = small.read()
    scanner = Scanner(code)
    parser = Parser()
    ast = parser.Parse(scanner).GetRoot()

    small_tree = Node(value='main')
    params = Node('params')
    ret = Node('return type: celina')
    body = Node('body')
    vozd = Node('VOZDAT')
    num = Node('1')

    vozd.AddChild(num)
    body.AddChild(vozd)
    small_tree.AddChild(params)
    small_tree.AddChild(ret)
    small_tree.AddChild(body)

    prog = Node('VeKrestKrestProg')
    prog.AddChild(small_tree)

    assert TreesEqual(ast, prog)