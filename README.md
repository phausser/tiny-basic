# Tiny BASIC Interpreter

Dieses Repository enthaelt ein fruehes Grundgeruest fuer einen Tiny-BASIC-Interpreter in Python.

## Struktur

- `tinybasic/` - Quellcode (Lexer, Parser, AST, Interpreter, REPL)
- `tests/` - erste Smoke- und Feature-Tests

## Kurzspezifikation

### Unterstuetzte Befehle

- `PRINT <expr|string>`
  - Gibt den Wert eines Ausdrucks oder einen String aus.
- `LET <var> = <expr>`
  - Weist einer Variablen einen numerischen Wert zu.
- `INPUT <var>`
  - Liest eine Zahl von der Eingabe und speichert sie in `<var>`.
- `IF <expr> <relop> <expr> THEN <statement|GOTO <line>>`
  - Fuehrt den THEN-Teil nur bei wahrer Bedingung aus.
- `GOTO <line>`
  - Springt zu einer vorhandenen Zeilennummer.
- `END`
  - Beendet das Programm sofort.
- `REM <text>`
  - Kommentar; wird ignoriert.

### Ausdrucksregeln

- Numerische Operatoren: `+`, `-`, `*`, `/`
- Klammern: `(` und `)` zur expliziten Gruppierung
- Variablen: alphanumerische Bezeichner (typisch ein Buchstabe)
- Praezedenz: Klammern > `*`/`/` > `+`/`-`
- Auswertung erfolgt linksassoziativ innerhalb gleicher Praezedenz.

### Fehlerverhalten

- Syntaxfehler (ungueltige Tokens, unvollstaendige Anweisungen): Abbruch mit klarer Fehlermeldung inkl. Zeile.
- Laufzeitfehler (z. B. Division durch 0, Sprung auf unbekannte Zeile, uninitialisierte Variable): Abbruch mit klarer Fehlermeldung inkl. Zeile.
- `INPUT`-Fehler (keine gueltige Zahl): erneute Eingabeaufforderung oder Fehlerabbruch; initial bevorzugt Fehlerabbruch mit Meldung.
- Interpreter darf bei Fehlern nicht stillschweigend weitermachen.

## Tests ausfuehren

```bash
.venv/bin/pytest -q
```
