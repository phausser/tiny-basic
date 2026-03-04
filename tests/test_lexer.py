from tinybasic.lexer import Lexer


def compact(tokens):
    return [(t.type, t.value) for t in tokens]


def test_lex_single_line_program_tokens():
    src = '10 LET A = 12\n20 PRINT "HI"\n'
    tokens = Lexer().tokenize(src)

    assert compact(tokens) == [
        ("NUMBER", 10),
        ("KEYWORD", "LET"),
        ("IDENT", "A"),
        ("OP", "="),
        ("NUMBER", 12),
        ("NEWLINE", "\n"),
        ("NUMBER", 20),
        ("KEYWORD", "PRINT"),
        ("STRING", "HI"),
        ("NEWLINE", "\n"),
    ]


def test_lex_keywords_and_operators():
    src = "IF A+2*3 THEN GOTO 100\nEND\n"
    tokens = Lexer().tokenize(src)

    assert compact(tokens) == [
        ("KEYWORD", "IF"),
        ("IDENT", "A"),
        ("OP", "+"),
        ("NUMBER", 2),
        ("OP", "*"),
        ("NUMBER", 3),
        ("KEYWORD", "THEN"),
        ("KEYWORD", "GOTO"),
        ("NUMBER", 100),
        ("NEWLINE", "\n"),
        ("KEYWORD", "END"),
        ("NEWLINE", "\n"),
    ]


def test_rem_skips_comment_text_until_newline():
    src = "REM this is ignored\nPRINT 1\n"
    tokens = Lexer().tokenize(src)

    assert compact(tokens) == [
        ("KEYWORD", "REM"),
        ("NEWLINE", "\n"),
        ("KEYWORD", "PRINT"),
        ("NUMBER", 1),
        ("NEWLINE", "\n"),
    ]
