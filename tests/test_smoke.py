from tinybasic import TinyBasicInterpreter


def test_interpreter_can_run_print_statement_smoke():
    interpreter = TinyBasicInterpreter()
    output = interpreter.run('PRINT "HELLO"')
    assert output == "HELLO"


def test_interpreter_accepts_empty_program_smoke():
    interpreter = TinyBasicInterpreter()
    output = interpreter.run("")
    assert output == ""
