import pytest

from services.exercise_parser import ParsedExerciseInput, ParsedSet, ParseError, parse_exercise_input


def test_basic_single_set():
    result = parse_exercise_input("Bench Press\n100 8")
    assert isinstance(result, ParsedExerciseInput)
    assert result.exercise_name == "Bench Press"
    assert len(result.sets) == 1
    assert result.sets[0] == ParsedSet(weight=100.0, reps=8)


def test_multiple_sets():
    result = parse_exercise_input("Жим лежачи\n100 8\n100 8\n95 6")
    assert len(result.sets) == 3
    assert result.sets[2].weight == 95.0
    assert result.sets[2].reps == 6


def test_failure_flag_uk():
    result = parse_exercise_input("Підтягування\n80 6 відказ")
    assert result.sets[0].is_failure is True
    assert result.sets[0].rir == 0


def test_failure_flag_en():
    result = parse_exercise_input("Pull-up\n80 6 failure")
    assert result.sets[0].is_failure is True


def test_comma_decimal_weight():
    result = parse_exercise_input("Squat\n102,5 5")
    assert result.sets[0].weight == 102.5


def test_missing_sets_raises():
    with pytest.raises(ParseError, match="хоча б один підхід"):
        parse_exercise_input("Bench Press")


def test_empty_input_raises():
    with pytest.raises(ParseError, match="порожнє"):
        parse_exercise_input("")


def test_too_many_sets_raises():
    sets = "\n".join(["100 8"] * 11)
    with pytest.raises(ParseError, match="Максимум"):
        parse_exercise_input(f"Squat\n{sets}")


def test_invalid_weight_raises():
    with pytest.raises(ParseError, match="не число"):
        parse_exercise_input("Squat\nabc 8")


def test_invalid_reps_raises():
    with pytest.raises(ParseError, match="не ціле число"):
        parse_exercise_input("Squat\n100 abc")


def test_weight_out_of_range_raises():
    with pytest.raises(ParseError, match="поза допустимим діапазоном"):
        parse_exercise_input("Squat\n600 5")


def test_reps_out_of_range_raises():
    with pytest.raises(ParseError, match="поза діапазоном"):
        parse_exercise_input("Squat\n100 50")


def test_exercise_name_too_short_raises():
    with pytest.raises(ParseError, match="коротка"):
        parse_exercise_input("A\n100 8")


def test_non_failure_set_has_default_rir():
    result = parse_exercise_input("Squat\n100 8")
    assert result.sets[0].rir == 2
    assert result.sets[0].is_failure is False
