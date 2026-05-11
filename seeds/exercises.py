from models.exercise import MuscleGroup
from models.exercise_alias import Language

# (canonical_uk, muscle_group, has_angle_variant, [(alias, language), ...])
EXERCISES: list[tuple[str, MuscleGroup, bool, list[tuple[str, Language]]]] = [
    # ── CHEST ────────────────────────────────────────────────────────────────
    (
        "Жим лежачи",
        MuscleGroup.chest,
        False,
        [
            ("жим", Language.uk),
            ("жим лежа", Language.uk),
            ("bench press", Language.en),
            ("bench", Language.en),
            ("flat bench", Language.en),
        ],
    ),
    (
        "Жим штанги на похилій лаві",
        MuscleGroup.chest,
        True,
        [
            ("жим на похилій", Language.uk),
            ("похила лава штанга", Language.uk),
            ("incline bench press", Language.en),
            ("incline bench", Language.en),
        ],
    ),
    (
        "Жим штанги на зворотній похилій лаві",
        MuscleGroup.chest,
        False,
        [
            ("жим на зворотній", Language.uk),
            ("decline bench press", Language.en),
            ("decline bench", Language.en),
        ],
    ),
    (
        "Жим гантелей лежачи",
        MuscleGroup.chest,
        False,
        [
            ("жим гантелей плоско", Language.uk),
            ("dumbbell bench press", Language.en),
            ("db bench", Language.en),
            ("flat db press", Language.en),
        ],
    ),
    (
        "Жим гантелей на похилій лаві",
        MuscleGroup.chest,
        True,
        [
            ("жим гантелей похила", Language.uk),
            ("похила лава гантелі", Language.uk),
            ("incline dumbbell press", Language.en),
            ("incline db press", Language.en),
        ],
    ),
    (
        "Розведення гантелей лежачи",
        MuscleGroup.chest,
        False,
        [
            ("розведення", Language.uk),
            ("дефлексія", Language.uk),
            ("dumbbell flyes", Language.en),
            ("chest flyes", Language.en),
            ("flyes", Language.en),
        ],
    ),
    (
        "Розведення гантелей на похилій лаві",
        MuscleGroup.chest,
        True,
        [
            ("розведення похила", Language.uk),
            ("incline flyes", Language.en),
            ("incline dumbbell flyes", Language.en),
        ],
    ),
    (
        "Кросовер у блоці",
        MuscleGroup.chest,
        False,
        [
            ("кросовер", Language.uk),
            ("cable crossover", Language.en),
            ("crossover", Language.en),
        ],
    ),
    (
        "Жим у тренажері для грудей",
        MuscleGroup.chest,
        False,
        [
            ("тренажер груди", Language.uk),
            ("chest press machine", Language.en),
            ("machine chest press", Language.en),
        ],
    ),
    (
        "Віджимання на брусах",
        MuscleGroup.chest,
        False,
        [
            ("бруси", Language.uk),
            ("dips", Language.en),
            ("chest dips", Language.en),
        ],
    ),
    # ── BACK ─────────────────────────────────────────────────────────────────
    (
        "Підтягування",
        MuscleGroup.back,
        False,
        [
            ("pull-up", Language.en),
            ("pullup", Language.en),
            ("chin-up", Language.en),
        ],
    ),
    (
        "Тяга штанги в нахилі",
        MuscleGroup.back,
        False,
        [
            ("тяга в нахилі", Language.uk),
            ("тяга штанги", Language.uk),
            ("barbell row", Language.en),
            ("bent over row", Language.en),
            ("bb row", Language.en),
        ],
    ),
    (
        "Тяга гантелі в нахилі",
        MuscleGroup.back,
        False,
        [
            ("тяга гантелі", Language.uk),
            ("dumbbell row", Language.en),
            ("db row", Language.en),
            ("one arm row", Language.en),
        ],
    ),
    (
        "Вертикальна тяга у блоці",
        MuscleGroup.back,
        False,
        [
            ("тяга зверху", Language.uk),
            ("тяга у тренажері зверху", Language.uk),
            ("тяга блоку зверху", Language.uk),
            ("lat pulldown", Language.en),
            ("pulldown", Language.en),
        ],
    ),
    (
        "Горизонтальна тяга у блоці",
        MuscleGroup.back,
        False,
        [
            ("тяга до пояса", Language.uk),
            ("тяга знизу", Language.uk),
            ("seated cable row", Language.en),
            ("cable row", Language.en),
            ("low row", Language.en),
        ],
    ),
    (
        "Тяга Т-грифа",
        MuscleGroup.back,
        False,
        [
            ("т-тяга", Language.uk),
            ("t-bar row", Language.en),
            ("t bar row", Language.en),
        ],
    ),
    (
        "Тяга блоку до обличчя",
        MuscleGroup.back,
        False,
        [
            ("тяга до обличчя", Language.uk),
            ("face pull", Language.en),
            ("face pulls", Language.en),
        ],
    ),
    # ── LEGS ─────────────────────────────────────────────────────────────────
    (
        "Присідання зі штангою",
        MuscleGroup.legs,
        False,
        [
            ("присідання", Language.uk),
            ("squat", Language.en),
            ("back squat", Language.en),
            ("barbell squat", Language.en),
        ],
    ),
    (
        "Жим ногами",
        MuscleGroup.legs,
        False,
        [
            ("жим ногами", Language.uk),
            ("leg press", Language.en),
        ],
    ),
    (
        "Розгинання ніг у тренажері",
        MuscleGroup.legs,
        False,
        [
            ("розгинання ніг", Language.uk),
            ("leg extension", Language.en),
            ("leg extensions", Language.en),
        ],
    ),
    (
        "Згинання ніг лежачи",
        MuscleGroup.legs,
        False,
        [
            ("згинання ніг", Language.uk),
            ("лежачи згинання", Language.uk),
            ("lying leg curl", Language.en),
            ("leg curl", Language.en),
        ],
    ),
    (
        "Румунська тяга",
        MuscleGroup.legs,
        False,
        [
            ("румунська", Language.uk),
            ("ртяга", Language.uk),
            ("romanian deadlift", Language.en),
            ("rdl", Language.en),
        ],
    ),
    (
        "Мертва тяга",
        MuscleGroup.legs,
        False,
        [
            ("дедліфт", Language.uk),
            ("deadlift", Language.en),
            ("dl", Language.en),
        ],
    ),
    (
        "Випади",
        MuscleGroup.legs,
        False,
        [
            ("lunges", Language.en),
            ("walking lunges", Language.en),
        ],
    ),
    (
        "Підйом на носки стоячи",
        MuscleGroup.legs,
        False,
        [
            ("підйом на носки", Language.uk),
            ("литки стоячи", Language.uk),
            ("standing calf raise", Language.en),
            ("calf raise", Language.en),
        ],
    ),
    # ── SHOULDERS ────────────────────────────────────────────────────────────
    (
        "Жим штанги стоячи",
        MuscleGroup.shoulders,
        False,
        [
            ("армійський жим", Language.uk),
            ("overhead press", Language.en),
            ("ohp", Language.en),
            ("military press", Language.en),
            ("shoulder press", Language.en),
        ],
    ),
    (
        "Жим гантелей сидячи",
        MuscleGroup.shoulders,
        False,
        [
            ("жим гантелей на плечі", Language.uk),
            ("dumbbell shoulder press", Language.en),
            ("db shoulder press", Language.en),
            ("seated db press", Language.en),
        ],
    ),
    (
        "Підйом гантелей через сторони",
        MuscleGroup.shoulders,
        False,
        [
            ("махи в сторони", Language.uk),
            ("махи", Language.uk),
            ("lateral raise", Language.en),
            ("lateral raises", Language.en),
            ("side raise", Language.en),
        ],
    ),
    (
        "Підйом гантелей перед собою",
        MuscleGroup.shoulders,
        False,
        [
            ("підйом перед собою", Language.uk),
            ("front raise", Language.en),
            ("front raises", Language.en),
        ],
    ),
    (
        "Тяга штанги до підборіддя",
        MuscleGroup.shoulders,
        False,
        [
            ("тяга до підборіддя", Language.uk),
            ("upright row", Language.en),
        ],
    ),
    # ── ARMS ─────────────────────────────────────────────────────────────────
    (
        "Підйом штанги на біцепс",
        MuscleGroup.arms,
        False,
        [
            ("підйом на біцепс", Language.uk),
            ("barbell curl", Language.en),
            ("bb curl", Language.en),
            ("bicep curl", Language.en),
        ],
    ),
    (
        "Підйом гантелей на біцепс",
        MuscleGroup.arms,
        False,
        [
            ("гантелі на біцепс", Language.uk),
            ("dumbbell curl", Language.en),
            ("db curl", Language.en),
            ("hammer curl", Language.en),
        ],
    ),
    (
        "Французький жим",
        MuscleGroup.arms,
        False,
        [
            ("французький", Language.uk),
            ("skull crusher", Language.en),
            ("skull crushers", Language.en),
            ("lying tricep extension", Language.en),
        ],
    ),
    (
        "Розгинання рук у блоці",
        MuscleGroup.arms,
        False,
        [
            ("розгинання трицепс", Language.uk),
            ("трицепс блок", Language.uk),
            ("cable pushdown", Language.en),
            ("tricep pushdown", Language.en),
            ("pushdown", Language.en),
        ],
    ),
    (
        "Віджимання на брусах для трицепса",
        MuscleGroup.arms,
        False,
        [
            ("бруси трицепс", Language.uk),
            ("tricep dips", Language.en),
        ],
    ),
    # ── CORE ─────────────────────────────────────────────────────────────────
    (
        "Планка",
        MuscleGroup.core,
        False,
        [
            ("plank", Language.en),
        ],
    ),
    (
        "Скручування",
        MuscleGroup.core,
        False,
        [
            ("crunch", Language.en),
            ("crunches", Language.en),
            ("abs crunch", Language.en),
        ],
    ),
    (
        "Підйом ніг лежачи",
        MuscleGroup.core,
        False,
        [
            ("підйом ніг", Language.uk),
            ("leg raise", Language.en),
            ("lying leg raise", Language.en),
        ],
    ),
]
