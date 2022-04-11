import time
import os
from pynput.keyboard import Key, Listener

def get_current_ms():
    return round(time.time() * 1000)

pw_key_time_list = list()

def press_callback(key):
    # print(key, end=None)
    if key == Key.backspace and pw_key_time_list:
        pw_key_time_list.pop()
        return
    pw_key_time_list.append((key.__str__(), get_current_ms()))

def normalize_list():
    pw_key_time_list.pop()
    ln = len(pw_key_time_list)
    if ln == 0:
        return
    first_ms = int(pw_key_time_list[0][1])
    for i in range(0, ln):
        pw_key_time_list[i] = (pw_key_time_list[i][0], str(int(pw_key_time_list[i][1]) - first_ms))

def compare_list(lhs: list, rhs: list) -> bool:

    ln = len(lhs)

    if ln != len(rhs):
        return False

    for i in range(0, ln):
        if lhs[i][0] != rhs[i][0]:

            return False
        
        # abs() = 절댓값
        if not (abs(int(lhs[i][1]) - int(rhs[i][1])) < 60):
            print("On key ", lhs[i][0], ", ", str(abs(int(lhs[i][1]) - int(rhs[i][1]))), "ms difference detected")
            return False

    return True

listener = Listener(
    on_press=press_callback)
listener.start()
# listener.setDaemon(True)

print("Key listener callback activiated(", listener, ")")

if os.path.exists('.pwd'):
    f = open('.pwd', 'r+')
    string_data = f.readline()
    if len(string_data) == 0:
        print('Empty file, reseting...')
    else:
        string_data = string_data[:-1] # delete \n
        datalist = string_data.split(',')

        for tup in datalist:
            if not tup:
                break
            t = tup.split(':')
            pw_key_time_list.append((t[0], t[1]))

def do_something() -> bool:
    global pw_key_time_list
    pw_key_time_list = list()
    input("Enter the new password\n")
    normalize_list()
    # print(pw_key_time_list)
    first = pw_key_time_list
    pw_key_time_list = list() # make empty
    input("Retype your password\n")
    normalize_list()
    return compare_list(pw_key_time_list, first)

if len(pw_key_time_list) == 0:
    while not do_something():
        print("Those two are different!")
    print("Set password")
    f = open('.pwd', 'a')
    f.seek(0)
    f.truncate()
    for tup in pw_key_time_list:
        s = str(tup[0]) + ":" + str(tup[1])
        f.write(s + ",")
    f.close()

# backup
compare_to = pw_key_time_list

while True:
    pw_key_time_list = list()
    pw = input("Enter the password: ")
    normalize_list()

    if compare_list(compare_to, pw_key_time_list):
        print("맞는 연결입니다")
    else:
        print("올바른 유저가 아닙니다")

        # for i in range(0, min(len(compare_to), len(pw_key_time_list))):
        #     print(f"{compare_to[i][0]}:{compare_to[i][1]} -> {pw_key_time_list[i][0]}:{pw_key_time_list[i][1]}")

listener.join()


#idea by anonkorea4869 / www.github.com/anonkorea4869
