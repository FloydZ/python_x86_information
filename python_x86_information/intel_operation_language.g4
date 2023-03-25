grammar intel_operation_language;

prog: base_block* EOF;
WS: [ \n\t\r]+ -> channel(HIDDEN);

/* base_block: (for_block | dowhile_block | if_block | base_line ); */
base_block: ( base_line );

base_line: NAME DEFINITION (base_line | INT | OPERATION | NAME);

OPERATION: ( '+' | '-' | '=' );
DEFINITION: ':=';
NAME: [a-zA-Z]+;
INT: [0-9]+;
