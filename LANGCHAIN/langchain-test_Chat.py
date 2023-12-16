import os
import sys

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

loader = TextLoader('data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

# Check if there is at least one command-line argument
if len(sys.argv) > 1:
    query = sys.argv[1]
    print(index.query(query, llm=ChatOpenAI()))
else:
    print("No command-line arguments provided.")


