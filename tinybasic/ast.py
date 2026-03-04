"""AST node definitions for Tiny BASIC."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NumberLiteral:
    value: int


@dataclass(frozen=True)
class StringLiteral:
    value: str


@dataclass(frozen=True)
class Variable:
    name: str


@dataclass(frozen=True)
class BinaryOp:
    op: str
    left: object
    right: object


@dataclass(frozen=True)
class LetStatement:
    name: str
    expression: object


@dataclass(frozen=True)
class PrintStatement:
    expression: object


@dataclass(frozen=True)
class GotoStatement:
    target: int


@dataclass(frozen=True)
class IfGotoStatement:
    left: object
    op: str
    right: object
    target: int


@dataclass(frozen=True)
class EndStatement:
    pass


@dataclass(frozen=True)
class Line:
    number: int
    statement: object
