from tinybasic.ast import BinaryOp, LetStatement, Line, NumberLiteral, PrintStatement, StringLiteral, Variable
from tinybasic.lexer import Lexer
from tinybasic.parser import Parser


def test_parse_let_and_print_lines_into_ast_list():
    source = '10 LET A = 1 + 2\n20 PRINT "HI"\n'
    tokens = Lexer().tokenize(source)

    ast_lines = Parser().parse(tokens)

    assert ast_lines == [
        Line(
            number=10,
            statement=LetStatement(
                name="A",
                expression=BinaryOp(
                    op="+",
                    left=NumberLiteral(1),
                    right=NumberLiteral(2),
                ),
            ),
        ),
        Line(number=20, statement=PrintStatement(expression=StringLiteral("HI"))),
    ]


def test_parse_print_expression_with_parentheses():
    source = "30 PRINT (A + 2) * 3\n"
    tokens = Lexer().tokenize(source)

    ast_lines = Parser().parse(tokens)

    assert ast_lines == [
        Line(
            number=30,
            statement=PrintStatement(
                expression=BinaryOp(
                    op="*",
                    left=BinaryOp(
                        op="+",
                        left=Variable("A"),
                        right=NumberLiteral(2),
                    ),
                    right=NumberLiteral(3),
                )
            ),
        )
    ]
