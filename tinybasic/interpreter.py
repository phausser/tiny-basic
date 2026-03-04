"""Core Tiny BASIC interpreter implementation."""

from tinybasic.ast import (
    BinaryOp,
    GotoStatement,
    IfGotoStatement,
    LetStatement,
    NumberLiteral,
    PrintStatement,
    StringLiteral,
    Variable,
)
from tinybasic.lexer import Lexer
from tinybasic.parser import Parser


class TinyBasicInterpreter:
    """Minimal Tiny BASIC interpreter for LET and PRINT."""

    def __init__(self) -> None:
        self.variables: dict[str, int | float] = {}
        self.output: list[str] = []

    def run(self, source: str) -> str:
        self.variables = {}
        self.output = []

        normalized = self._ensure_line_numbers(source)
        if not normalized.strip():
            return ""

        tokens = Lexer().tokenize(normalized)
        lines = Parser().parse(tokens)
        line_map = {}
        for line in lines:
            line_map[line.number] = line
        program = [line_map[number] for number in sorted(line_map)]
        line_to_index = {line.number: idx for idx, line in enumerate(program)}

        pc = 0
        while pc < len(program):
            jump_target = self._execute_statement(program[pc].statement)
            if jump_target is None:
                pc += 1
                continue
            if jump_target not in line_to_index:
                raise ValueError(f"GOTO target line does not exist: {jump_target}")
            pc = line_to_index[jump_target]

        return "\n".join(self.output)

    def _ensure_line_numbers(self, source: str) -> str:
        raw_lines = source.splitlines()
        if not raw_lines:
            return ""

        def has_number_prefix(text: str) -> bool:
            stripped = text.lstrip()
            if not stripped:
                return False
            parts = stripped.split(maxsplit=1)
            return parts[0].isdigit()

        numbered_flags = [
            has_number_prefix(ln) for ln in raw_lines if ln.strip()
        ]
        if numbered_flags and any(numbered_flags) and not all(numbered_flags):
            raise ValueError("Mixed numbered and unnumbered lines are not allowed")

        if all((not ln.strip()) or has_number_prefix(ln) for ln in raw_lines):
            return source if source.endswith("\n") else f"{source}\n"

        numbered: list[str] = []
        line_no = 10
        for ln in raw_lines:
            if not ln.strip():
                continue
            numbered.append(f"{line_no} {ln}")
            line_no += 10
        return "\n".join(numbered) + "\n"

    def _execute_statement(self, statement: object) -> int | None:
        if isinstance(statement, LetStatement):
            self.variables[statement.name] = self._eval_expr(statement.expression)
            return None
        if isinstance(statement, PrintStatement):
            value = self._eval_expr(statement.expression)
            self.output.append(str(value))
            return None
        if isinstance(statement, GotoStatement):
            return statement.target
        if isinstance(statement, IfGotoStatement):
            left = self._eval_expr(statement.left)
            right = self._eval_expr(statement.right)
            op = statement.op
            if op == "=":
                condition = left == right
            elif op == "<":
                condition = left < right
            elif op == ">":
                condition = left > right
            else:
                raise ValueError(f"Unsupported IF operator: {op}")
            return statement.target if condition else None
        raise ValueError(f"Unsupported statement type: {type(statement).__name__}")

    def _eval_expr(self, expr: object) -> int | float | str:
        if isinstance(expr, NumberLiteral):
            return expr.value
        if isinstance(expr, StringLiteral):
            return expr.value
        if isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise ValueError(f"Undefined variable: {expr.name}")
            return self.variables[expr.name]
        if isinstance(expr, BinaryOp):
            left = self._eval_expr(expr.left)
            right = self._eval_expr(expr.right)
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise ValueError(f"Binary operator '{expr.op}' requires numeric operands")
            if expr.op == "+":
                return left + right
            if expr.op == "-":
                return left - right
            if expr.op == "*":
                return left * right
            if expr.op == "/":
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            raise ValueError(f"Unsupported operator: {expr.op}")
        raise ValueError(f"Unsupported expression type: {type(expr).__name__}")
