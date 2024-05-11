# -------------------------------------------------------------------------
# Parser.py -- ATG file parser
# Compiler Generator Coco/R,
# Copyright (c) 1990, 2004 Hanspeter Moessenboeck, University of Linz
# extended by M. Loeberbauer & A. Woess, Univ. of Linz
# ported from Java to Python by Ronald Longo
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# As an exception, it is allowed to write an extension of Coco/R that is
# used as a plugin in non-free software.
#
# If not otherwise stated, any source code generated by Coco/R (other than
# Coco/R itself) does not fall under the GNU General Public License.
# -------------------------------------------------------------------------*/

from AstTree import Node, ASTree, ConnectSame, ConnectWithOps

import sys

from Scanner import Token
from Scanner import Scanner
from Scanner import Position


class ErrorRec(object):
    def __init__(self, l, c, s):
        self.line = l
        self.col = c
        self.num = 0
        self.str = s


class Errors(object):
    errMsgFormat = "file %(file)s : (%(line)d, %(col)d) %(text)s\n"
    eof = False
    count = 0  # number of errors detected
    fileName = ''
    listName = ''
    mergeErrors = False
    mergedList = None  # PrintWriter
    errors = []
    minErrDist = 2
    errDist = minErrDist

    # A function with prototype: f( errorNum=None ) where errorNum is a
    # predefined error number.  f returns a tuple, ( line, column, message )
    # such that line and column refer to the location in the
    # source file most recently parsed.  message is the error
    # message corresponging to errorNum.

    @staticmethod
    def Init(fn, dir, merge, getParsingPos, errorMessages):
        Errors.theErrors = []
        Errors.getParsingPos = getParsingPos
        Errors.errorMessages = errorMessages
        Errors.fileName = fn
        listName = dir + 'listing.txt'
        Errors.mergeErrors = merge
        if Errors.mergeErrors:
            try:
                Errors.mergedList = open(listName, 'w', encoding='utf-8')
            except IOError:
                raise RuntimeError('-- Compiler Error: could not open ' + listName)

    @staticmethod
    def storeError(line, col, s):
        if Errors.mergeErrors:
            Errors.errors.append(ErrorRec(line, col, s))
        else:
            Errors.printMsg(Errors.fileName, line, col, s)

    @staticmethod
    def SynErr(errNum, errPos=None):
        line, col = errPos if errPos else Errors.getParsingPos()
        msg = Errors.errorMessages[errNum]
        Errors.storeError(line, col, msg)
        Errors.count += 1

    @staticmethod
    def SemErr(errMsg, errPos=None):
        line, col = errPos if errPos else Errors.getParsingPos()
        Errors.storeError(line, col, errMsg)
        Errors.count += 1

    @staticmethod
    def Warn(errMsg, errPos=None):
        line, col = errPos if errPos else Errors.getParsingPos()
        Errors.storeError(line, col, errMsg)

    @staticmethod
    def Exception(errMsg):
        print(errMsg)
        sys.exit(1)

    @staticmethod
    def printMsg(fileName, line, column, msg):
        vals = {'file': fileName, 'line': line, 'col': column, 'text': msg}
        sys.stdout.write(Errors.errMsgFormat % vals)

    @staticmethod
    def display(s, e):
        Errors.mergedList.write('**** ')
        for c in range(1, e.col):
            if s[c - 1] == '\t':
                Errors.mergedList.write('\t')
            else:
                Errors.mergedList.write(' ')
        Errors.mergedList.write('^ ' + e.str + '\n')

    @staticmethod
    def Summarize(sourceBuffer):
        if Errors.mergeErrors:
            # Initialize the line iterator
            srcLineIter = iter(sourceBuffer)
            srcLineStr = srcLineIter.next()
            srcLineNum = 1

            try:
                # Initialize the error iterator
                errIter = iter(Errors.errors)
                errRec = errIter.next()

                # Advance to the source line of the next error
                while srcLineNum < errRec.line:
                    Errors.mergedList.write('%4d %s\n' % (srcLineNum, srcLineStr))

                    srcLineStr = srcLineIter.next()
                    srcLineNum += 1

                # Write out all errors for the current source line
                while errRec.line == srcLineNum:
                    Errors.display(srcLineStr, errRec)

                    errRec = errIter.next()
            except:
                pass

            # No more errors to report
            try:
                # Advance to end of source file
                while True:
                    Errors.mergedList.write('%4d %s\n' % (srcLineNum, srcLineStr))

                    srcLineStr = srcLineIter.next()
                    srcLineNum += 1
            except:
                pass

            Errors.mergedList.write('\n')
            Errors.mergedList.write('%d errors detected\n' % Errors.count)
            Errors.mergedList.close()

        sys.stdout.write('%d errors detected\n' % Errors.count)
        if (Errors.count > 0) and Errors.mergeErrors:
            sys.stdout.write('see ' + Errors.listName + '\n')


class Parser(object):
    _EOF = 0
    _identifier = 1
    _number = 2
    _string = 3
    maxT = 39

    T = True
    x = False
    minErrDist = 2

    def __init__(self):
        self.scanner = None
        self.token = None  # last recognized token
        self.la = None  # lookahead token
        self.genScanner = False
        self.tokenString = ''  # used in declarations of literal tokens
        self.noString = '-none-'  # used in declarations of literal tokens
        self.errDist = Parser.minErrDist

    def getParsingPos(self):
        return self.la.line, self.la.col

    def SynErr(self, errNum):
        if self.errDist >= Parser.minErrDist:
            Errors.SynErr(errNum)

        self.errDist = 0

    def SemErr(self, msg):
        if self.errDist >= Parser.minErrDist:
            Errors.SemErr(msg)

        self.errDist = 0

    def Warning(self, msg):
        if self.errDist >= Parser.minErrDist:
            Errors.Warn(msg)

        self.errDist = 0

    def Successful(self):
        return Errors.count == 0;

    def LexString(self):
        return self.token.val

    def LookAheadString(self):
        return self.la.val

    def Get(self):
        while True:
            self.token = self.la
            self.la = self.scanner.Scan()
            if self.la.kind <= Parser.maxT:
                self.errDist += 1
                break

            self.la = self.token

    def Expect(self, n):
        if self.la.kind == n:
            self.Get()
        else:
            self.SynErr(n)

    def StartOf(self, s):
        return self.set[s][self.la.kind]

    def ExpectWeak(self, n, follow):
        if self.la.kind == n:
            self.Get()
        else:
            self.SynErr(n)
            while not self.StartOf(follow):
                self.Get()

    def WeakSeparator(self, n, syFol, repFol):
        s = [False for i in range(Parser.maxT + 1)]
        if self.la.kind == n:
            self.Get()
            return True
        elif self.StartOf(repFol):
            return False
        else:
            for i in range(Parser.maxT):
                s[i] = self.set[syFol][i] or self.set[repFol][i] or self.set[0][i]
            self.SynErr(n)
            while not s[self.la.kind]:
                self.Get()
            return self.StartOf(syFol)

    def VeKrestKrest(self):
        main_tree = Node(value='VeKrestKrestProg', t='body')
        while self.la.kind == 1:
            def_tree = self.Defenition()
            main_tree.AddChild(def_tree)

        tree = ASTree()
        tree.AddNode(main_tree)

        return tree

    def Defenition(self):
        start_pos = self.token.pos
        self.Expect(1)
        name = self.token.val
        params = self.Params()
        self.Expect(4)
        type = self.Type()
        end_pos = self.token.pos + len(type)
        tree = self.FunctionDefinition()
        defTree = Node(value=f'{name}({params})->{type}', t='decl', start_pos=start_pos, end_pos=end_pos)
        tree.Rename('body')
        defTree.AddChild(tree)

        return defTree

    def Params(self):
        params = ''
        self.Expect(5)
        if (self.StartOf(1)):
            fparams = self.FormalParamList()
            params += fparams
        self.Expect(6)
        return params

    def Type(self):
        if self.la.kind == 8:
            type = ''
            self.Get()
            type = self.token.val
            if (self.la.kind == 9):
                self.Get()
                self.ConstExpression()
                self.Expect(10)
        elif self.la.kind == 11:
            self.Get()
            type = self.token.val
        elif self.la.kind == 12:
            self.Get()
            type = self.token.val
            if (self.la.kind == 9):
                self.Get()
                self.ConstExpression()
                self.Expect(10)
        elif self.la.kind == 13:
            self.Get()
            type = self.token.val
            if (self.la.kind == 9):
                self.Get()
                self.ConstExpression()
                self.Expect(10)
        else:
            self.SynErr(40)
        return type

    def FunctionDefinition(self):
        tree = self.CompoundStatement()
        return tree

    def FormalParamList(self):
        fparams = ''
        fp = self.FormalParameter()
        fparams += fp
        while self.la.kind == 7:
            self.Get()
            fp = self.FormalParameter()
            fparams += ', ' + fp

        return fparams

    def FormalParameter(self):
        fp = ''
        type = self.Type()
        fp = self.token.val
        self.Expect(1)
        fp += ' ' + self.token.val
        return fp

    def CompoundStatement(self):
        tree = Node(t='body')
        self.Expect(14)
        start_pos = self.token.pos
        while self.StartOf(2):
            t = self.DeclrationOrStatement()
            tree.AddChild(t)

        self.Expect(15)
        end_pos = self.token.pos;
        tree.SetCoords(start_pos, end_pos)
        return tree

    def ConstExpression(self):
        tree = self.Expression()

    def Statement(self):
        tree = Node(t='stat')
        if self.StartOf(3):
            assigm_tree = self.AssignmentExpression()
            tree = assigm_tree
        elif self.la.kind == 14:
            cmpd_tree = self.CompoundStatement()
            tree = cmpd_tree
        elif self.la.kind == 20:
            if_tree = self.IfStatement()
            tree = if_tree
        elif self.la.kind == 18:
            ret_tree = self.ReturnStatement()
            tree.Rename("VOZDAT");
            tree.AddChild(ret_tree)
        elif self.la.kind == 19:
            while_tree = self.WhileStatement()
            tree = while_tree
        else:
            self.SynErr(41)
        return tree

    def AssignmentExpression(self):
        t = self.Expression()
        self.Expect(17)
        return t

    def IfStatement(self):
        tree = Node(value='KOLI', t='key')
        self.Expect(20)
        self.Expect(5)
        expr_tree = self.Expression()
        self.Expect(6)
        state_tree = self.Statement()
        condition = Node("condition")
        condition.AddChild(expr_tree)
        tree.AddChild(condition)
        state_tree.Rename("statements")
        tree.AddChild(state_tree)

        if (self.la.kind == 21):
            self.Get()
            else_state_tree = self.Statement()
            else_state_tree.Rename("OTNUD")
            tree.AddChild(else_state_tree)

        return tree

    def ReturnStatement(self):
        self.Expect(18)
        if (self.StartOf(3)):
            tree = self.Expression()
        self.Expect(17)
        return tree

    def WhileStatement(self):
        tree = Node(value='DOKOLE', t='key')
        self.Expect(19)
        self.Expect(5)
        expr_tree = self.Expression()
        self.Expect(6)
        state_tree = self.Statement()
        condition = Node("condition")
        condition.AddChild(expr_tree)
        tree.AddChild(condition)
        state_tree.Rename("statements")
        tree.AddChild(state_tree)

        return tree

    def DeclrationOrStatement(self):
        t = Node()
        if self.StartOf(1):
            declar_tree = self.LocalDeclaration()
            t = declar_tree
        elif self.StartOf(4):
            stat_tree = self.Statement()
            t = stat_tree
        else:
            self.SynErr(42)
        return t

    def LocalDeclaration(self):
        type = self.Type()
        self.Expect(1)
        name = type + " " + self.token.val;
        tree = Node(value=name, t='decl')
        if self.la.kind == 5:
            self.Get()
            if (self.StartOf(1)):
                fparams = self.FormalParamList()
            self.Expect(6)
        elif self.la.kind == 16:
            self.Get()
            expr_tree = self.Expression()
            tree.Rename(name + ' =')
            tree.AddChild(expr_tree)

        else:
            self.SynErr(43)
        self.Expect(17)
        return tree

    def Expression(self):
        cond_tree = self.Conditional()
        tree = cond_tree
        while self.StartOf(5):
            op = self.AssignmentOperator()
            expr_tree = self.Expression()
            tree = Node(t='expr')
            tree.AddChild(cond_tree)
            tree.Rename(op)
            tree.AddChild(expr_tree)

        return tree

    def Conditional(self):
        tree = self.LogORExp()
        return tree

    def AssignmentOperator(self):
        if self.la.kind == 16:
            self.Get()
            op = self.token.val
        elif self.la.kind == 34:
            self.Get()
            op = self.token.val
        elif self.la.kind == 35:
            self.Get()
            op = self.token.val
        elif self.la.kind == 36:
            self.Get()
            op = self.token.val
        elif self.la.kind == 37:
            self.Get()
            op = self.token.val
        else:
            self.SynErr(44)
        return op

    def LogORExp(self):
        and_tree_1 = self.LogANDExp()
        tree = and_tree_1
        trees = [and_tree_1]
        while self.la.kind == 22:
            self.Get()
            and_tree_2 = self.LogANDExp()
            trees.append(and_tree_2)

        tree = ConnectSame(tree, trees, 'ALI')
        return tree

    def LogANDExp(self):
        eq_tree_1 = self.EqualExp()
        tree = eq_tree_1
        trees = [eq_tree_1]
        while self.la.kind == 23:
            self.Get()
            eq_tree_2 = self.EqualExp()
            trees.append(eq_tree_2)

        tree = ConnectSame(tree, trees, 'DA')
        return tree

    def EqualExp(self):
        rel_tree_1 = self.RelationExp()
        tree = (rel_tree_1)
        trees = [rel_tree_1]
        while self.la.kind == 24:
            self.Get()
            rel_tree_2 = self.RelationExp()
            trees.append(rel_tree_2)

        tree = ConnectSame(tree, trees, '==')
        return tree

    def RelationExp(self):
        sub_tree_1 = self.AddExp()
        tree = sub_tree_1
        trees = [sub_tree_1];
        ops = []
        while self.StartOf(6):
            if self.la.kind == 25:
                self.Get()
                op = '<'
            elif self.la.kind == 26:
                self.Get()
                op = '>'
            elif self.la.kind == 27:
                self.Get()
                op = '<='
            else:
                self.Get()
                op = '>='
            sub_tree_2 = self.AddExp()
            ops.append(op)
            trees.append(sub_tree_2)

        tree = ConnectWithOps(tree, trees, ops)
        return tree

    def AddExp(self):
        mult_tree_1 = self.MultExp()
        tree = mult_tree_1
        trees = [mult_tree_1];
        ops = []
        while self.la.kind == 29 or self.la.kind == 30:
            if self.la.kind == 29:
                self.Get()
                op = self.token.val
            else:
                self.Get()
                op = self.token.val
            mult_tree_2 = self.MultExp()
            ops.append(op)
            trees.append(mult_tree_2)

        tree = ConnectWithOps(tree, trees, ops)
        return tree

    def MultExp(self):
        cast_tree_1 = self.CastExp()
        tree = cast_tree_1
        trees = [cast_tree_1];
        ops = []
        while self.la.kind == 31 or self.la.kind == 32 or self.la.kind == 33:
            if self.la.kind == 31:
                self.Get()
                op = "*"
            elif self.la.kind == 32:
                self.Get()
                op = "/"
            else:
                self.Get()
                op = "%"
            cast_tree_2 = self.CastExp()
            ops.append(op)
            trees.append(cast_tree_2)

        tree = ConnectWithOps(tree, trees, ops)
        return tree

    def CastExp(self):
        urary_tree = self.UnaryExp()
        tree = urary_tree
        return tree

    def UnaryExp(self):
        if self.StartOf(7):
            s = self.PostFixExp()
            tree = s
        elif self.StartOf(8):
            op = self.UnaryOperator()
            cast_tree = self.CastExp()
            tree = Node()
            tree.Rename(op)
            tree.AddChild(cast_tree)

        else:
            self.SynErr(45)
        return tree

    def PostFixExp(self):
        child = self.Primary()
        tree = child;
        while self.la.kind == 5 or self.la.kind == 9:
            if self.la.kind == 9:
                self.Get()
                expression_tree = self.Expression()
                self.Expect(10)
                tree.AddChild(expression_tree)
            else:
                f_call_tree = self.FunctionCall()
                tree = f_call_tree

        return tree

    def UnaryOperator(self):
        if self.la.kind == 29:
            self.Get()
            op = self.token.val
        elif self.la.kind == 30:
            self.Get()
            op = self.token.val
        elif self.la.kind == 31:
            self.Get()
            op = self.token.val
        elif self.la.kind == 38:
            self.Get()
            op = self.token.val
        else:
            self.SynErr(46)
        return op

    def Primary(self):
        if self.la.kind == 1:
            self.Get()
            prim = Node(value=self.token.val, t='identifier', start_pos=self.token.pos,
                        end_pos=(self.token.pos + len(self.token.val)))
        elif self.la.kind == 3:
            self.Get()
            prim = Node(value=self.token.val, t='string', start_pos=self.token.pos,
                        end_pos=(self.token.pos + len(self.token.val)))
        elif self.la.kind == 2:
            self.Get()
            prim = Node(value=self.token.val, t='number', start_pos=self.token.pos,
                        end_pos=(self.token.pos + len(self.token.val)))
        elif self.la.kind == 5:
            self.Get()
            start_pos = self.token.pos
            tree = self.Expression()
            self.Expect(6)
            end_pos = self.token.pos
            prim = Node(value="()", t='expr', start_pos=start_pos, end_pos=end_pos)
            prim.AddChild(tree)

        else:
            self.SynErr(47)
        return prim

    def FunctionCall(self):
        res = Node(value=self.token.val, t='call')
        self.Expect(5)
        if (self.StartOf(3)):
            expr = self.ActualParameters()
            res.AddChild(expr)
        self.Expect(6)
        return res

    def ActualParameters(self):
        tree = Node('params')
        expr = self.Expression()
        tree.AddChild(expr)
        while self.la.kind == 7:
            self.Get()
            expr2 = self.Expression()
            tree.AddChild(expr2)

        return tree

    def Parse(self, scanner):
        self.scanner = scanner
        self.la = Token()
        self.la.val = u''
        self.Get()
        return self.VeKrestKrest()
        self.Expect(0)

    set = [
        [T, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x,
         x, x, x, x],
        [x, x, x, x, x, x, x, x, T, x, x, T, T, T, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x,
         x, x, x, x],
        [x, T, T, T, x, T, x, x, T, x, x, T, T, T, T, x, x, x, T, T, T, x, x, x, x, x, x, x, x, T, T, T, x, x, x, x, x,
         x, T, x, x],
        [x, T, T, T, x, T, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, T, T, T, x, x, x, x, x,
         x, T, x, x],
        [x, T, T, T, x, T, x, x, x, x, x, x, x, x, T, x, x, x, T, T, T, x, x, x, x, x, x, x, x, T, T, T, x, x, x, x, x,
         x, T, x, x],
        [x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, T, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, T, T, T,
         T, x, x, x],
        [x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, T, T, T, T, x, x, x, x, x, x, x, x,
         x, x, x, x],
        [x, T, T, T, x, T, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x,
         x, x, x, x],
        [x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, T, T, T, x, x, x, x, x,
         x, T, x, x]

    ]

    errorMessages = {

        0: "EOF expected",
        1: "identifier expected",
        2: "number expected",
        3: "string expected",
        4: "\"->\" expected",
        5: "\"(\" expected",
        6: "\")\" expected",
        7: "\",\" expected",
        8: "\"celina\" expected",
        9: "\"[\" expected",
        10: "\"]\" expected",
        11: "\"bukvi\" expected",
        12: "\"drob\" expected",
        13: "\"pravda\" expected",
        14: "\"{\" expected",
        15: "\"}\" expected",
        16: "\"=\" expected",
        17: "\";\" expected",
        18: "\"vozdat\" expected",
        19: "\"dokole\" expected",
        20: "\"koli\" expected",
        21: "\"otnud\" expected",
        22: "\"ali\" expected",
        23: "\"da\" expected",
        24: "\"==\" expected",
        25: "\"<\" expected",
        26: "\">\" expected",
        27: "\"<=\" expected",
        28: "\">=\" expected",
        29: "\"+\" expected",
        30: "\"-\" expected",
        31: "\"*\" expected",
        32: "\"/\" expected",
        33: "\"%\" expected",
        34: "\"*=\" expected",
        35: "\"/=\" expected",
        36: "\"%=\" expected",
        37: "\"+=\" expected",
        38: "\"ne\" expected",
        39: "??? expected",
        40: "invalid Type",
        41: "invalid Statement",
        42: "invalid DeclrationOrStatement",
        43: "invalid LocalDeclaration",
        44: "invalid AssignmentOperator",
        45: "invalid UnaryExp",
        46: "invalid UnaryOperator",
        47: "invalid Primary",
    }

