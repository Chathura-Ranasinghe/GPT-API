import json
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI()

# File path for storing conversation history
history_file_path = "conversation_history.json"

# Load conversation history from file if it exists
if os.path.exists(history_file_path) and os.stat(history_file_path).st_size > 0:
    with open(history_file_path, "r") as file:
        try:
            conversation_history = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the file is not valid JSON
            print("Error: The file does not contain valid JSON data.")
            conversation_history = []
else:
    # Initialize conversation history if the file doesn't exist or is empty
    conversation_history = []

# Initial system message
print("\n\033[92mgpt : Hi there! How can I help you?")

# Chat loop
while True:
    # Get user input

    user_input = input("\n\033[97mme  > ") # \033[92m represents white color

    # Add user input with formatted date and time to conversation history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_message = {"role": "user", "content": f"{user_input} - {timestamp}"}
    conversation_history.append(user_message)


    # Create a completion using the user input
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
                *conversation_history
            ]
        )
    except Exception as e:
        print(f"Error communicating with OpenAI: {str(e)}")
        # Handle the error gracefully, perhaps by asking the user to try again
        continue  # Skip the rest of the loop and ask for user input again
    
    if user_input.lower() == "undo":
      if len(conversation_history) > 1:
          conversation_history.pop()  # Remove the last user message
      else:
          print("Cannot undo further.")
      continue  # Skip the rest of the loop and ask for user input again


    # Break the loop if the user input is "goodbye"
    if user_input.lower() == "goodbye":
        model_reply = completion.choices[0].message.content
        conversation_history.pop()  # Remove the goodbye message
        print("\033[92mgpt >", model_reply)  # \033[92m represents green color
        print("\033[97m\n", end="")
        break

    # Get the model's reply
    model_reply = completion.choices[0].message.content

    # Print the model's response
    print("\033[92mgpt >", model_reply)  # \033[92m represents green color

# Save conversation history to file
with open(history_file_path, "w") as file:
    json.dump(conversation_history, file)