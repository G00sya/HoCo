import os.path

from src.parser.Parser import *

srcName = 'example.txt'
dirName, fileName = os.path.split(srcName)

#print(dirName, fileName)

try:
   s = open(srcName, 'r', encoding='utf-8' )
   try:
      strVal = s.read()
   except IOError:
      sys.stdout.write( '-- Compiler Error: Failed to read from source file "%s"\n' % srcName )

   try:
      s.close( )
   except IOError:
      raise RuntimeError( '-- Compiler Error: cannot close source file "%s"' % srcName )
except IOError:
   raise RuntimeError( '-- Compiler Error: Cannot open file "%s"' % srcName )

scanner = Scanner(strVal)
parser = Parser()

Errors.Init(fileName, dirName, False, parser.getParsingPos, parser.errorMessages)

ast = parser.Parse(scanner)
Errors.Summarize(scanner.buffer)
ast

if Errors.count != 0:
   sys.exit(1)

