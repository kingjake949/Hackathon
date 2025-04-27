# smart_chef_camera.py

# Importing the libraries we need for this project
import cv2  # for using the webcam
import tensorflow as tf  # for using the AI model
from transformers import TFAutoModelForImageClassification, AutoImageProcessor  # from huggingface
import difflib  # to find close matches if the model is unsure

# Tell the user the model is loading
print("Loading model... (first time takes a minute)")

# Choose which model we want to use
model_name = "google/vit-base-patch16-224"

# Load the processor (which helps resize and prepare images for the model)
processor = AutoImageProcessor.from_pretrained(model_name)

# Load the actual model itself (this is what makes predictions)
model = TFAutoModelForImageClassification.from_pretrained(model_name)

# Tell the user the model finished loading
print("Model loaded successfully!")

# List of foods and food-related items
# (This helps us know what foods we want to detect)
FOOD_ITEMS = [
    # Original foods
    'guacamole', 'apple', 'carrot', 'pear', 'consomme', 'hot pot', 'trifle', 'ice cream', 'ice lolly',
    'french loaf', 'bagel', 'pretzel', 'cheeseburger', 'hotdog', 'mashed potato',
    'head cabbage', 'broccoli', 'cauliflower', 'zucchini', 'spaghetti squash',
    'acorn squash', 'butternut squash', 'cucumber', 'artichoke', 'bell pepper',
    'cardoon', 'mushroom', 'granny smith', 'strawberry', 'orange', 'lemon',
    'fig', 'pineapple', 'banana', 'jackfruit', 'custard apple', 'pomegranate',
    'carbonara', 'chocolate sauce', 'dough', 'meat loaf', 'pizza', 'potpie',
    'burrito', 'red wine', 'espresso', 'cup', 'eggnog',
    'bakery', 'cleaver', 'cocktail shaker', 'coffee mug', 'coffeepot',
    'confectionery', 'corkscrew', 'crock pot', 'dining table', 'dishrag',
    'dishwasher', 'dutch oven', 'frying pan', 'grocery store', 'kitchen utensil',
    'ladle', 'measuring cup', 'mixing bowl', 'pot', 'potter\'s wheel',
    'refrigerator', 'restaurant', 'saltshaker', 'spatula', 'soup bowl',
    'teapot', 'toaster', 'tray', 'waffle iron', 'water bottle', 'water jug',
    'whiskey jug', 'wine bottle', 'wooden spoon', 'plate',
    'apple', 'avocado', 'blueberry', 'blackberry', 'raspberry', 'grape',
    'watermelon', 'cantaloupe', 'honeydew', 'peach', 'pear', 'plum',
    'cherry', 'apricot', 'nectarine', 'mango', 'kiwi', 'coconut', 'lime',
    'carrot', 'potato', 'sweet potato', 'onion', 'garlic', 'lettuce',
    'spinach', 'kale', 'cabbage', 'green bean', 'pea', 'corn', 'eggplant',
    'radish', 'beet', 'celery', 'asparagus', 'brussels sprout',
    'beef', 'chicken', 'pork', 'turkey', 'lamb', 'salmon', 'tuna', 'shrimp',
    'crab', 'lobster',
    'butter', 'cheese', 'milk', 'cream', 'yogurt', 'bread', 'pasta', 'rice',
    'noodles', 'oatmeal', 'granola',
    'hamburger', 'sandwich', 'submarine sandwich', 'taco', 'quesadilla',
    'nachos', 'sushi', 'ramen', 'dumpling', 'spring roll', 'egg roll',
    'brownie', 'cookie', 'cake', 'cupcake', 'donut', 'muffin', 'pie', 'pudding',
    'jelly', 'jam', 'honey',
    'coffee', 'tea', 'lemonade', 'smoothie', 'milkshake', 'soda', 'beer',
    'whiskey', 'vodka', 'gin', 'wine', 'champagne'
]

# Function that prepares the image for the AI model
def preprocess(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image to RGB colors
    target_height = processor.size["height"]  # Get the height that the model expects
    target_width = processor.size["width"]    # Get the width that the model expects
    frame_resized = cv2.resize(frame_rgb, (target_width, target_height))  # Resize the image
    inputs = processor(images=frame_resized, return_tensors="tf")  # Get it ready for the model
    return inputs

# This list will store the food items we detect
scanned_food_list = []

# Start the webcam
cap = cv2.VideoCapture(0)

# Ask the user if they want to delete the old food list
deleteYN = input("Would you like to delete the previous food items (y/n): ")
if deleteYN.lower() == "y":
    # If yes, open the file and clear it
    with open('foods.txt', 'r') as file:
        content = file.read()
    content = content.replace(content, '')  # Clear everything
    with open('foods.txt', 'w') as file:
        file.write(content)
else:
    # If no, do nothing
    pass

# Tell the user how to use the program
print("\nPress 'c' to capture an image and detect food.")
print("Press 'q' to quit.\n")

# Main loop that keeps the camera running
while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame.")  # Error if camera frame doesn't work
        break

    cv2.imshow("Smart Chef Camera", frame)  # Show the frame
    key = cv2.waitKey(1)  # Wait for a key press

    if key == ord('c'):  # If 'c' key is pressed
        # Preprocess the frame
        inputs = preprocess(frame)
        outputs = model(**inputs)
        preds = outputs.logits

        # Get the best prediction
        predicted_class_idx = int(tf.argmax(preds, axis=-1)[0])
        label = model.config.id2label[predicted_class_idx].lower()

        # See if it's an exact food match
        if label in FOOD_ITEMS:
            print("Detected food item:", label)
            scanned_food_list.append(label)  # Add to our list
        else:
            # If not exact, find the closest match
            closest_matches = difflib.get_close_matches(label, FOOD_ITEMS, n=1, cutoff=0.6)
            if closest_matches:
                approx_label = closest_matches[0]
                print(f"Approximate match found: {approx_label}")
                scanned_food_list.append(approx_label)
            else:
                # If no match at all
                print("Not a recognized or close food item. Ignored.")

    elif key == ord('q'):  # If 'q' key is pressed
        break  # Exit the loop

# After exiting the loop, release the camera
cap.release()
cv2.destroyAllWindows()

# Print the final list of detected foods
print("\nFinal scanned food items:")
print(scanned_food_list)

# Save the food list to a text file
if scanned_food_list:
    with open("foods.txt", "w") as file:
        for item in scanned_food_list:
            file.write(f"{item}\n")
    print("\nFood list saved to 'foods.txt'.")
else:
    print("No food items were scanned. Nothing saved.")
