import random

def unknown_string():
    unknown_list = [
        "I don't understand what you're saying",
        "Do you mind rephrasing that?",
        "I'm sorry, I didn't quite catch that",
        "Please try something else"
    ]
    return unknown_list[random.randrange(0, len(unknown_list))]