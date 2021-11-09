
#Actividad 3.3: Analizador léxico para lenguaje SQL

#Nombre y matricula de los alumnos:
#Jesús Abraham Canul Couoh (19070034)
#Evan Jazheel Ku Canche (19070048)
#Fernando Javier Noh Requena (19070052)
#Semestre y grupo: 5°B
#Fecha de entrega: 09 de Noviembre del 2021

#Librerías que usaremos para este programa:
import ply.lex as lex
import sys
from tabulate import tabulate

#Aqui agregamos las palabras reservadas que maneja el lenguaje SQL
reserved = {
    'add':'ADD',
    'all':'ALL',
    'alter':'ALTER',
    'analyze':'ANALYZE',
    'and':'AND',
    'as':'AS',
    'asc':'ASC',
    'asensitive':'ASENSITIVE',
    'before':'BEFORE',
    'between': 'BETWEEN',
    'both':'BOTH',
    'blob':'BLOB',
    'by':'BY',
    'call':'CALL',
    'cascade':'CASCADE',
    'case':'CASE',
    'change':'CHANGE',
    'char':'CHAR',
    'character':'CHARACTER',
    'check':'CHECK',
    'collate':'COLLATE',
    'condition':'CONDITION',
    'constraint': 'CONSTRAINT',
    'create':'CREATE',
    'database':'DATEBASE',
    'default':'DEFAULT',
    'delayed':'DELAYED',
    'delete':'DELETE',
    'describe':'DESCRIBE',
    'declare':'DECLARE',
    'drop':'DROP',
    'each': 'EACH',
    'else':'ELSE',
    'elseif':'ELSEIF',
    'enclosed':'ENCLOSED',
    'escaped':'ESCAPED',
    'exit':'EXIT',
    'explain':'EXPLAIN',
    'false':'FALSE',
    'for':'FOR',
    'force':'FORCE',
    'foreign':'FOREIGN',
    'from':'FROM',
    'grant':'GRANT',
    'group':'GROUP',
    'having':'HAVING',
    'if':'IF',
    'insert':'INSERT',
    'ignore': 'IGNORE',
    'into':'INTO',
    'inner':'INNER',
    'in':'IN',
    'int':'INT',
    'intenger':'INTENGER',
    'index':'INDEX',
    'infile':'INFILE',
    'float':'FLOAT',
    'text':'TEXT',
    'is':'IS',
    'join':'JOIN',
    'key':'KEY',
    'kill':'KILL',
    'keys':'KEYS',
    'left':'LEFT',
    'limit': 'LIMIT',
    'lines':'LINES',
    'leave':'LEAVE',
    'like': 'LIKE',
    'load': 'LOAD',
    'leading':'LEADING',
    'lock':'LOCK',
    'loop': 'LOOP',
    'match':'MATCH',
    'mod':'MOD',
    'modifies':'MODIFIES',
    'natural':'NATURAL',
    'not':'NOT',
    'null':'NULL',
    'on':'ON',
    'optimize':'OPTIMIZE',
    'option':'OPTION',
    'or':'OR',
    'order':'ORDER',
    'out':'OUT',
    'outer': 'OUTER',
    'outfile':'OUTFILE',
    'precision': 'PRECISION',
    'primary':'PRIMARY',
    'procedure':'PROCEDURE',
    'purge':'PURGE',
    'raido':'RAIDO',
    'read':'READ',
    'reads':'READS',
    'real':'REAL',
    'references':'REFERENCES',
    'regexp':'REGEXP',
    'rename':'RENAME',
    'release':'RELEASE',
    'repeat':'REPEAT',
    'replace':'REPLACE',
    'return':'RETURN',
    'restrict':'RESTRICT',
    'require':'REQUIRE',
    'schema':'SCHEMA',
    'schemas':'SCHEMAS',
    'select':'SELECT',
    'sensitive':'SENSITIVE',
    'separator':'SEPARATOR',
    'set':'SET',
    'soname':'SONAME',
    'spatial':'SPATIAL',
    'specific':'SPECIFIC',
    'sql':'SQL',
    'show':'SHOW',
    'table':'TABLE',
    'terminated':'TERMINATED',
    'then':'THEN',
    'to':'TO',
    'trailing':'TRAILING',
    'trigger':'TRIGGER',
    'true':'TRUE',
    'undo':'UNDO',
    'union':'UNION',
    'update':'UPDATE',
    'unique':'UNIQUE',
    'unlock':'UNLOCK',
    'unsigned':'UNSIGNED',
    'upgrade':'UPGRADE',
    'usage':'USAGE',
    'use':'USE',
    'using':'USING',
    'values':'VALUES',
    'varchar': 'VARCHAR',
    'varying':'VARYING',
    'when':'WHEN',
    'where':'WHERE',
    'while':'WHILE',
    'with':'WITH',
    'write':'WRITE',
    'xor':'XOR',
    'zerofill': 'ZEROFILL',
    'date':'DATE',
    'time':'TIME',

}

#Aquí enlistamos los tokens que usaremos, dividiendolos por secciones para identidentificarlos mejor:
tokens = list(reserved.values()) + [
    # Simbolos
    'ASSIGN',
    'MOD',
    'PLUS',
    'PLUSPLUS',
    'PLUSEQUAL',
    #'MINUS',
    #'MINUSMINUS',
    #'MINUSEQUAL',
    'TIMES',
    #'DIVIDE',
    'LESS',
    'LESSEQUAL',
    'GREATER',
    'GREATEREQUAL',
    'EQUAL',
    'DEQUAL',
    #'DISTINT',
    #'ISEQUAL',
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBLOCK',
    'RBLOCK',
    'COLON',
    'AMPERSANT',
    'HASHTAG',
    'DOT',
    'QUESTIONMARK',
    'COMILLASIMPLE',
    'COMILLASDOBLES',

#--------------------------------------------------------------------------------------------------------------------------
    #Variables
    'DOLLAR',
    'FECHA',
    'TIEMPO',
    'NUMERO_DECIMAL',
    'NUMERO_ENTERO',
#---------------------------------------------------------------------------------------------------------------------------
    # Otros
    'COMENTARIO',
    'COMENTARIO_EN_LINEAS',
    'VARIABLE',
    'NUMBER',
    'CADENA',
    'ID',
]
#---------------------------------------------------------------------------------------------------------------------------
#Expresiones regulares para los tokens simples:
t_MOD = r'%'
t_TIMES  = r'\*'
t_EQUAL = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_SEMICOLON = ';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBLOCK = r'{'
t_RBLOCK = r'}'
t_COLON = r':'
t_AMPERSANT = r'\&'
t_HASHTAG = r'\#'
t_DOT = r'\.'
t_COMILLASIMPLE = r'\''
t_COMILLASDOBLES = r'\"'
t_QUESTIONMARK = r'\?'
#_________________________________________________________________________________________________________________________________
#Expresiones para los tokens de variables
t_DOLLAR = r'\$'
t_FECHA= r'\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])*'
t_TIEMPO= r'(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)'
t_NUMERO_DECIMAL =r'[0-9][.][0-9]'
t_NUMERO_ENTERO = r'[\d]+'

#-----------------------------------------------------------------------------------------------------------------------------------
#definimos los tokens:

#En esta función identificamos que palabras son variables y cuales palabras reservadas:
def t_VARIABLE(t):
    r'[a-zA-Z]([\w])*'
    if t.value in reserved:
        t.type = reserved[t.value]  #Llamamos a la lista de palabras reservadas y evaluamos si coincide con alguna
        return t #Si encontro una coincidencia, regresa esa misma opción
    else:
        return t #Si no, se considera como una variable

# Con la anterior función, checamos las palabras reservadas
#Esto nos ayuda a reducir el número de expresiones regulares y mejora el procedimiento del programa

#--------------------------------------------------------------------------------------------------------------------------------------

#Ahora, definimos el resto de tokens que faltan:
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]  # Check for reserved words
        return t
    else:
        t_error(t)

def t_CADENA(t):
    r'\"([^\"].)*\"'
    return t

def t_LESSEQUAL(t):
    r'<='
    return t

def t_GREATEREQUAL(t):
    r'>='
    return t

def t_ASSIGN(t):
    r'=>'
    return t

def t_DEQUAL(t):
    r'!='
    return t

def t_ISEQUAL(t):
    r'=='
    return t

"""def t_MINUSMINUS(t):
    r'--'
    return t"""

"""def t_PLUSPLUS(t):
    r'\+\+'
    return t"""

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_space(t):
    r'\s+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_COMENTARIO(t):
    r'\--(.)*?\n+'
    t.lexer.lineno += 1
    return t

def t_COMENTARIO_EN_LINEAS(t):
    #r'\/*(.|A-Za-z)*?\n+\*/'
    r'(\/*)(.|\n)*?(\*/)'
    #r'[/\*][.]*?\n+[*/]'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print("Lexical error: " + str(t.value))
    t.lexer.skip(1)

#--------------------------------------------------------------------------------------------------------------------------------------

#Manejo, proceso e impresión de datos procedentes del archivo txt
def test(data, lexer):
    lexer.input(data)
    i = 1  # Representa la línea
    while True:
        tok = lexer.token()
        if not tok:
            break
        #Imprimimos los resultados en una tabla con tabulate y le damos formato:
        datos=[[str(i), str(tok.lineno), str(tok.type), str(tok.value)]]
        print(tabulate(datos, headers=["Número de linea", "Linea de código", "Tipo de Token", "Valor"], tablefmt="fancy_grid"))
        i += 1

lexer = lex.lex()

#Ingreso del archivo txt a usar
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        fin = sys.argv[1]
    else:
        fin = 'index.sql.txt' #Para usar un archivo, basta con agregar el nombre aquí, pero tiene que estar en el mismo directorio del programa
        f = open(fin, 'r') #Se abre y se usa r para la lectura del txt
        data = f.read() #Se lee el contenido del txt
        test(data, lexer) #Se envia los datos a la función test