%{
#include <stdio.h>
#include "y.tab.h"
%}

%%
\".*\"       return STRING;
[ \n\t]      /*ignorance go brrrr*/
#.*          /*ignorance go brrrr*/
use          return USE;
print        return PRINT;
my           return VAR;
until        return UNTIL;
$[A-Za-z]+   return VARNAME;
@[A-Za-z]+   return ARRNAME;
\=            return EQ;
\=\=           return EQV;
\>            return GT;
\<            return LT;
[0-9]+       return NUMBER;
;            return SEMI;
\(           return OP;
\)           return CL;
,            return COMMA;
\{            return BLOCKOP;
\}            return BLOCKCL;
[A-Za-z]+    return IDENTIFIER;
%%
