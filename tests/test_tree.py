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
            return False

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

    
def test_MidFunc():
    small = open('mid_func.txt', 'r')
    code = small.read()
    scanner = Scanner(code)
    parser = Parser()
    ast = parser.Parse(scanner).GetRoot()

    mid_tree = Node(value='main')

    a_p = Node('a')
    a_p.AddChild(Node('type: celina'))

    b_p = Node('b')
    b_p.AddChild(Node('type: bukvi'))

    params = Node('params')
    params.AddChild(a_p)
    params.AddChild(b_p)
    

    ret = Node('return type: bukvi')

    body = Node('body')

    comp = Node('>')
    comp.AddChild(Node('a'))
    comp.AddChild(Node('10'))

    cond = Node('condition')
    cond.AddChild(comp)

    koli = Node('KOLI')

    eq = Node('=')
    eq.AddChild(Node('b'))
    eq.AddChild(Node('"123"'))

    stat_koli = Node('statements')
    stat_koli.AddChild(eq)

    koli.AddChild(cond)
    koli.AddChild(stat_koli)

    plus = Node('+')
    plus.AddChild(Node('b'))
    plus.AddChild(Node('"321"'))
    vozd = Node('VOZDAT')
    vozd.AddChild(plus)

    body.AddChild(koli)
    body.AddChild(vozd)

    mid_tree.AddChild(params)
    mid_tree.AddChild(ret)
    mid_tree.AddChild(body)

    prog = Node('VeKrestKrestProg')
    prog.AddChild(mid_tree)

    mid_tree.Print()

    assert TreesEqual(ast, prog)