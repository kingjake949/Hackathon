questions = ("What is Food Waste?",                  #lots of research and help from youtube to figure out the quiz
            "Which of the following is the most common reason for food waste at home?",
            "Which of the following is a way to reduce food waste?",
            "What is 'Best Before' date?",
            "Which food item is often wasted in most households?")

options = (("A. Throwing away food because it is expired", "B. Food that is not eaten and discarded ", "C. Eating food that has been on the floor", "D. Cooking more food than needed"),
           ("A. Over-purchasing groceries", "B. Not knowing how to cook", "C. Eating expired food", "D. Not liking the food"),
           ("A. Buy only as much fod as you will eat", "B. Throw away leftovers", "C. Avoid using reusable containers", "D. Shop without a list"),
           ("A. The date when food must be consumed", "B. The date after which food becomes unsafe to eat", "C. A suggestion for the food's best quality", "D. A warning label for food allergies"),
           ("A. Fresh fruit and vegetables", "B. Frozen meals", "C. Bottled drinks", "D. Canned food"))

answers = ("B", "A", "A", "C", "A")     # gives the computer the correct answers the user should input
guesses = []                            # there is only one guess
question_num = 0                        # shows that it starts at the first question, once the user inpts an answer
                                        # the code registers it and follows up to the next question
for question in questions:
    print()
    print(question)
    for option in options[question_num]:
        print(option)

    guess = input("Enter (A, B, C, D): ").upper()  # incase user inputs a guess in lowercase, the code changes
    guesses.append(guess)                          # it to uppercase to not confuse the computer
    if guess == answers[question_num]:             # this function shows the product if the user gets the answer
        print("Correct!")                          # right/wrong it will print different answers
    else:
        print("Incorrect :(")
        print(f"{answers[question_num]} is the correct answer")
    question_num += 1

print("Thank you For Playing the Quiz")