from services.progression import Recommendation, SetData, epley_1rm, recommend_next


def test_epley_single_rep():
    assert epley_1rm(100, 1) == 100.0


def test_epley_increases_with_reps():
    assert epley_1rm(100, 10) > epley_1rm(100, 5)


def test_recommend_add_reps_when_not_at_top():
    sets = [SetData(weight=80, reps=8, rir=2, is_failure=False)]
    rec = recommend_next("Жим лежачи", sets)
    assert rec.trend == "add_reps"
    assert rec.target_weight == 80


def test_recommend_increase_weight_at_top_with_low_rir():
    sets = [SetData(weight=80, reps=12, rir=1, is_failure=False)]
    rec = recommend_next("Жим лежачи", sets)
    assert rec.trend == "increase_weight"
    assert rec.target_weight > 80


def test_recommend_increase_weight_when_too_easy():
    sets = [SetData(weight=80, reps=8, rir=4, is_failure=False)]
    rec = recommend_next("Жим лежачи", sets)
    assert rec.trend == "increase_weight"


def test_recommend_deload_when_too_heavy():
    sets = [SetData(weight=120, reps=4, rir=0, is_failure=True)]
    rec = recommend_next("Присідання", sets)
    assert rec.trend == "deload"
    assert rec.target_weight < 120


def test_recommend_empty_sets_returns_maintain():
    rec = recommend_next("Squat", [])
    assert rec.trend == "maintain"
    assert rec.target_weight == 0


def test_increment_large_for_heavy_weight():
    sets = [SetData(weight=100, reps=12, rir=1, is_failure=False)]
    rec = recommend_next("Deadlift", sets)
    assert rec.target_weight == 105.0


def test_increment_small_for_light_weight():
    sets = [SetData(weight=30, reps=12, rir=1, is_failure=False)]
    rec = recommend_next("Lateral raise", sets)
    assert rec.target_weight == 32.5


def test_recommendation_is_dataclass():
    sets = [SetData(weight=60, reps=10, rir=2, is_failure=False)]
    rec = recommend_next("Bench", sets)
    assert isinstance(rec, Recommendation)
    assert rec.exercise_name == "Bench"
