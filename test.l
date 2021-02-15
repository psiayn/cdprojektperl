%{
#include <stdio.h>
#include<stdlib.h>
#include<string.h>
#include "y.tab.h"
extern int yylineno;
extern YYSTYPE yylval;
%}

alpha  [A-Za-z]
digit  [0-9]
under  [_]
name   [A-Za-z_]([A-Za-z_]|[0-9])*

%%

[ \t]          /*ignorance go brrrr*/
#.*            /*ignorance go brrrr*/
[\n]           {yylineno++;}

"use"          {return(USE);}
"print"        {return(PRINT);}
"my"           {return(VARINIT);}
"until"        {return(UNTIL);}
"foreach"      {return(FOREACH);}
"return"       {return(RETURN);}

({digit})*                                      {yylval.ival = atoi(yytext); return(INT);}
({digit})+([Ee][+-]?({digit})+)                 {yylval.doub = atof(yytext); return(DOUBLE); }
({digit})*"."({digit})+([Ee][+-]?({digit})+)?   {yylval.doub = atof(yytext); return(DOUBLE); }
({digit})+"."({digit})*([Ee][+-]?({digit})+)?   {yylval.doub = atof(yytext); return(DOUBLE); }

{name}         {strcpy(yylval.name, yytext); return(IDENTIFIER);}
\"[.]*\"       {strcpy(yylval.str, yytext); return(STRING);}

"&&"           {return(AND);}
"||"           {return(OR);}

"=="           {return(EQ);}
">"            {return(GT);}
"<"            {return(LT);}
">="           {return(GTE);}
"<="           {return(LTE);}
"!="           {return(NE);}

";"            {return(';'); }    
","            {return(','); }
"="            {return('='); }
"~"            {return('~'); }
"&"            {return('&'); }
"|"            {return('|'); }
"%"            {return('%'); }
"@"            {return('@'); }
"$"            {return('$'); }
"+"            {return('+'); }
"-"            {return('-'); }
"/"            {return('/'); }
"*"            {return('*'); }
"{"            {return('{'); }
"}"            {return('}'); }
"["            {return('['); }
"]"            {return(']'); }
"("            {return('('); }
")"            {return(')'); }

%%
