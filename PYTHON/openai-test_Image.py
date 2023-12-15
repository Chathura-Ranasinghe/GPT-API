import webbrowser

from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

# Accessing the URL from the response and printing it
url = response.data[0].url  # Assuming you want the URL from the first image
print(url)

# Opening the URL in the default web browser
webbrowser.open(url)
