import json
import os
import msvcrt as m

global notes
notes = [""]
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

def save_data():
    savedata = ""
    with open("saved.txt", "w") as file:
        for _ in counters:
            savedata += json.dumps(_.__dict__) + "\n"
        file.write(savedata)
        file.write("#\n") # Separator for counters & notes
        savedata = ""
        for _ in notes:
            savedata += str(_)
            savedata += "#\n"
        file.write(savedata[:-2] + "\n")
    
def load_data():
    global notes
    savedata = ""
    line = ""
    obj = {}
    n = 0
    if not os.path.isfile("saved.txt"):
        return
    with open("saved.txt", "r") as file:
        # Load counters
        line = file.readline()
        while not line == "#\n":
            obj = json.loads(line)
            Counter(obj["name"], obj["count"], obj["max"])
            line = file.readline()
        # Load notes
        while line:
            line = file.readline()
            if line == "#\n":
                notes.append("")
                n += 1
                line = file.readline()
            notes[n] += line
        
def note_interface():
    """ Note interface and controls """
    cursor = 0
    user_input = ''
    while not user_input == b'q':
        os.system("cls")
        print(" n) New d) Delete a) Append q) Back")
        print(" -----------------------------------\n")
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
        # Edit
        elif user_input == b'n':
            write_note(len(notes))
        elif user_input == b'a':
            write_note(cursor, False)
        # Delete
        elif user_input == b'd':
            if notes:
                notes.pop(cursor)
            if cursor > 0:
                cursor -= 1

def write_note(n, clear = True):
    """ Add / Append to notes[n] """
    entry = ""
    if clear:
        notes.append("")
        notes[n] = ""
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
    print(" a) Add d) Delete  f) Fill F) Fill all  N) Notes \
| Navigate with arrow keys, Increase/decrease with +/-, Esc to quit")
    print(" ----------------------------------------------\
---------------------------------------------------------------------\n")
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
            counters[cursor].count = counters[cursor].max
    elif user_input == b'F':
        for _ in counters:
            _.count = _.max
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
        save_data()