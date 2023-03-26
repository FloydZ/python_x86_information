grammar intel_operation_language;


prog
	: base_block* EOF
	;

/* base_block: (for_block | dowhile_block | if_block | base_line ); */
base_block: base_line;

base_line: EXPRESSION DEFINITION EXPRESSION+;


DEFINITION
	: ':='
	;

EXPRESSION
	: VARIABLE
	| OPERATOR
	| INT
	| TERNARYOPERATOR
	;

/*
	(A > B ? C : D)
*/
TERNARYOPERATOR
	: '(' COMPARISON '?' EXPRESSION ':' EXPRESSION ')'
	;

COMPARISON
	: ( VARIABLE | INT ) OPERATOR ( VARIABLE | INT )
	;

VARIABLE
	: NAME+ ACCESSOPERATOR?
	;


/* Memory/Bit Accessors: (ONLY THE ACCESSORS, NOT `tmp`)
	tmp[31:0]
	tmp[0]
	tmp[out+32: 32]
	tmp[out+32: out+0]
*/
ACCESSOPERATOR
	: '[' ACCESSOPERATORNAME ':' ACCESSOPERATORNAME ']' 
	| '[' ACCESSOPERATORNAME ']'
	;

ACCESSOPERATORNAME
	: NAME '+' (NAME | INT)
	| (NAME | INT)+
	;

OPERATOR
	: '+' | '-' | '=' | '>' | '<'
	;

NAME
	: [a-zA-Z_]+
	;

INT
	: [0-9]+
	;

EOL
   : [\n]+
   ;

WS
	: [ \n\t\r]+ -> skip
	;
