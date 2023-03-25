import json
import os
import msvcrt as m

counters = []
cursor = 0
user_input = ""

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
        savedata = savedata[:-1]
        file.write(savedata)    
    
def load_data():
    savedata = ""
    obj = ""
    if not os.path.isfile("saved.txt"):
        return
    with open("saved.txt", "r") as file:
        for line in file:
            obj = json.loads(line)
            Counter(obj["name"], obj["count"], obj["max"])


load_data()

while user_input != b'\x1b':   
    ## Output ##
    os.system("cls")
    for _ in range(len(counters)):
        # Active Line
        if cursor == _:
            print(" >> ", end="")
        else:
            print("    ", end="")
        # Counter List
        print(_ + 1, counters[_].name, sep=". ", end=" || ")
        print(counters[_].count, "/", counters[_].max, "||", "I"*counters[_].count)
    # Menu
    print("\n a) Add d) Delete f) Fill F) Fill All | Navigate with arrow keys, Increase/decrease counters with +/-, Esc to quit")

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

    # Esc
    elif user_input == b'\x1b':
        save_data()