import sys
import json

from functools import reduce

def read_chat(chat_file):
    with open(chat_file, encoding = "utf-8") as file:
        return json.load(file)

def considered_equal(entry_a, entry_b):
    for k, v in entry_a.items():
        if v != entry_b[k]:
            return False
    return True

def join_chats(chat_a, chat_b):
    if chat_a == None:
        return None
    if len(chat_a) == 0:
        return chat_b
    if len(chat_b) == 0:
        return chat_a
    pivot = chat_a.pop()
    for i, entry in enumerate(chat_b):
        if considered_equal(pivot, entry):
            return chat_a + chat_b[i:]
    return None

def main(output_file, *chat_files):
    chats = [read_chat(chat_file) for chat_file in chat_files]
    chat  = reduce(join_chats, chats)
    if not chat:
        print("Chat logs do not overlap.")
        return
    with open(output_file, "w", encoding = "utf-8") as file:
        json.dump(chat, file, indent = 4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python join_chats.py <output_path> <chat_files...>"
        )
    else:
        main(sys.argv[1], *sys.argv[2:])
