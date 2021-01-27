import sys
import json
import os

def chop(xs, n):
    if len(xs) <= n:
        return [xs]
    return [xs[:n], *chop(xs[n:], n)]

def main(input_file, n = 400):
    chat = None
    with open(input_file, encoding = "utf-8") as file:
        chat = json.load(file)
    chunks = chop(chat, n)
    for i, chunk in enumerate(chunks):
        num  = "{:0>3}".format(i)
        name = f"chunk{num}"
        os.mkdir(f"output/{name}")
        with open(f"output/{name}/{name}.json", "w", encoding = "utf-8") as file:
            json.dump(chunk, file, indent = 4)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python divide.py <input file> []")
