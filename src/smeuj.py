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

def add_smeu(state, trv_smeuj, author, inspiration, date, time, content, example):
    smeu = {
        "author":      author.get(),
        "inspiration": inspiration.get() if inspiration.get() else None,
        "date":        date.get(),
        "time":        time.get(),
        "content":     content.get(),
        "example":     example.get() if example.get() else None
    }
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
    state.smeuj.append(smeu)
    save(state)

def change_chat_entry(index, state, author, inspiration, date, time, content, example):
    state.index = index
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

def change_chat_entry_to_selected(event, trv_chat, state, author, inspiration, date, time, content, example):
    selection = trv_chat.identify("item", event.x, event.y)
    if selection:
        change_chat_entry(
            trv_chat.index(selection), state,
            author, inspiration, date, time, content, example
        )

def decrement_chat_entry(state, author, inspiration, date, time, content, example):
    change_chat_entry(state.index - 1, state, author, inspiration, date, time, content, example)

def increment_chat_entry(state, author, inspiration, date, time, content, example):
    change_chat_entry(state.index + 1, state, author, inspiration, date, time, content, example)

def save(state):
    with open(state.out_path, "w", encoding = "utf-8") as dest:
        json.dump(state.smeuj, dest, indent = 4)

def delete(state, trv_smeuj):
    selection = trv_smeuj.selection()
    indices   = { trv_smeuj.index(item) for item in selection }
    trv_smeuj.delete(*selection)
    state.smeuj = [
        smeu for i, smeu in enumerate(state.smeuj)
        if i not in indices
    ]
    save(state)

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

    trv_chat = ttk.Treeview(ui)
    trv_chat["columns"] = (
        "date", "time", "author", "message"
    )

    trv_chat.column("#0", width = 0, stretch = False)
    trv_chat.column("date",    anchor = tk.W, width = 60,  stretch = False)
    trv_chat.column("time",    anchor = tk.W, width = 60,  stretch = False)
    trv_chat.column("author",  anchor = tk.W, width = 120, stretch = False)
    trv_chat.column("message", anchor = tk.W, width = 360, stretch = False)

    trv_chat.heading("#0", text = "")
    trv_chat.heading("date",    anchor = tk.W, text = "Date")
    trv_chat.heading("time",    anchor = tk.W, text = "Time")
    trv_chat.heading("author",  anchor = tk.W, text = "Author")
    trv_chat.heading("message", anchor = tk.W, text = "Message")

    for entry in state.chat:
        trv_chat.insert(
            parent = "",
            index  = "end",
            iid    = None,
            text   = "",
            values = (
                entry["date"],
                entry["time"],
                entry["author"],
                entry["message"]
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
    ent_content     = tk.Entry(textvariable = content, width = 128)
    example         = tk.StringVar()
    lbl_example     = tk.Label(text = "Example")
    ent_example     = tk.Entry(textvariable = example)

    trv_smeuj.pack()
    trv_chat.pack()
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

    trv_chat.bind("<Button-1>", lambda event: change_chat_entry_to_selected(
        event, trv_chat, state,
        author, inspiration, date, time, content, example
    ))

    btn_add  = tk.Button(text = "Add",  command = apply(
        add_smeu, state, trv_smeuj,
        author, inspiration, date, time, content, example
    ))
    btn_delete = tk.Button(text = "Delete", command = apply(
        delete, state, trv_smeuj
    ))
    btn_next = tk.Button(text = "Next", command = apply(
        increment_chat_entry, state,
        author, inspiration, date, time, content, example
    ))
    btn_prev = tk.Button(text = "Previous", command = apply(
        decrement_chat_entry, state,
        author, inspiration, date, time, content, example
    ))

    btn_add.pack()
    btn_next.pack()
    btn_prev.pack()
    btn_delete.pack()

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
