"""Parser for Tiny BASIC tokens."""

from tinybasic.ast import (
    BinaryOp,
    GotoStatement,
    IfGotoStatement,
    LetStatement,
    Line,
    NumberLiteral,
    PrintStatement,
    StringLiteral,
    Variable,
)
from tinybasic.lexer import Token


class Parser:
    """Parses token streams into Tiny BASIC AST lines."""

    def __init__(self) -> None:
        self.tokens: list[Token] = []
        self.pos = 0

    def parse(self, tokens: list[Token]) -> list[Line]:
        self.tokens = tokens
        self.pos = 0
        lines: list[Line] = []

        while not self._at_end():
            if self._match("NEWLINE"):
                continue
            line_no = self._consume("NUMBER", "Expected line number at start of line")
            stmt = self._parse_statement()
            self._consume("NEWLINE", "Expected newline after statement")
            lines.append(Line(number=int(line_no.value), statement=stmt))

        return lines

    def _parse_statement(self) -> object:
        keyword = self._consume("KEYWORD", "Expected statement keyword")
        if keyword.value == "LET":
            ident = self._consume("IDENT", "Expected variable name after LET")
            self._consume("OP", "Expected '=' after variable name", expected_value="=")
            return LetStatement(name=str(ident.value), expression=self._parse_expression())
        if keyword.value == "PRINT":
            if self._check("STRING"):
                token = self._advance()
                return PrintStatement(expression=StringLiteral(value=str(token.value)))
            return PrintStatement(expression=self._parse_expression())
        if keyword.value == "GOTO":
            target = self._consume("NUMBER", "Expected line number after GOTO")
            return GotoStatement(target=int(target.value))
        if keyword.value == "IF":
            left = self._parse_expression()
            relop = self._consume("OP", "Expected relational operator in IF condition")
            if relop.value not in {"=", "<", ">"}:
                raise ValueError(
                    f"Unsupported relational operator {relop.value!r} at line {relop.line}, column {relop.column}"
                )
            right = self._parse_expression()
            self._consume("KEYWORD", "Expected THEN in IF statement", expected_value="THEN")
            self._consume("KEYWORD", "Expected GOTO after THEN", expected_value="GOTO")
            target = self._consume("NUMBER", "Expected line number after GOTO")
            return IfGotoStatement(
                left=left, op=str(relop.value), right=right, target=int(target.value)
            )
        raise ValueError(
            f"Unsupported statement {keyword.value} at line {keyword.line}, column {keyword.column}"
        )

    def _parse_expression(self) -> object:
        expr = self._parse_term()
        while self._check("OP", "+") or self._check("OP", "-"):
            op = str(self._advance().value)
            right = self._parse_term()
            expr = BinaryOp(op=op, left=expr, right=right)
        return expr

    def _parse_term(self) -> object:
        expr = self._parse_primary()
        while self._check("OP", "*") or self._check("OP", "/"):
            op = str(self._advance().value)
            right = self._parse_primary()
            expr = BinaryOp(op=op, left=expr, right=right)
        return expr

    def _parse_primary(self) -> object:
        if self._match("NUMBER"):
            token = self.tokens[self.pos - 1]
            return NumberLiteral(value=int(token.value))
        if self._match("IDENT"):
            token = self.tokens[self.pos - 1]
            return Variable(name=str(token.value))
        if self._match("OP", "("):
            expr = self._parse_expression()
            self._consume("OP", "Expected ')' after expression", expected_value=")")
            return expr
        token = self._peek()
        if token is None:
            raise ValueError("Unexpected end of input while parsing expression")
        raise ValueError(
            f"Unexpected token {token.type}:{token.value!r} at line {token.line}, column {token.column}"
        )

    def _consume(
        self, token_type: str, message: str, expected_value: str | None = None
    ) -> Token:
        if self._check(token_type, expected_value):
            return self._advance()
        token = self._peek()
        if token is None:
            raise ValueError(f"{message} at end of input")
        raise ValueError(f"{message} at line {token.line}, column {token.column}")

    def _match(self, token_type: str, expected_value: str | None = None) -> bool:
        if not self._check(token_type, expected_value):
            return False
        self._advance()
        return True

    def _check(self, token_type: str, expected_value: str | None = None) -> bool:
        token = self._peek()
        if token is None or token.type != token_type:
            return False
        if expected_value is not None and token.value != expected_value:
            return False
        return True

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _peek(self) -> Token | None:
        if self._at_end():
            return None
        return self.tokens[self.pos]

    def _at_end(self) -> bool:
        return self.pos >= len(self.tokens)
