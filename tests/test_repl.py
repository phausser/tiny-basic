from tinybasic import repl


def test_repl_store_list_and_run_program(monkeypatch, capsys):
    inputs = iter([
        '10 PRINT "HELLO"',
        "LIST",
        "RUN",
        "QUIT",
    ])

    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))

    repl.main()

    out = capsys.readouterr().out
    assert '10 PRINT "HELLO"' in out
    assert "HELLO" in out
