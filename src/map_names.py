import sys
import json

def main(chat_file, name_file, output_file = None):
    if output_file == None:
        output_file = chat_file
    mapping = None
    with open(name_file, encoding = "utf-8") as file:
        mapping = json.load(file)
    chat = None
    with open(chat_file, encoding = "utf-8") as file:
        chat = json.load(file)
    for entry in chat:
        author = entry["author"]
        if author in mapping:
            entry["author"] = mapping[author]
    with open(output_file, "w", encoding = "utf-8") as file:
        json.dump(chat, file, indent = 4)

if __name__ == "__main__":
    if 3 <= len(sys.argv) <= 4:
        main(*sys.argv[1:])
    else:
        print(
            "Usage: python map_names.py <chat_path> <name_path> [output_path]"
        )
        
