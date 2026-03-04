"""Lexer for Tiny BASIC source code."""

from dataclasses import dataclass


KEYWORDS = {"PRINT", "LET", "INPUT", "IF", "THEN", "GOTO", "END", "REM"}


@dataclass(frozen=True)
class Token:
    """Single lexed token."""

    type: str
    value: str | int
    line: int
    column: int


class Lexer:
    """Tokenizes Tiny BASIC source into a stream of tokens."""

    def tokenize(self, source: str) -> list[Token]:
        tokens: list[Token] = []
        i = 0
        line = 1
        col = 1
        length = len(source)

        while i < length:
            ch = source[i]

            if ch in {" ", "\t", "\r"}:
                i += 1
                col += 1
                continue

            if ch == "\n":
                tokens.append(Token("NEWLINE", "\n", line, col))
                i += 1
                line += 1
                col = 1
                continue

            if ch.isdigit():
                start = i
                start_col = col
                while i < length and source[i].isdigit():
                    i += 1
                    col += 1
                tokens.append(Token("NUMBER", int(source[start:i]), line, start_col))
                continue

            if ch == '"':
                start_col = col
                i += 1
                col += 1
                start = i
                while i < length and source[i] != '"':
                    if source[i] == "\n":
                        raise ValueError(
                            f"Unterminated string at line {line}, column {start_col}"
                        )
                    i += 1
                    col += 1
                if i >= length:
                    raise ValueError(
                        f"Unterminated string at line {line}, column {start_col}"
                    )
                value = source[start:i]
                i += 1
                col += 1
                tokens.append(Token("STRING", value, line, start_col))
                continue

            if ch.isalpha():
                start = i
                start_col = col
                while i < length and (source[i].isalnum() or source[i] == "_"):
                    i += 1
                    col += 1
                word = source[start:i].upper()
                token_type = "KEYWORD" if word in KEYWORDS else "IDENT"
                tokens.append(Token(token_type, word, line, start_col))

                if word == "REM":
                    while i < length and source[i] != "\n":
                        i += 1
                        col += 1
                continue

            if ch in "+-*/()=<>,":
                tokens.append(Token("OP", ch, line, col))
                i += 1
                col += 1
                continue

            raise ValueError(f"Unexpected character {ch!r} at line {line}, column {col}")

        return tokens
