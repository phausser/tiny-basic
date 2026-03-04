import pytest

from tinybasic import TinyBasicInterpreter


def test_undefined_variable_raises_clear_error():
    interpreter = TinyBasicInterpreter()
    with pytest.raises(ValueError, match="Undefined variable"):
        interpreter.run("PRINT A")


def test_mixed_numbered_and_unnumbered_lines_raise_error():
    interpreter = TinyBasicInterpreter()
    program = "\n".join(["10 PRINT \"A\"", 'PRINT "B"'])
    with pytest.raises(ValueError, match="Mixed numbered and unnumbered lines"):
        interpreter.run(program)


def test_division_by_zero_raises_error():
    interpreter = TinyBasicInterpreter()
    with pytest.raises(ValueError, match="Division by zero"):
        interpreter.run("LET A = 1 / 0\nPRINT A")


def test_goto_statement_jumps_to_target_line():
    interpreter = TinyBasicInterpreter()
    program = "\n".join(["10 GOTO 30", '20 PRINT "NO"', '30 PRINT "YES"'])
    assert interpreter.run(program) == "YES"


def test_duplicate_line_number_uses_last_definition():
    interpreter = TinyBasicInterpreter()
    program = "\n".join(['10 PRINT "OLD"', '10 PRINT "NEW"'])
    assert interpreter.run(program) == "NEW"
