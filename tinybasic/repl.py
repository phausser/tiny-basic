"""Simple REPL entrypoint for Tiny BASIC."""

from tinybasic.interpreter import TinyBasicInterpreter


def main() -> None:
    interpreter = TinyBasicInterpreter()
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip().upper() in {"QUIT", "EXIT"}:
            break
        print(interpreter.run(line))


if __name__ == "__main__":
    main()
