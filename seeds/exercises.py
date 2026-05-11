from models.exercise import MuscleGroup
from models.exercise_alias import Language

# (canonical_uk, muscle_group, [(alias, language), ...])
EXERCISES: list[tuple[str, MuscleGroup, list[tuple[str, Language]]]] = [
    # ── CHEST ────────────────────────────────────────────────────────────────
    (
        "Жим лежачи",
        MuscleGroup.chest,
        [
            ("жим", Language.uk),
            ("жим лежа", Language.uk),
            ("bench press", Language.en),
            ("bench", Language.en),
            ("flat bench", Language.en),
        ],
    ),
    (
        "Жим лежачи на похилій лаві",
        MuscleGroup.chest,
        [
            ("жим на похилій", Language.uk),
            ("похила лава", Language.uk),
            ("incline bench press", Language.en),
            ("incline bench", Language.en),
        ],
    ),
    (
        "Жим лежачи на зворотній похилій лаві",
        MuscleGroup.chest,
        [
            ("жим на зворотній", Language.uk),
            ("decline bench press", Language.en),
            ("decline bench", Language.en),
        ],
    ),
    (
        "Жим гантелей лежачи",
        MuscleGroup.chest,
        [
            ("жим гантелей", Language.uk),
            ("dumbbell bench press", Language.en),
            ("db bench", Language.en),
        ],
    ),
    (
        "Розведення гантелей лежачи",
        MuscleGroup.chest,
        [
            ("розведення", Language.uk),
            ("дефлексія", Language.uk),
            ("dumbbell flyes", Language.en),
            ("chest flyes", Language.en),
            ("flyes", Language.en),
        ],
    ),
    (
        "Кросовер у блоці",
        MuscleGroup.chest,
        [
            ("кросовер", Language.uk),
            ("cable crossover", Language.en),
            ("crossover", Language.en),
        ],
    ),
    (
        "Жим у тренажері для грудей",
        MuscleGroup.chest,
        [
            ("тренажер груди", Language.uk),
            ("chest press machine", Language.en),
            ("machine chest press", Language.en),
        ],
    ),
    (
        "Віджимання на брусах",
        MuscleGroup.chest,
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
        [
            ("pull-up", Language.en),
            ("pullup", Language.en),
            ("chin-up", Language.en),
        ],
    ),
    (
        "Тяга штанги в нахилі",
        MuscleGroup.back,
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
        [
            ("т-тяга", Language.uk),
            ("t-bar row", Language.en),
            ("t bar row", Language.en),
        ],
    ),
    (
        "Тяга блоку до обличчя",
        MuscleGroup.back,
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
        [
            ("жим ногами", Language.uk),
            ("leg press", Language.en),
        ],
    ),
    (
        "Розгинання ніг у тренажері",
        MuscleGroup.legs,
        [
            ("розгинання ніг", Language.uk),
            ("leg extension", Language.en),
            ("leg extensions", Language.en),
        ],
    ),
    (
        "Згинання ніг лежачи",
        MuscleGroup.legs,
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
        [
            ("дедліфт", Language.uk),
            ("deadlift", Language.en),
            ("dl", Language.en),
        ],
    ),
    (
        "Випади",
        MuscleGroup.legs,
        [
            ("lunges", Language.en),
            ("walking lunges", Language.en),
        ],
    ),
    (
        "Підйом на носки стоячи",
        MuscleGroup.legs,
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
        [
            ("підйом перед собою", Language.uk),
            ("front raise", Language.en),
            ("front raises", Language.en),
        ],
    ),
    (
        "Тяга штанги до підборіддя",
        MuscleGroup.shoulders,
        [
            ("тяга до підборіддя", Language.uk),
            ("upright row", Language.en),
        ],
    ),
    # ── ARMS ─────────────────────────────────────────────────────────────────
    (
        "Підйом штанги на біцепс",
        MuscleGroup.arms,
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
        [
            ("бруси трицепс", Language.uk),
            ("tricep dips", Language.en),
        ],
    ),
    # ── CORE ─────────────────────────────────────────────────────────────────
    (
        "Планка",
        MuscleGroup.core,
        [
            ("plank", Language.en),
        ],
    ),
    (
        "Скручування",
        MuscleGroup.core,
        [
            ("crunch", Language.en),
            ("crunches", Language.en),
            ("abs crunch", Language.en),
        ],
    ),
    (
        "Підйом ніг лежачи",
        MuscleGroup.core,
        [
            ("підйом ніг", Language.uk),
            ("leg raise", Language.en),
            ("lying leg raise", Language.en),
        ],
    ),
]
