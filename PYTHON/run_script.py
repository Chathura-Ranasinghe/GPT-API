import os

def run_chat_script():
    print("Running openai-test_Chat.py")
    os.system("python openai-test_Chat.py")

def run_image_script():
    print("Running openai-test_Image.py")
    os.system("python openai-test_Image.py")

def main():
    print("Choose a script to run:")
    print("1. Run openai-test_Chat.py")
    print("2. Run openai-test_Image.py")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        run_chat_script()
    elif choice == "2":
        run_image_script()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
