import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAI client
client = OpenAI(api_key=api_key)

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

# Redirect stderr to null
sys.stderr = open(os.devnull, 'w')

loader = TextLoader('data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

print("\ngpt  > Welcome to the chat! Type 'goodbye' to exit.")

conversation_history = []

while True:
    # Prompt the user for input
    query = input("\nuser > ")

    if query:
        # Append the user's query to the conversation history
        conversation_history.append(f"{query}")

        try:
            result = index.query("\n".join(conversation_history), llm=ChatOpenAI())
            print("gpt  > ",result)
            conversation_history.append(f"{result}")
        except Exception as e:
            print("gpt  > An error occurred:", str(e))

    else:
        print("gpt  > No query provided.")

    if query.lower() == "goodbye":
        break
