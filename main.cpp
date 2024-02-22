#include <iostream>
#include <wchar.h>
#include "parser_src/Parser.h"
#include "parser_src/Scanner.h"
 
#include <string>
 
void parse(std::string name)
{
    wchar_t *file  = coco_string_create(name.c_str());

    Scanner *scanner = new Scanner(file);
    Parser *parser   = new Parser(scanner);
    parser->Parse();

    delete parser;
    delete scanner;
    delete file;
}
 
int main(int argc, char *argv[])
{
    if (argc == 1) {
        parse("../in.txt");
        return 0;
    }

    if (argc == 2) {
        parse(argv[1]);
        return 0;
    }

    return 0;
}