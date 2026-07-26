import quiz
import scoring

QUESTIONS_PER_ROUND = 10


def show_menu():
    print("\n=== MATH CHALLENGE ===")
    print("1. Play")
    print("2. View High Scores")
    print("3. Quit")


def choose_difficulty():
    while True:
        choice = input("\nSelect difficulty (1=Easy, 2=Medium, 3=Hard): ")
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        print("Invalid choice. Try again.")


def play_round(difficulty):
    correct = 0
    for i in range(1, QUESTIONS_PER_ROUND + 1):
        question, answer = quiz.generate_question(difficulty)
        print(f"\nQ{i}: {question}")
        user_input = input("> ")
        if quiz.check_answer(user_input, answer):
            print("Correct!")
            correct += 1
        else:
            print(f"Wrong! The answer was {answer}")
    return correct


def main():
    scores = scoring.load_highscores()
    scoring.display_highscores(scores)

    while True:
        show_menu()
        choice = input("> ")

        if choice == "1":
            difficulty = choose_difficulty()
            score = play_round(difficulty)
            print(f"\nRound over! You scored {score}/{QUESTIONS_PER_ROUND} on {difficulty}!")

            if scoring.is_highscore(score, scores):
                name = input("New high score! Enter your name: ")
                scores = scoring.add_score(name, score, difficulty, scores)
                scoring.save_highscores(scores)
            else:
                print("Not a high score — try again!")

        elif choice == "2":
            scoring.display_highscores(scores)

        elif choice == "3":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()