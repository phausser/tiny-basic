from tinybasic import TinyBasicInterpreter


def test_if_goto_jumps_to_target_line():
    program = "\n".join(
        [
            "10 LET A = 1",
            "20 IF A = 1 THEN GOTO 40",
            '30 PRINT "NO"',
            '40 PRINT "YES"',
        ]
    )
    interpreter = TinyBasicInterpreter()
    assert interpreter.run(program) == "YES"
