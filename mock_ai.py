import random

def generate_mock_response(user_input: str) -> str:
    responses = [
        "Bunu daha önce de sormuştun.",
        "Harika bir soru!",
        "Bu konuda emin değilim ama araştırabilirim.",
        "Bunu bir düşünelim...",
        f"'{user_input}' hakkında bildiklerimi aktarıyorum..."
    ]
    return random.choice(responses)