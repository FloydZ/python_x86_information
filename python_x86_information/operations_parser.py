
test = ['\n'
       'DEFINE SELECT4(src, control) {\n'
       '\tCASE(control[1:0]) OF\n'
       '\t0:\ttmp[63:0] := src[63:0]\n'
       '\t1:\ttmp[63:0] := src[127:64]\n'
       '\t2:\ttmp[63:0] := src[191:128]\n'
       '\t3:\ttmp[63:0] := src[255:192]\n'
       '\tESAC\n'
       '\tRETURN tmp[63:0]\n'
       '}\n'
       'dst[63:0] := SELECT4(a[255:0], imm8[1:0])\n'
       'dst[127:64] := SELECT4(a[255:0], imm8[3:2])\n'
       'dst[191:128] := SELECT4(a[255:0], imm8[5:4])\n'
       'dst[255:192] := SELECT4(a[255:0], imm8[7:6])\n'
       'dst[MAX:256] := 0\n'
       '\t',

       'DEFINE SELECT4(src, control) {\n'
       '\tCASE(control[1:0]) OF\n'
       '\t0:\ttmp[63:0] := src[63:0]\n'
       '\t1:\ttmp[63:0] := src[127:64]\n'
       '\t2:\ttmp[63:0] := src[191:128]\n'
       '\t3:\ttmp[63:0] := src[255:192]\n'
       '\tESAC\n'
       '\tRETURN tmp[63:0]\n'
       '}\n'
       'tmp_dst[63:0] := SELECT4(a[255:0], imm8[1:0])\n'
       'tmp_dst[127:64] := SELECT4(a[255:0], imm8[3:2])\n'
       'tmp_dst[191:128] := SELECT4(a[255:0], imm8[5:4])\n'
       'tmp_dst[255:192] := SELECT4(a[255:0], imm8[7:6])\n'
       'tmp_dst[319:256] := SELECT4(a[511:256], imm8[1:0])\n'
       'tmp_dst[383:320] := SELECT4(a[511:256], imm8[3:2])\n'
       'tmp_dst[447:384] := SELECT4(a[511:256], imm8[5:4])\n'
       'tmp_dst[511:448] := SELECT4(a[511:256], imm8[7:6])\n'
       'FOR j := 0 to 7\n'
       '\ti := j*64\n'
       '\tIF k[j]\n'
       '\t\tdst[i+63:i] := tmp_dst[i+63:i]\n'
       '\tELSE\n'
       '\t\tdst[i+63:i] := 0\n'
       '\tFI\n'
       'ENDFOR\n'
       'dst[MAX:512] := 0\n'
       '\t',

        'dst[255:0] := (a[255:0] XOR b[255:0])'
        'dst[MAX:256] := 0',
        """
tmp := 0
IF a == 0
	// MEM[index+31:index] is undefined
	dst := 0
ELSE
	DO WHILE ((tmp < 32) AND a[tmp] == 0)
		tmp := tmp + 1
	OD
	MEM[index+31:index] := tmp
	dst := (tmp == 31) ? 0 : 1
FI
        """,
        'dst[63:0] := ZeroExtend64(tmp[(start[7:0] + len[7:0] - 1):start[7:0]])',

        """
FOR i := 0 to 3
	q := i * 64
	FOR j := 0 to 7
		tmp8 := 0
		ctrl := a[q+j*8+7:q+j*8] & 63
		FOR l := 0 to 7
			tmp8[l] := b[q+((ctrl+l) & 63)]
		ENDFOR
		IF k[i*8+j]
			dst[q+j*8+7:q+j*8] := tmp8[7:0]
		ELSE
			dst[q+j*8+7:q+j*8] := 0
		FI
	ENDFOR
ENDFOR
dst[MAX:256] := 0
"""
        ]

#for t in test:
#    print(str(t))

import sys
from antlr4 import *
from antlr4.tree import Trees
from python_x86_information.intel_operation_languageLexer import intel_operation_languageLexer as Lexer
from python_x86_information.intel_operation_languageParser import intel_operation_languageParser as Parser


def main(argv):
    input_stream = InputStream('tmp := 1')
    lexer = Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)
    tree = parser.prog()

if __name__ == "__main__":
    main(sys.argv)
