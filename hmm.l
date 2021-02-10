%{
#include <stdio.h>
%}

%%
\".*\"       printf("STRING\n");
[ \n\t]      /*ignorance go brrrr*/
#.*          /*ignorance go brrrr*/


use          printf("USE\n");
print        printf("PRINT\n");
my           printf("var decl ");
[0-9]+       printf("NUMBER\n");
;            printf("SEMI\n");
[A-Za-z]+    printf("IDENTIFIER\n");
$[A-Za-z]+   printf("varname ");
@[A-Za-z]+   printf("arrname ");
=            printf("eq ");
%%
