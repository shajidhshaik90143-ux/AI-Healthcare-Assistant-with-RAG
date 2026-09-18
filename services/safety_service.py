EMERGENCY_TERMS = [

    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "severe difficulty breathing",

    "chest pain",
    "severe chest pain",

    "heart attack",

    "unconscious",
    "passed out",
    "loss of consciousness",

    "severe bleeding",
    "uncontrolled bleeding",

    "stroke symptoms",
    "face drooping",
    "slurred speech",

    "seizure",

    "suicide attempt",
    "overdose",

    "poisoning",

    "severe allergic reaction",
    "anaphylaxis"
]


def check_emergency(text):

    normalized = text.lower()

    for term in EMERGENCY_TERMS:

        if term in normalized:
            return True

    return False