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
$[A-Za-z]+   return VARNAME;
@[A-Za-z]+   return ARRNAME;
=            return EQ;
[0-9]+       return NUMBER;
;            return SEMI;
[A-Za-z]+    return IDENTIFIER;
%%
