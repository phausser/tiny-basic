"""Simple REPL entrypoint for Tiny BASIC."""

from tinybasic.interpreter import TinyBasicInterpreter


def _parse_numbered_line(line: str) -> tuple[int, str] | None:
    stripped = line.strip()
    if not stripped:
        return None
    parts = stripped.split(maxsplit=1)
    if not parts[0].isdigit():
        return None
    line_no = int(parts[0])
    statement = parts[1] if len(parts) > 1 else ""
    return line_no, statement


def _build_program_source(program: dict[int, str]) -> str:
    lines = []
    for number in sorted(program):
        statement = program[number].strip()
        if statement:
            lines.append(f"{number} {statement}")
    return "\n".join(lines)


def main() -> None:
    interpreter = TinyBasicInterpreter()
    program: dict[int, str] = {}

    while True:
        try:
            line = input("> ")
        except EOFError:
            break

        stripped = line.strip()
        if not stripped:
            continue

        command = stripped.upper()
        if command == "QUIT":
            break
        if command == "NEW":
            program.clear()
            continue
        if command == "LIST":
            for number in sorted(program):
                statement = program[number].strip()
                if statement:
                    print(f"{number} {statement}")
            continue
        if command == "RUN":
            source = _build_program_source(program)
            try:
                output = interpreter.run(source)
            except ValueError as exc:
                print(f"ERROR: {exc}")
                continue
            if output:
                print(output)
            continue

        numbered = _parse_numbered_line(line)
        if numbered is not None:
            line_no, statement = numbered
            if statement.strip():
                program[line_no] = statement
            elif line_no in program:
                del program[line_no]
            continue

        try:
            output = interpreter.run(line)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            continue
        if output:
            print(output)


if __name__ == "__main__":
    main()
