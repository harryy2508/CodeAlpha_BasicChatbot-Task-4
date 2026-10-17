import ast
import operator
import random
from datetime import datetime
from pathlib import Path


BOT_NAME = "Nova"
HISTORY_FILE = Path(__file__).with_name("chat_history.txt")

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the programmer quit his job? Because he didn't get arrays!",
    "Why was the computer cold? It left its Windows open!",
    "What do programmers do when they are hungry? They grab a byte!",
    "Why do Python programmers wear glasses? Because they cannot C!"
]

QUIZ_QUESTIONS = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["A. function", "B. def", "C. define", "D. fun"],
        "answer": "B"
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["A. int", "B. str", "C. bool", "D. list"],
        "answer": "C"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["A. //", "B. <!--", "C. #", "D. **"],
        "answer": "C"
    },
    {
        "question": "Which method adds an item to the end of a list?",
        "options": ["A. add()", "B. append()", "C. insert_end()", "D. push()"],
        "answer": "B"
    },
    {
        "question": "Which loop runs while a condition remains true?",
        "options": ["A. if", "B. for", "C. while", "D. switch"],
        "answer": "C"
    }
]

KNOWLEDGE = {
    "python": "Python is a high-level programming language known for its readable syntax.",
    "html": "HTML defines the structure of web pages.",
    "css": "CSS controls the appearance and layout of web pages.",
    "javascript": "JavaScript adds interactive behavior to websites.",
    "database": "A database stores and organizes information for efficient retrieval.",
    "algorithm": "An algorithm is a sequence of steps used to solve a problem.",
    "artificial intelligence": "Artificial intelligence enables machines to perform tasks that typically require human intelligence.",
    "machine learning": "Machine learning uses data to train systems to identify patterns and make predictions.",
    "cybersecurity": "Cybersecurity protects computers, networks, and data from digital threats.",
    "programming": "Programming is the process of writing instructions that computers can execute."
}


def display_banner():
    print("\n" + "=" * 58)
    print("                 NOVA SMART CHATBOT")
    print("=" * 58)
    print("Your interactive Python conversation assistant")
    print("Type /help to explore commands.")
    print("Type /quit to end the conversation.")
    print("=" * 58)


def save_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {sender}: {message}\n")
    except OSError:
        print("Warning: Chat history could not be saved.")


def show_history():
    if not HISTORY_FILE.exists():
        print(f"{BOT_NAME}: No saved conversations were found.")
        return

    try:
        history = HISTORY_FILE.read_text(encoding="utf-8").strip()

        if history:
            print("\n" + "=" * 58)
            print("                    CHAT HISTORY")
            print("=" * 58)
            print(history)
            print("=" * 58)
        else:
            print(f"{BOT_NAME}: Your chat history is empty.")

    except OSError:
        print(f"{BOT_NAME}: Unable to read the chat history.")


def clear_history():
    confirmation = input(
        "Are you sure you want to clear saved chat history? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        try:
            HISTORY_FILE.write_text("", encoding="utf-8")
            print(f"{BOT_NAME}: Chat history cleared.")
        except OSError:
            print(f"{BOT_NAME}: Unable to clear chat history.")
    else:
        print(f"{BOT_NAME}: Chat history was not changed.")


def show_help():
    print("\nAVAILABLE COMMANDS")
    print("-" * 45)
    print("/help       Show available commands")
    print("/time       Display the current time")
    print("/date       Display today's date")
    print("/joke       Tell a programming joke")
    print("/quiz       Start a Python quiz")
    print("/calc       Open the calculator")
    print("/history    View saved conversation history")
    print("/clear      Clear saved conversation history")
    print("/name       Change your name")
    print("/quit       Exit the chatbot")
    print("-" * 45)
    print("You can also ask about Python, HTML, CSS, AI, and more.")


def get_user_name():
    while True:
        name = input("\nWhat should I call you? ").strip()

        if name and any(character.isalnum() for character in name):
            return name

        print("Please enter a valid name.")


def safe_calculate(expression):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg
    }

    def evaluate(node, depth=0):
        if depth > 20:
            raise ValueError("Expression is too complex.")

        if isinstance(node, ast.Expression):
            return evaluate(node.body, depth + 1)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left, depth + 1)
            right = evaluate(node.right, depth + 1)

            if abs(left) > 10**100 or abs(right) > 10**100:
                raise ValueError("Numbers are too large.")

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            result = allowed_operators[type(node.op)](left, right)

            if isinstance(result, complex):
                raise ValueError("Complex results are not supported.")

            if isinstance(result, (int, float)) and abs(result) > 10**100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](
                evaluate(node.operand, depth + 1)
            )

        raise ValueError("Unsupported expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree)

        if isinstance(result, float) and not __import__("math").isfinite(result):
            return "The result is outside the supported numeric range."

        return f"Result: {result}"

    except ZeroDivisionError:
        return "Division by zero is not allowed."
    except (ValueError, TypeError, OverflowError, SyntaxError, MemoryError):
        return "Invalid calculation. Try something like 12 * (5 + 3)."


def calculator():
    print(f"\n{BOT_NAME}: Enter a mathematical expression.")
    print("Supported operators: +, -, *, /, //, %, **")
    print("Type 'back' to return to the conversation.")

    while True:
        expression = input("Calculate: ").strip()

        if expression.lower() == "back":
            break

        if not expression:
            print("Please enter an expression.")
            continue

        if len(expression) > 200:
            print("Expression is too long.")
            continue

        print(safe_calculate(expression))


def start_quiz():
    questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))
    score = 0

    print(f"\n{BOT_NAME}: Welcome to the Python Quiz!")
    print("Enter A, B, C, or D to answer.")
    print("Type 'quit' to stop the quiz.")

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for option in question["options"]:
            print(option)

        while True:
            answer = input("Your answer: ").strip().upper()

            if answer == "QUIT":
                print(f"{BOT_NAME}: Quiz ended.")
                print(f"Your score: {score}/{number - 1}")
                return

            if answer in ("A", "B", "C", "D"):
                break

            print("Please enter A, B, C, or D.")

        if answer == question["answer"]:
            print("Correct answer!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {question['answer']}.")

    print("\nQUIZ COMPLETED")
    print(f"Your final score: {score}/{len(questions)}")

    if score == len(questions):
        print("Excellent work! You answered every question correctly.")
    elif score >= 3:
        print("Good job! Keep practising.")
    else:
        print("Keep learning. Practice will help you improve!")


def find_response(message, user_name):
    text = message.lower().strip()
    normalized = text.rstrip("?!., ")

    if normalized in ("hi", "hello", "hey", "good morning", "good evening"):
        return random.choice([
            f"Hello, {user_name}! How can I help you?",
            f"Hey {user_name}! Nice to chat with you.",
            f"Hi {user_name}! What's on your mind?"
        ])

    if "how are you" in text:
        return "I'm functioning well and ready to chat. How are you?"

    if "your name" in text or "who are you" in text:
        return f"I'm {BOT_NAME}, a rule-based chatbot built with Python."

    if "my name" in text:
        return f"Your name is {user_name}, as you told me earlier."

    if "thank" in text:
        return random.choice([
            "You're welcome!",
            "Happy to help!",
            "Anytime! What else would you like to know?"
        ])

    if "who created you" in text or "your creator" in text:
        return "I was created using Python and a collection of predefined rules."

    if "joke" in text:
        return random.choice(JOKES)

    if text in ("help", "commands"):
        show_help()
        return None

    if "what can you do" in text:
        return "I can chat, tell jokes, answer basic programming questions, run a quiz, and calculate expressions."

    if "how old are you" in text:
        return "I don't have a human age. I'm a Python program!"

    for topic, answer in KNOWLEDGE.items():
        if text == topic or text in (
            f"what is {topic}",
            f"what is {topic}?",
            f"tell me about {topic}"
        ):
            return answer

    return random.choice([
        "I don't know the answer to that yet. Try asking about Python or technology.",
        "I'm still learning predefined responses. Type /help to see what I can do.",
        "I couldn't understand that question. Could you try phrasing it differently?"
    ])


def handle_command(message, user_name):
    command = message.lower().strip()

    if command == "/help":
        show_help()

    elif command == "/time":
        print(f"{BOT_NAME}: Current time: {datetime.now().strftime('%I:%M:%S %p')}")

    elif command == "/date":
        print(f"{BOT_NAME}: Today's date: {datetime.now().strftime('%d %B %Y')}")

    elif command == "/joke":
        print(f"{BOT_NAME}: {random.choice(JOKES)}")

    elif command == "/quiz":
        start_quiz()

    elif command == "/calc":
        calculator()

    elif command == "/history":
        show_history()

    elif command == "/clear":
        clear_history()

    elif command == "/name":
        return get_user_name()

    elif command in ("/quit", "/exit"):
        print(f"{BOT_NAME}: Goodbye, {user_name}! Take care.")
        return None

    else:
        print(f"{BOT_NAME}: Unknown command. Type /help to see available commands.")

    return user_name


def main():
    display_banner()
    user_name = get_user_name()

    greeting = f"Hello, {user_name}! I'm {BOT_NAME}. Let's start chatting."
    print(f"\n{BOT_NAME}: {greeting}")
    save_message(BOT_NAME, greeting)

    while True:
        try:
            message = input(f"\n{user_name}: ").strip()

            if not message:
                print(f"{BOT_NAME}: Please enter a message.")
                continue

            save_message(user_name, message)

            if message.lower() in ("/quit", "/exit", "bye", "goodbye"):
                print(f"{BOT_NAME}: Goodbye, {user_name}! Have a great day.")
                save_message(BOT_NAME, f"Goodbye, {user_name}!")
                break

            if message.startswith("/"):
                updated_name = handle_command(message, user_name)

                if updated_name is None:
                    save_message(BOT_NAME, f"Goodbye, {user_name}!")
                    break

                if updated_name != user_name:
                    user_name = updated_name
                    print(f"{BOT_NAME}: I'll call you {user_name} from now on.")

                continue

            response = find_response(message, user_name)

            if response:
                print(f"{BOT_NAME}: {response}")
                save_message(BOT_NAME, response)

        except (KeyboardInterrupt, EOFError):
            print(f"\n{BOT_NAME}: Conversation interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()