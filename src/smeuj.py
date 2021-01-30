import tkinter as tk
import re
import json
import sys
import os

from tkinter import ttk

class State:
    def __init__(self, out_path, smeuj = [], chat = [], index = -1):
        self.out_path      = out_path
        self.smeuj         = smeuj
        self.chat          = chat
        self.index         = index
        self.selected_smeu = None

def apply(f, *args):
    def g():
        f(*args)
    return g

def all_equal(xs):
    return len(set(xs)) <= 1

def intercalate_str(xs, y):
    if not xs:
        return ""
    r = xs[0]
    for x in xs[1:]:
        r += y
        r += x
    return r

def insert_smeu(trv_smeuj, smeu, index = "end"):
    trv_smeuj.insert(
        parent = "",
        index  = index,
        iid    = None,
        text   = "",
        values = (
            smeu["author"],
            intercalate_str(smeu["inspirations"], ";")
            if smeu["inspirations"] else None,
            smeu["date"],
            smeu["time"],
            smeu["content"],
            intercalate_str(
                [example["content"] for example in smeu["examples"]], ";"
            ) if smeu["examples"] else None
        )
    )

def make_smeu(author, inspiration, date, time, content, example, ex_author,
        ex_date, ex_time):
    ex_contents = example.get().split(";")   if example.get() else []
    ex_authors  = ex_author.get().split(";") if ex_author.get() else []
    ex_dates    = ex_date.get().split(";")   if ex_date.get() else []
    ex_times    = ex_time.get().split(";")   if ex_time.get() else []
    if not all_equal(map(len, [ex_contents, ex_authors, ex_dates, ex_times])):
        return None
    return {
        "author":       author.get(),
        "inspirations": inspiration.get().split(";")
        if inspiration.get() else [],
        "date":         date.get(),
        "time":         time.get(),
        "content":      content.get(),
        "examples":     [
            {
                "content": ex_content,
                "author":  ex_author,
                "date":    ex_date,
                "time":    ex_time
            }
            for ex_content, ex_author, ex_date, ex_time
            in zip(ex_contents, ex_authors, ex_dates, ex_times)
        ]
    }

def add_smeu(state, trv_smeuj, author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time):
    smeu = make_smeu(
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    )
    insert_smeu(trv_smeuj, smeu)
    state.smeuj.append(smeu)
    save(state)
    # trv_smeuj.see()
    trv_smeuj.yview("moveto", 1.0)

def change_chat_entry(index, state, author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time):
    state.selected_smeu = None
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
    content.set(entry["message"].lower())
    example.set("")
    ex_author.set("")
    ex_date.set("")
    ex_time.set("")

def change_chat_entry_to_selected(event, trv_chat, state, author, inspiration,
        date, time, content, example, ex_author, ex_date, ex_time):
    selection = trv_chat.identify("item", event.x, event.y)
    if selection:
        change_chat_entry(
            trv_chat.index(selection), state,
            author, inspiration, date, time, content, example,
            ex_author, ex_date, ex_time
        )

def change_smeu_entry_to_selected(event, trv_smeuj, state, author, inspiration,
        date, time, content, example, ex_author, ex_date, ex_time):
    state.selected_smeu = None
    selection = trv_smeuj.identify("item", event.x, event.y)
    if not selection:
        return
    state.selected_smeu = trv_smeuj.index(selection)
    entry = state.smeuj[state.selected_smeu]
    author.set(entry["author"])
    inspiration.set(intercalate_str(entry["inspirations"], ";"))
    date.set(entry["date"])
    time.set(entry["time"])
    content.set(entry["content"])
    if entry["examples"]:
        get_str = lambda name: intercalate_str(
            [example[name] for example in entry["examples"]], ";"
        )
        example.set(get_str("content"))
        ex_author.set(get_str("author"))
        ex_date.set(get_str("date"))
        ex_time.set(get_str("time"))
    else:
        example.set("")
        ex_author.set("")
        ex_date.set("")
        ex_time.set("")

def edit(state, trv_smeuj, author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time):
    if not state.selected_smeu:
        return
    selection = trv_smeuj.selection()
    indices   = { trv_smeuj.index(item) for item in selection }
    if len(indices) != 1:
        state.selected_smeu = None
        return
    smeu = make_smeu(
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    )
    state.smeuj[state.selected_smeu] = smeu
    trv_smeuj.delete(*selection)
    insert_smeu(trv_smeuj, smeu, index = state.selected_smeu)
    save(state)

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
        insert_smeu(trv_smeuj, smeu)

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
    ex_author       = tk.StringVar()
    lbl_ex_author   = tk.Label(text = "Example author")
    ent_ex_author   = tk.Entry(textvariable = ex_author)
    ex_date         = tk.StringVar()
    lbl_ex_date     = tk.Label(text = "Example date")
    ent_ex_date     = tk.Entry(textvariable = ex_date)
    ex_time         = tk.StringVar()
    lbl_ex_time     = tk.Label(text = "Example time")
    ent_ex_time     = tk.Entry(textvariable = ex_time)

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
    lbl_ex_author.pack()
    ent_ex_author.pack()
    lbl_ex_date.pack()
    ent_ex_date.pack()
    lbl_ex_time.pack()
    ent_ex_time.pack()

    trv_chat.bind("<Button-1>", lambda event: change_chat_entry_to_selected(
        event, trv_chat, state,
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    ))
    trv_smeuj.bind("<Button-1>", lambda event: change_smeu_entry_to_selected(
        event, trv_smeuj, state,
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    ))
    btn_add  = tk.Button(text = "Add",  command = apply(
        add_smeu, state, trv_smeuj,
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    ))
    btn_delete = tk.Button(text = "Delete", command = apply(
        delete, state, trv_smeuj
    ))
    btn_edit = tk.Button(text = "Edit", command = apply(
        edit, state, trv_smeuj,
        author, inspiration, date, time, content,
        example, ex_author, ex_date, ex_time
    ))

    btn_add.pack()
    btn_delete.pack()
    btn_edit.pack()

    return ui

def main(chat_path, smeuj_path):
    chat  = None
    smeuj = None
    with open(chat_path, encoding = "utf-8") as file:
        chat = json.load(file)
    if not os.path.exists(smeuj_path):
        with open(smeuj_path, "w", encoding = "utf-8") as file:
            json.dump([], file)
    with open(smeuj_path, encoding = "utf-8") as file:
        smeuj = json.load(file)

    ui = setup_ui(State(smeuj_path, chat = chat, smeuj = smeuj))
    ui.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python smeuj.py <chat_path> <smeuj_path>")
    else:
        main(sys.argv[1], sys.argv[2])
