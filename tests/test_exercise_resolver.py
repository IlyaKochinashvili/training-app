from services.exercise_resolver import ResolveResult, is_trash, resolve_exercise

CANDIDATES = [
    ("Жим лежачи", ["жим", "bench press", "bench", "flat bench"]),
    ("Вертикальна тяга у блоці", ["тяга зверху", "тяга блоку зверху", "lat pulldown", "pulldown"]),
    ("Присідання зі штангою", ["присідання", "squat", "back squat"]),
]


def test_exact_canonical_match():
    result = resolve_exercise("Жим лежачи", CANDIDATES)
    assert result is not None
    assert result.canonical_name == "Жим лежачи"
    assert result.is_exact is True
    assert result.score == 100.0


def test_exact_alias_match():
    result = resolve_exercise("bench press", CANDIDATES)
    assert result is not None
    assert result.canonical_name == "Жим лежачи"
    assert result.is_exact is True


def test_fuzzy_match_typo():
    result = resolve_exercise("жим лижачи", CANDIDATES)
    assert result is not None
    assert result.canonical_name == "Жим лежачи"
    assert result.is_exact is False


def test_fuzzy_alias_match():
    result = resolve_exercise("тяга сверху", CANDIDATES)
    assert result is not None
    assert result.canonical_name == "Вертикальна тяга у блоці"


def test_case_insensitive_match():
    result = resolve_exercise("BENCH PRESS", CANDIDATES)
    assert result is not None
    assert result.canonical_name == "Жим лежачи"


def test_no_match_returns_none():
    result = resolve_exercise("хурдурмурдур", CANDIDATES)
    assert result is None


def test_trash_name_returns_none():
    result = resolve_exercise("вправа", CANDIDATES)
    assert result is None


def test_too_short_returns_none():
    result = resolve_exercise("ab", CANDIDATES)
    assert result is None


def test_is_trash_known_tokens():
    assert is_trash("вправа") is True
    assert is_trash("test") is True
    assert is_trash("тест") is True


def test_is_trash_short_string():
    assert is_trash("аа") is True
    assert is_trash("ab") is True


def test_is_not_trash_valid_name():
    assert is_trash("Жим лежачи") is False
    assert is_trash("bench press") is False


def test_resolve_returns_result_dataclass():
    result = resolve_exercise("squat", CANDIDATES)
    assert isinstance(result, ResolveResult)
    assert result.canonical_name == "Присідання зі штангою"
