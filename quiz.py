import random

def generate_question(difficulty):
    if difficulty == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif difficulty == "medium":
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        op = random.choice(["+", "-", "*"])
    else:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(["+", "-", "*", "/"])
        if op == "/":
            a = a * b
            b = b or 1
            return f"{a} / {b} = ?", a // b

    if op == "+":
        answer = a + b
    elif op == "-":
        answer = a - b
    else:
        answer = a * b

    return f"{a} {op} {b} = ?", answer


def check_answer(user_input, correct_answer):
    try:
        return int(user_input) == correct_answer
    except ValueError:
        return False