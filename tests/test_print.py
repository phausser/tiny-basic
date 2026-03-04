from tinybasic import TinyBasicInterpreter


def test_print_statement_outputs_text():
    interpreter = TinyBasicInterpreter()
    assert interpreter.run('PRINT "HI"') == "HI"
