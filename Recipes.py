# recipe_generator.py

# Import libraries we need
import requests  # to send a request to our chatbot
import datetime  # to get the date and time when saving the recipe

# This function will save the recipe to a text file
def save_recipe(recipe_text):
    # Get the current date and time
    now = datetime.datetime.now()

    # Make the date and time into a nice format for the filename
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file name using the timestamp
    filename = f"recipe_{timestamp}.txt"

    # Open a new file and write the recipe inside
    with open(filename, "w", encoding="utf-8") as file:
        file.write(recipe_text)

    # Tell the user the recipe was saved
    print(f"\nRecipe saved to '{filename}' successfully!")

# This function reads the list of scanned foods from a text file
def read_food_list(filename="foods.txt"):
    try:
        # Try to open the file and read each line
        with open(filename, "r") as file:
            # Remove empty lines and whitespace
            food_list = [line.strip() for line in file.readlines() if line.strip()]
        return food_list
    except FileNotFoundError:
        # If the file doesn't exist, tell the user
        print("No scanned food list found. Please run the scanner first.")
        return []

# This function sends the food list to the chatbot and asks for a recipe
def ask_chatbot(food_list):
    # Turn the list into one string separated by commas
    food_string = ', '.join(food_list)

    # Make a prompt to tell the chatbot what we have
    prompt = f"I have these ingredients: {food_string}. Can you suggest a recipe using them?"

    # Make the request we will send to the chatbot
    payload = {
        "model": "llama3",  # This is the model name (change if using different model)
        "prompt": prompt,
        "stream": False
    }

    # Send the request to the chatbot server
    response = requests.post("http://localhost:11434/api/generate", json=payload)

    # Check if the chatbot answered successfully
    if response.status_code == 200:
        # Get the recipe from the chatbot's answer
        result = response.json()
        recipe = result.get('response', '(No response)')
        return recipe
    else:
        # If something went wrong, show an error
        return f"Error communicating with chatbot: {response.status_code}"

# Main function that controls the whole program
def main():
    # First, read the food list from the file
    food_list = read_food_list()

    # If there is no food list, stop the program
    if not food_list:
        return

    # Print the foods we found
    print("\nScanned Food Items:")
    for item in food_list:
        print("-", item)

    # Tell the user we are asking the chatbot
    print("\nAsking the chatbot for a recipe...\n")

    # Ask the chatbot for a recipe
    recipe = ask_chatbot(food_list)

    # Print the recipe that was generated
    print("\nGenerated Recipe:\n")
    print(recipe)

    # Ask if the user wants to save the recipe
    saveYN = input("\nDo you want to save this recipe? (y/n): ")
    if saveYN.lower() == "y":
        save_recipe(recipe)
    else:
        # If they say no, just skip saving
        pass

# This makes sure main() runs if we start this file
if __name__ == "__main__":
    main()
