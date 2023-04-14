import pickle
import os
import msvcrt as m

global notes
notes = []
counters = []
cursor = 0
user_input = ''

class Counter:
    def __init__(self, name = "", count = 0, max = 0):
        self.name = name
        self.count = int(count)
        self.max = int(max) if max else int(count)
        counters.append(self)
        
    def add(self):
        if self.count < self.max:
            self.count += 1
        
    def sub(self):
        if self.count > 0:
            self.count -= 1
            
    def fill(self):
        self.count = self.max

def save_data():
    with open("save.pickle", "wb") as file:
        pickle.dump((counters, notes), file)
            
def load_data():
    global counters
    global notes
    if not os.path.isfile("save.pickle"):
        notes = []
        return
    with open("save.pickle", "rb") as file:
        counters, notes = pickle.load(file)
        
def note_interface():
    """ Note interface and controls """
    global notes
    cursor = 0
    user_input = ''
    while not user_input == b'q':
        os.system("cls")
        print(" n) New  d) Delete  a) Append  q) Back |")
        print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨`")
        for _ in range(len(notes)):
            if cursor == _:
                print(">", end=" ")
            print(notes[_])        
        # Input
        user_input = m.getch()
        # Up/Down Arrows
        if user_input == b'H':
            if cursor > 0:
                cursor -= 1
        elif user_input == b'P':
            if cursor < len(notes) - 1:
                cursor += 1
        # New, Append, Delete
        elif user_input == b'n':
            cursor = len(notes)
            write_note(cursor)
        elif user_input == b'a':
            if notes:
                write_note(cursor, False)
        elif user_input == b'd':
            if notes:
                notes.pop(cursor)
            if cursor > 0:
                cursor -= 1

def write_note(n, new_note = True):
    """ Add / Append to notes[n] """
    entry = ""
    if new_note:
        notes.append("")
    while True:
        os.system("cls")
        print(" Write note:\n")
        print(notes[n])
        entry = input()
        if not entry == "":
            notes[n] += entry + "\n"
        else:
            break
    
load_data()

 # Main loop
while not user_input == b'\x1b':   
    ## Output ##
    os.system("cls")
    # Menu
    print(" a) Add  d) Delete  f) Fill  F) Fill all  n) Notes |" +
          " Navigate with arrow keys, Increase/decrease with +/-, Esc to quit")
    print("¨" * 120)
    for _ in range(len(counters)):
        # Active line
        if cursor == _:
            print(" >> ", end="")
        else:
            print("    ", end="")
        # Counter list
        print(_ + 1, counters[_].name, sep=". ", end=" | ")
        print(counters[_].count, "/", counters[_].max, "|", "I"*counters[_].count)
    ## User Input ##
    user_input = m.getch()
    # Up/Down Arrows
    if user_input == b'H':
        if cursor > 0:
            cursor -= 1
    elif user_input == b'P':
        if cursor < len(counters) - 1:
            cursor += 1
    # +/-
    elif user_input == b'+':
        counters[cursor].add()
    elif user_input == b'-':
        counters[cursor].sub()
    # Fill & Fill All
    elif user_input == b'f':
        if not counters == []:
            counters[cursor].fill()
    elif user_input == b'F':
        for _ in counters:
            _.fill()
    # Add
    elif user_input == b'a':
        print()
        Counter(input("Name: "), input("Count: "), input("Max: "))
    # Delete
    elif user_input == b'd':
        if counters:
            counters.pop(cursor)
        if cursor == len(counters) != 0:
            cursor -= 1
    # Notes
    elif user_input == b'n' or user_input == b'N':
        note_interface()
    # Esc
    elif user_input == b'\x1b':
        os.system("cls")
        save_data()