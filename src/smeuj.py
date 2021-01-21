import tkinter as tk
import re
import json
import sys

from tkinter import ttk

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

    trv_smeuj = ttk.Treeview(ui)
    trv_smeuj["columns"] = (
        "author", "inspiration", "date", "time", "content", "example"
    )

    trv_smeuj.column("#0", width = 0, stretch = False)
    trv_smeuj.column("author",      anchor = tk.W, width = 120, stretch = False)
    trv_smeuj.column("inspiration", anchor = tk.W, width = 120, stretch = False)
    trv_smeuj.column("date",        anchor = tk.W, width = 60, stretch = False)
    trv_smeuj.column("time",        anchor = tk.W, width = 60, stretch = False)
    trv_smeuj.column("content",     anchor = tk.W, width = 120, stretch = False)
    trv_smeuj.column("example",     anchor = tk.W, width = 120, stretch = False)

    trv_smeuj.heading("#0", text = "")
    trv_smeuj.heading("author",      anchor = tk.W, text = "Author")
    trv_smeuj.heading("inspiration", anchor = tk.W, text = "Inspiration")
    trv_smeuj.heading("date",        anchor = tk.W, text = "Date")
    trv_smeuj.heading("time",        anchor = tk.W, text = "Time")
    trv_smeuj.heading("content",     anchor = tk.W, text = "Content")
    trv_smeuj.heading("example",     anchor = tk.W, text = "Example")

    for smeu in state.smeuj:
        trv_smeuj.insert(
            parent = "",
            index  = "end",
            iid    = None,
            text   = "",
            values = (
                smeu["author"],
                smeu["inspiration"],
                smeu["date"],
                smeu["time"],
                smeu["content"],
                smeu["example"]
            )
        )

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

    trv_smeuj.pack()
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

def main(chat_path, smeuj_path):
    chat  = None
    smeuj = None
    with open(chat_path, encoding = "utf-8") as source:
        chat = json.load(source)
    with open(smeuj_path, encoding = "utf-8") as source:
        smeuj = json.load(source)

    ui = setup_ui(State(smeuj_path, chat = chat, smeuj = smeuj))
    ui.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python smeuj.py <chat_path> <smeuj_path>")
    else:
        main(sys.argv[1], sys.argv[2])
