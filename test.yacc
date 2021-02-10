%{
#include <stdio.h>
#include <string.h>
int lineno;
%}

%token STRING USE PRINT NUMBER SEMI IDENTIFIER VAR VARNAME EQ ARRNAME OP CL COMMA BLOCKOP BLOCKCL UNTIL LT GT EQV

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
       |
       until
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
       VAR ARRNAME EQ OP array_init CL SEMI {
	 printf("Array initialized\n");
       }
       ;
array_init:
       STRING COMMA array_init
       |
       NUMBER COMMA array_init
       |
       STRING
       |
       NUMBER
       ;
until:
       UNTIL OP expr CL BLOCKOP start BLOCKCL {
	 printf("until case\n");
       }
       ;

expr:
       VARNAME GT NUMBER
       |
       VARNAME LT NUMBER
       |
       VARNAME EQV NUMBER
       |
       VARNAME GT EQ NUMBER
       |
       VARNAME LT EQ NUMBER
       |
       VARNAME GT VARNAME
       |
       VARNAME LT VARNAME
       |
       VARNAME EQV VARNAME
       |
       VARNAME GT EQ VARNAME
       |
       VARNAME LT EQ VARNAME
       |
       VARNAME EQV STRING
       |
       VARNAME
       |
       NUMBER GT NUMBER
       |
       NUMBER LT NUMBER
       |
       NUMBER EQV NUMBER
       |
       NUMBER GT EQ NUMBER
       |
       NUMBER LT EQ NUMBER
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

/*

*/
