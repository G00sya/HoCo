import sys


class Token(object):
    def __init__(self):
        self.kind = 0  # token kind
        self.pos = 0  # token position in the source text (starting at 0)
        self.col = 0  # token column (starting at 0)
        self.line = 0  # token line (starting at 1)
        self.val = ''  # token value
        self.next = None  # AW 2003-03-07 Tokens are kept in linked list


class Position(object):  # position of source code stretch (e.g. semantic action, resolver expressions)
    def __init__(self, buf, beg, len, col):
        assert isinstance(buf, Buffer)
        assert isinstance(beg, int)
        assert isinstance(len, int)
        assert isinstance(col, int)

        self.buf = buf
        self.beg = beg  # start relative to the beginning of the file
        self.len = len  # length of stretch
        self.col = col  # column number of start position

    def getSubstring(self):
        return self.buf.readPosition(self)


class Buffer(object):
    EOF = '\u0100'  # 256

    def __init__(self, s):
        self.buf = s
        self.bufLen = len(s)
        self.pos = 0
        self.lines = s.splitlines(True)

    def Read(self):
        if self.pos < self.bufLen:
            result = self.buf[self.pos]
            self.pos += 1
            return result
        else:
            return Buffer.EOF

    def ReadChars(self, numBytes=1):
        result = self.buf[self.pos: self.pos + numBytes]
        self.pos += numBytes
        return result

    def Peek(self):
        if self.pos < self.bufLen:
            return self.buf[self.pos]
        else:
            return Scanner.buffer.EOF

    def getString(self, beg, end):
        s = ''
        oldPos = self.getPos()
        self.setPos(beg)
        while beg < end:
            s += self.Read()
            beg += 1
        self.setPos(oldPos)
        return s

    def getPos(self):
        return self.pos

    def setPos(self, value):
        if value < 0:
            self.pos = 0
        elif value >= self.bufLen:
            self.pos = self.bufLen
        else:
            self.pos = value

    def readPosition(self, pos):
        assert isinstance(pos, Position)
        self.setPos(pos.beg)
        return self.ReadChars(pos.len)

    def __iter__(self):
        return iter(self.lines)


class Scanner(object):
    EOL = '\n'
    eofSym = 0

    charSetSize = 256
    maxT = 39
    noSym = 39
    start = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 3, 0, 0, 28, 0, 0, 6, 7, 26, 25, 8, 21, 0, 27,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 13, 23, 22, 24, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 10, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 0, 12, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        -1]
    valCh = u''  # current input character (for token.val)

    def __init__(self, s):
        self.buffer = Buffer(str(s))  # the buffer instance

        self.ch = '\0'  # current input character
        self.pos = -1  # column number of current character
        self.line = 1  # line number of current character
        self.lineStart = 0  # start position of current line
        self.oldEols = 0  # EOLs that appeared in a comment;
        self.NextCh()
        self.ignore = set()  # set of characters to be ignored by the scanner
        self.ignore.add(ord(' '))  # blanks are always white space
        self.ignore.add(9)
        self.ignore.add(10)
        self.ignore.add(13)

        # fill token list
        self.tokens = Token()  # the complete input token stream
        node = self.tokens

        node.next = self.NextToken()
        node = node.next
        while node.kind != Scanner.eofSym:
            node.next = self.NextToken()
            node = node.next

        node.next = node
        node.val = 'EOF'
        self.t = self.tokens  # current token
        self.pt = self.tokens  # current peek token

    def NextCh(self):
        if self.oldEols > 0:
            self.ch = Scanner.EOL
            self.oldEols -= 1
        else:
            self.ch = self.buffer.Read()
            self.pos += 1
            # replace isolated '\r' by '\n' in order to make
            # eol handling uniform across Windows, Unix and Mac
            if (self.ch == '\r') and (self.buffer.Peek() != '\n'):
                self.ch = Scanner.EOL
            if self.ch == Scanner.EOL:
                self.line += 1
                self.lineStart = self.pos + 1
                valCh = self.ch
        if self.ch != Buffer.EOF:
            self.ch = self.ch.lower()

    def CheckLiteral(self):
        lit = self.t.val.lower()
        if lit == "celina":
            self.t.kind = 8
        elif lit == "bukvi":
            self.t.kind = 11
        elif lit == "drob":
            self.t.kind = 12
        elif lit == "pravda":
            self.t.kind = 13
        elif lit == "vozdat":
            self.t.kind = 18
        elif lit == "dokole":
            self.t.kind = 19
        elif lit == "koli":
            self.t.kind = 20
        elif lit == "otnud":
            self.t.kind = 21
        elif lit == "ali":
            self.t.kind = 22
        elif lit == "da":
            self.t.kind = 23
        elif lit == "ne":
            self.t.kind = 38

    def NextToken(self):
        while ord(self.ch) in self.ignore:
            self.NextCh()

        self.t = Token()
        self.t.pos = self.pos
        self.t.col = self.pos - self.lineStart + 1
        self.t.line = self.line
        if ord(self.ch) < len(self.start):
            state = self.start[ord(self.ch)]
        else:
            state = 0
        buf = ''
        buf += str(self.ch)
        self.NextCh()

        done = False
        while not done:
            if state == -1:
                self.t.kind = Scanner.eofSym  # NextCh already done
                done = True
            elif state == 0:
                self.t.kind = Scanner.noSym  # NextCh already done
                done = True
            elif state == 1:
                if (self.ch >= '0' and self.ch <= '9'
                        or self.ch == '_'
                        or self.ch >= 'a' and self.ch <= 'z'):
                    buf += str(self.ch)
                    self.NextCh()
                    state = 1
                else:
                    self.t.kind = 1
                    self.t.val = buf
                    self.CheckLiteral()
                    return self.t
            elif state == 2:
                if (self.ch >= '0' and self.ch <= '9'):
                    buf += str(self.ch)
                    self.NextCh()
                    state = 2
                else:
                    self.t.kind = 2
                    done = True
            elif state == 3:
                if (self.ch >= ' ' and self.ch <= '!'
                        or self.ch >= '#' and ord(self.ch) <= 254):
                    buf += str(self.ch)
                    self.NextCh()
                    state = 3
                elif self.ch == '"':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 4
                else:
                    self.t.kind = Scanner.noSym
                    done = True
            elif state == 4:
                self.t.kind = 3
                done = True
            elif state == 5:
                self.t.kind = 4
                done = True
            elif state == 6:
                self.t.kind = 5
                done = True
            elif state == 7:
                self.t.kind = 6
                done = True
            elif state == 8:
                self.t.kind = 7
                done = True
            elif state == 9:
                self.t.kind = 9
                done = True
            elif state == 10:
                self.t.kind = 10
                done = True
            elif state == 11:
                self.t.kind = 14
                done = True
            elif state == 12:
                self.t.kind = 15
                done = True
            elif state == 13:
                self.t.kind = 17
                done = True
            elif state == 14:
                self.t.kind = 24
                done = True
            elif state == 15:
                self.t.kind = 27
                done = True
            elif state == 16:
                self.t.kind = 28
                done = True
            elif state == 17:
                self.t.kind = 34
                done = True
            elif state == 18:
                self.t.kind = 35
                done = True
            elif state == 19:
                self.t.kind = 36
                done = True
            elif state == 20:
                self.t.kind = 37
                done = True
            elif state == 21:
                if self.ch == '>':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 5
                else:
                    self.t.kind = 30
                    done = True
            elif state == 22:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 14
                else:
                    self.t.kind = 16
                    done = True
            elif state == 23:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 15
                else:
                    self.t.kind = 25
                    done = True
            elif state == 24:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 16
                else:
                    self.t.kind = 26
                    done = True
            elif state == 25:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 20
                else:
                    self.t.kind = 29
                    done = True
            elif state == 26:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 17
                else:
                    self.t.kind = 31
                    done = True
            elif state == 27:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 18
                else:
                    self.t.kind = 32
                    done = True
            elif state == 28:
                if self.ch == '=':
                    buf += str(self.ch)
                    self.NextCh()
                    state = 19
                else:
                    self.t.kind = 33
                    done = True

        self.t.val = buf
        return self.t

    def Scan(self):
        self.t = self.t.next
        self.pt = self.t.next
        return self.t

    def Peek(self):
        self.pt = self.pt.next
        while self.pt.kind > self.maxT:
            self.pt = self.pt.next

        return self.pt

    def ResetPeek(self):
        self.pt = self.t
