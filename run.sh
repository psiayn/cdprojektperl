#!/bin/bash
lex test.lex
yacc -d test.yacc
clang -o test y.tab.c lex.yy.c
clear
echo "OUT"
./test < test.pl
echo
echo
echo
echo "OG"
cat test.pl

./test < test.pl > ly_out
