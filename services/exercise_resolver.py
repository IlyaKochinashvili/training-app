from dataclasses import dataclass

from rapidfuzz import fuzz, process

# Minimum score to consider a match valid
EXACT_THRESHOLD = 100
FUZZY_THRESHOLD = 75

# Trash input that should never be saved
TRASH_NAMES = {
    "вправа",
    "exercise",
    "підхід",
    "set",
    "тренування",
    "workout",
    "ааа",
    "тест",
    "test",
    "123",
    "???",
}


@dataclass
class ResolveResult:
    canonical_name: str
    score: float
    is_exact: bool


def _normalize(text: str) -> str:
    return text.strip().lower()


def is_trash(name: str) -> bool:
    return _normalize(name) in TRASH_NAMES or len(name.strip()) < 3


def resolve_exercise(
    raw_input: str,
    candidates: list[tuple[str, list[str]]],
) -> ResolveResult | None:
    """
    Find the best matching canonical exercise name.

    candidates: list of (canonical_name, [alias1, alias2, ...])
    Returns None when confidence is below threshold.
    """
    if is_trash(raw_input):
        return None

    normalized_input = _normalize(raw_input)

    # Build flat lookup: normalized alias -> canonical name
    alias_map: dict[str, str] = {}
    for canonical, aliases in candidates:
        alias_map[_normalize(canonical)] = canonical
        for alias in aliases:
            alias_map[_normalize(alias)] = canonical

    # Exact match first
    if normalized_input in alias_map:
        return ResolveResult(
            canonical_name=alias_map[normalized_input],
            score=100.0,
            is_exact=True,
        )

    # Fuzzy match against all known aliases
    all_aliases = list(alias_map.keys())
    match = process.extractOne(
        normalized_input,
        all_aliases,
        scorer=fuzz.WRatio,
        score_cutoff=FUZZY_THRESHOLD,
    )

    if match is None:
        return None

    matched_alias, score, _ = match
    return ResolveResult(
        canonical_name=alias_map[matched_alias],
        score=score,
        is_exact=False,
    )
