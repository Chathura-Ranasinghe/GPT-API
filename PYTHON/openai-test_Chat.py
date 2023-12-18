import json
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAI client
client = OpenAI(api_key=api_key)

# File path for storing conversation history
dynamic_file_path = "data/dynamic_data.json"
static_file_path = "data/static_data.json"

# Set the maximum number of messages to keep in the conversation history
max_history_length = 50

# Load conversation history from file if it exists
if os.path.exists(dynamic_file_path) and os.stat(dynamic_file_path).st_size > 0:
    with open(dynamic_file_path, "r") as file:
        try:
            conversation_history = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the file is not valid JSON
            print("Error: The file does not contain valid JSON data.")
            conversation_history = []
else:
    # Initialize conversation history if the file doesn't exist or is empty
    conversation_history = []

# Load personal data from file if it exists
if os.path.exists(static_file_path) and os.stat(static_file_path).st_size > 0:
    with open(static_file_path, "r") as file:
        try:
            personal_data = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the file is not valid JSON
            print("Error: The file does not contain valid JSON data.")
            personal_data = []
else:
    # Initialize conversation history if the file doesn't exist or is empty
    personal_data = []

# Initial system message
print("\n\033[92mgpt : Hi there! How can I help you?")

# Chat loop
while True:
    # Get user input

    user_input = input("\n\033[97mme  > ") # \033[92m represents white color

    # Add user input with formatted date and time to conversation history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_message = {"role": "user", "content": f"{user_input} - {timestamp}"}
    # user_message = {"role": "user", "content": user_input}
    conversation_history.append(user_message)


    # Create a completion using the user input
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
                *personal_data,
                *conversation_history,

            ]
        )
    except Exception as e:
        print(f"Error communicating with OpenAI: {str(e)}")
        # Handle the error gracefully, perhaps by asking the user to try again
        continue  # Skip the rest of the loop and ask for user input again

    # Append model reply to conversation history
    model_reply = completion.choices[0].message.content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # model_message = {"role": "assistant", "content": f"{model_reply} - {timestamp}"}
    model_message = {"role": "assistant", "content": model_reply}
    conversation_history.append(model_message)
    
    if user_input.lower() == "undo":
      if len(conversation_history) > 1:
          conversation_history.pop()  # Remove the last user message
      else:
          print("Cannot undo further.")
      continue  # Skip the rest of the loop and ask for user input again


    # Break the loop if the user input is "goodbye"
    if user_input.lower() == "goodbye":
        conversation_history.pop()  # Remove the goodbye message
        model_reply = completion.choices[0].message.content
        conversation_history.pop()  # Remove the gpt  message
        print("\033[92mgpt >", model_reply)  # \033[92m represents green color
        print("\033[97m\n", end="")
        break

    # Print the model's response
    print("\033[92mgpt >", model_reply)  # \033[92m represents green color

if len(conversation_history) > max_history_length:
    conversation_history = conversation_history[-max_history_length:]

# Save conversation history to file
with open(dynamic_file_path, "w") as file:
    json.dump(conversation_history, file)