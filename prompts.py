LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Hindi",
    "Japanese",
    "Mandarin"
]


def build_personality_prompt(personality_name, personality_description, personality_behavior, language, message):
    return (
        f"System Directive:\n"
        f"You are acting as the persona described below. Your response must stay in-character, follow the specified style and guidelines, and be written in the specified language.\n\n"
        f"--- Persona Profile ---\n"
        f"Name: {personality_name}\n"
        f"Description: {personality_description}\n"
        f"Behavior Guidelines: {personality_behavior}\n"
        f"Response Language: {language}\n\n"
        f"--- User Message ---\n"
        f"{message}"
    )
