%{
#include <stdio.h>
#include <string.h>
int lineno;
%}

%token STRING USE PRINT NUMBER SEMI IDENTIFIER VAR VARNAME EQ ARRNAME

%%
start: 
          | start command
          ;

command:
       use
       |
       print
       |
       variable_declaration
       |
       array_declaration
       ;
use:
       USE IDENTIFIER SEMI {
	 printf("use statement\n");
       }
       ;

print:
       PRINT STRING SEMI {
	 printf("print string\n");
       }
       |
       PRINT NUMBER SEMI {
	 printf("print number\n");
       }
       ;

variable_declaration:
       VAR VARNAME SEMI {
	 printf("Variable declared\n");
       }
       |
       VAR VARNAME EQ NUMBER SEMI {
	 printf("numerical variable declaration\n");
       }
       |
       VAR VARNAME EQ STRING SEMI {
	 printf("string variable declaration\n");
       }
       ;
array_declaration:
       VAR ARRNAME SEMI {
	 printf("Array declared\n");
       }
       |
       VAR ARRNAME EQ '(' array_inner ')' {
	 printf("Array initialized\n");
       }
       ;

array_inner:
       STRING ',' array_inner
       |
       STRING
       |
       NUMBER
       |
       NUMBER ',' array_inner
       ;
%%


int yyerror(char *s) {
  fprintf(stderr, "ERROR: %s\n", s);
}

int yywrap() {
  return 1;
}

main(void) {
  yyparse();
}
