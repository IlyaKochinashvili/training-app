from dataclasses import dataclass

# Hypertrophy target rep range
REP_RANGE_LOW = 6
REP_RANGE_HIGH = 12

# Weight increments by exercise type (kg)
SMALL_INCREMENT = 2.5
LARGE_INCREMENT = 5.0

# RIR threshold: if avg RIR <= this after hitting top of range → increase weight
RIR_READY_THRESHOLD = 1


@dataclass
class SetData:
    weight: float
    reps: int
    rir: int
    is_failure: bool


@dataclass
class Recommendation:
    exercise_name: str
    target_weight: float
    rep_range_low: int
    rep_range_high: int
    trend: str  # "increase_weight" | "add_reps" | "maintain" | "deload"
    note: str


def epley_1rm(weight: float, reps: int) -> float:
    """Estimate 1RM using the Epley formula: 1RM = w * (1 + r/30)."""
    if reps == 1:
        return weight
    return weight * (1 + reps / 30)


def best_set(sets: list[SetData]) -> SetData:
    """Return the set with the highest estimated 1RM."""
    return max(sets, key=lambda s: epley_1rm(s.weight, s.reps))


def recommend_next(exercise_name: str, current_sets: list[SetData]) -> Recommendation:
    """
    Apply double progression logic to produce next-session recommendation.

    Phase 1 — add reps: if user hasn't hit REP_RANGE_HIGH with low RIR, keep weight.
    Phase 2 — add weight: once top of range is hit with RIR <= threshold, bump weight.
    """
    if not current_sets:
        return Recommendation(
            exercise_name=exercise_name,
            target_weight=0,
            rep_range_low=REP_RANGE_LOW,
            rep_range_high=REP_RANGE_HIGH,
            trend="maintain",
            note="Немає даних для аналізу",
        )

    top = best_set(current_sets)
    avg_rir = sum(s.rir for s in current_sets) / len(current_sets)
    hit_top_of_range = top.reps >= REP_RANGE_HIGH

    if hit_top_of_range and avg_rir <= RIR_READY_THRESHOLD:
        # Ready to add weight — choose increment based on exercise load
        increment = LARGE_INCREMENT if top.weight >= 60 else SMALL_INCREMENT
        new_weight = top.weight + increment
        return Recommendation(
            exercise_name=exercise_name,
            target_weight=new_weight,
            rep_range_low=REP_RANGE_LOW,
            rep_range_high=REP_RANGE_HIGH,
            trend="increase_weight",
            note=f"Збільши вагу: {top.weight} → {new_weight} кг",
        )

    if avg_rir >= 3 and not hit_top_of_range:
        # Too easy — suggest jumping weight faster
        increment = LARGE_INCREMENT if top.weight >= 60 else SMALL_INCREMENT
        new_weight = top.weight + increment
        return Recommendation(
            exercise_name=exercise_name,
            target_weight=new_weight,
            rep_range_low=REP_RANGE_LOW,
            rep_range_high=REP_RANGE_HIGH,
            trend="increase_weight",
            note=f"Занадто легко — збільши вагу: {top.weight} → {new_weight} кг",
        )

    if top.reps < REP_RANGE_LOW and avg_rir <= RIR_READY_THRESHOLD:
        # Weight too heavy for the range — deload slightly
        new_weight = round(top.weight * 0.9 / SMALL_INCREMENT) * SMALL_INCREMENT
        return Recommendation(
            exercise_name=exercise_name,
            target_weight=new_weight,
            rep_range_low=REP_RANGE_LOW,
            rep_range_high=REP_RANGE_HIGH,
            trend="deload",
            note=f"Знизь вагу до {new_weight} кг і пропрацюй діапазон {REP_RANGE_LOW}-{REP_RANGE_HIGH} повторів",
        )

    # Default: keep weight, aim for more reps
    target_reps_low = min(top.reps + 1, REP_RANGE_HIGH)
    return Recommendation(
        exercise_name=exercise_name,
        target_weight=top.weight,
        rep_range_low=target_reps_low,
        rep_range_high=REP_RANGE_HIGH,
        trend="add_reps",
        note=f"Тримай {top.weight} кг, цілься на {target_reps_low}-{REP_RANGE_HIGH} повторів",
    )


def format_recommendation(rec: Recommendation) -> str:
    trend_icon = {
        "increase_weight": "📈",
        "add_reps": "🔄",
        "maintain": "➡️",
        "deload": "📉",
    }.get(rec.trend, "➡️")

    return (
        f"{trend_icon} <b>{rec.exercise_name}</b>\n"
        f"   {rec.note}\n"
        f"   Ціль: {rec.target_weight} кг × {rec.rep_range_low}-{rec.rep_range_high} повт."
    )
