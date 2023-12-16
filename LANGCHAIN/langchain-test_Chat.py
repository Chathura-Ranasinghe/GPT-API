import os
import sys
from datetime import datetime

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

# Redirect stderr to null
sys.stderr = open(os.devnull, 'w')

loader = TextLoader('data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

log_file = open("chat_log.txt", "a")

print("\ngpt  > Welcome to the chat! Type 'goodbye' to exit.")

conversation_history = []

while True:
    # Prompt the user for input
    query = input("\nuser > ")

    if query:
        # Append the user's query to the conversation history
        conversation_history.append(f"{query}")

        # Pass the entire conversation history to the model
        result = index.query("\n".join(conversation_history), llm=ChatOpenAI())

        try:
            result = index.query("\n".join(conversation_history), llm=ChatOpenAI())
            print("gpt  > ",result)
            conversation_history.append(f"{result}")
        except Exception as e:
            print("gpt  > An error occurred:", str(e))


        # Append the model's response to the conversation history
        conversation_history.append(f"{result}")

        log_file.write(f"{datetime.now()} - User: {query}, GPT: {result}\n")
        
    else:
        print("gpt  > No query provided.")

    if query.lower() == "goodbye":
        break
