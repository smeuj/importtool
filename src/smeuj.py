import tkinter as tk
import re
import json
import sys

class State:
    def __init__(self, out_path, smeuj = [], chat = [], index = -1):
        self.out_path = out_path
        self.smeuj    = smeuj
        self.chat     = chat
        self.index    = index

def apply(f, *args):
    def g():
        f(*args)
    return g

def add_smeu(state, author, inspiration, date, time, content, example):
    state.smeuj.append({
        "author":      author.get(),
        "inspiration": inspiration.get() if inspiration.get() else None,
        "date":        date.get(),
        "time":        time.get(),
        "content":     content.get(),
        "example":     example.get() if example.get() else None
    })

def change_chat_entry(step, state, author, inspiration, date, time, content, example):
    state.index += step
    if state.index < 0:
        state.index = len(state.chat) - 1
    elif state.index >= len(state.chat):
        state.index = 0
    entry = state.chat[state.index]
    author.set(entry["author"])
    inspiration.set("")
    date.set(entry["date"])
    time.set(entry["time"])
    content.set(entry["message"])
    example.set("")

def save(state):
    with open(state.out_path, "w", encoding = "utf-8") as dest:
        json.dump(state.smeuj, dest, indent = 4)

def undo(state):
    state.smeuj.pop()

def setup_ui(state):
    ui = tk.Tk()
    ui.title("Smeuj")

    author          = tk.StringVar()
    lbl_author      = tk.Label(text = "Author")
    ent_author      = tk.Entry(textvariable = author)
    inspiration     = tk.StringVar()
    lbl_inspiration = tk.Label(text = "Inspiration")
    ent_inspiration = tk.Entry(textvariable = inspiration)
    date            = tk.StringVar()
    lbl_date        = tk.Label(text = "Date")
    ent_date        = tk.Entry(textvariable = date)
    time            = tk.StringVar()
    lbl_time        = tk.Label(text = "Time")
    ent_time        = tk.Entry(textvariable = time)
    content         = tk.StringVar()
    lbl_content     = tk.Label(text = "Content")
    ent_content     = tk.Entry(textvariable = content, width = 256)
    example         = tk.StringVar()
    lbl_example     = tk.Label(text = "Example")
    ent_example     = tk.Entry(textvariable = example)

    lbl_author.pack()
    ent_author.pack()
    lbl_inspiration.pack()
    ent_inspiration.pack()
    lbl_date.pack()
    ent_date.pack()
    lbl_time.pack()
    ent_time.pack()
    lbl_content.pack()
    ent_content.pack()
    lbl_example.pack()
    ent_example.pack()

    btn_add  = tk.Button(text = "Add",  command = apply(
        add_smeu, state, author, inspiration, date, time, content, example
    ))
    btn_next = tk.Button(text = "Next", command = apply(
        change_chat_entry, 1, state, author, inspiration, date, time, content,
        example
    ))
    btn_prev = tk.Button(text = "Previous", command = apply(
        change_chat_entry, -1, state, author, inspiration, date, time, content,
        example
    ))
    btn_save = tk.Button(text = "Save", command = apply(save, state))
    btn_undo = tk.Button(text = "Undo", command = apply(undo, state))

    btn_add.pack()
    btn_next.pack()
    btn_prev.pack()
    btn_save.pack()
    btn_undo.pack()

    return ui

def main(in_path, out_path):
    chat = None
    with open(in_path, encoding = "utf-8") as source:
        chat = json.load(source)

    ui = setup_ui(State(out_path, chat = chat))
    ui.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python smeuj.py <input_path> <output_path>")
    else:
        main(sys.argv[1], sys.argv[2])
