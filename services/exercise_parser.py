from dataclasses import dataclass, field

FAILURE_TOKENS = {"відказ", "відмова", "до відмови", "failure", "fail", "0"}

MIN_WEIGHT = 0.25
MAX_WEIGHT = 500.0
MIN_REPS = 1
MAX_REPS = 30
MIN_SETS = 1
MAX_SETS = 10


class ParseError(Exception):
    pass


@dataclass
class ParsedSet:
    weight: float
    reps: int
    is_failure: bool = False
    rir: int = 2


@dataclass
class ParsedExerciseInput:
    exercise_name: str
    sets: list[ParsedSet] = field(default_factory=list)


def _parse_set_line(line: str, line_num: int) -> ParsedSet:
    parts = line.strip().split()

    if len(parts) < 2:
        raise ParseError(f"Рядок {line_num}: очікується «вага повтори», отримано «{line}»")

    try:
        weight = float(parts[0].replace(",", "."))
    except ValueError as err:
        raise ParseError(f"Рядок {line_num}: «{parts[0]}» — не число для ваги") from err

    try:
        reps = int(parts[1])
    except ValueError as err:
        raise ParseError(f"Рядок {line_num}: «{parts[1]}» — не ціле число для повторів") from err

    if not (MIN_WEIGHT <= weight <= MAX_WEIGHT):
        raise ParseError(f"Рядок {line_num}: вага {weight} кг поза допустимим діапазоном ({MIN_WEIGHT}–{MAX_WEIGHT})")

    if not (MIN_REPS <= reps <= MAX_REPS):
        raise ParseError(f"Рядок {line_num}: повтори {reps} поза діапазоном ({MIN_REPS}–{MAX_REPS})")

    suffix = " ".join(parts[2:]).lower() if len(parts) > 2 else ""
    is_failure = suffix in FAILURE_TOKENS
    rir = 0 if is_failure else 2

    return ParsedSet(weight=weight, reps=reps, is_failure=is_failure, rir=rir)


def parse_exercise_input(text: str) -> ParsedExerciseInput:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if not lines:
        raise ParseError("Повідомлення порожнє")

    exercise_name = lines[0]

    if len(exercise_name) < 2:
        raise ParseError("Назва вправи занадто коротка")

    set_lines = lines[1:]

    if len(set_lines) < MIN_SETS:
        raise ParseError("Додай хоча б один підхід: «вага повтори»")

    if len(set_lines) > MAX_SETS:
        raise ParseError(f"Максимум {MAX_SETS} підходів за раз")

    sets = [_parse_set_line(line, i + 2) for i, line in enumerate(set_lines)]

    return ParsedExerciseInput(exercise_name=exercise_name, sets=sets)
