import sys
import json

def unique_authors(chat):
    return { entry["author"] for entry in chat }

def main(chat_path):
    chat = None
    with open(chat_path, encoding = "utf-8") as file:
        chat = json.load(file)
    for author in unique_authors(chat):
        print(author)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unique_authors.py <chat_path>")
    else:
        main(sys.argv[1])
