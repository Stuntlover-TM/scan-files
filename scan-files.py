import os
import subprocess
import datetime
import re

print("(You can press CTRl+C to stop the program anytime)\n")

try:
    from tqdm import tqdm
except:
    subprocess.call(["python", "-m", "pip", "install", "tqdm"])
    subprocess.call(["cls"], shell=True)
    from tqdm import tqdm

scan_dir = input("What directory or file would you like to scan? (Press enter to scan the current directory) ")
scan_word = input("What would you like to scan for? ")

if scan_dir == "":
    scan_dir = "."

if scan_word == "":
    proceed = input("This will search for all characters, are you sure you want to proceed? (Y/N)\n")
    if proceed.lower() in ("y", "ye", "yes"):
        proceed = True
    else:
        proceed = False
        exit()

first_write = True
is_file = os.path.isfile(scan_dir)
if is_file:
    with open(scan_dir, "r") as scan_file:
        scan_file_lines = scan_file.readlines()
files = os.listdir(scan_dir) if not is_file else scan_dir
prev_file = ""
occurences = 0

with open("search_log.log", "w") as logfile: pass

def log(filename, message, time):
    global first_write
    now = datetime.datetime.now()

    with open(filename, 'a') as logfile:
        if first_write:
            first_write = False
            logfile.write(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] " + message) if time == True else logfile.write(message)
        else:
            logfile.write(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] " + message + '\n') if time == True else logfile.write(message)# + "\n")


def search(path, filename, is_dir, pbar=None):
    global occurences, prev_file
    with open(path, "r") as file:
        lines = file.read().split("\n")
        line_number = 1

        for line in lines:
            if scan_word in str(line):
                line_occurences = line.count(scan_word)
                occurences += line_occurences

                for _ in range(line_occurences):
                    if is_dir:
                        ljust_amount = len(f'Found "{scan_word}" in {filename} on line {str(line_number).ljust(10)}:') + 10
                        log("search_log.log", f'Found "{scan_word}" in {filename} on line {str(line_number).ljust(10)}:'.ljust(ljust_amount) + line, True)
                    else:
                        filename = path.split("\\")[-1]
                        ljust_amount = len(f'Found "{scan_word}" in {filename} on line {str(line_number).ljust(10)}: ') + 10
                        log("search_log.log", f'Found "{scan_word}" in {filename} on line {str(line_number).ljust(10)}: '.ljust(ljust_amount) + line, True)
            
            if prev_file != filename:
                prev_file = filename

                if first_write and scan_word in str(line):
                    log("search_log.log", f"Scanning {filename}\n", False)

                elif scan_word in str(line):
                    log("search_log.log", f"\n\nScanning {filename}", False)

            line_number += 1
            pbar.update(1) if pbar else None


if not is_file:
    for filename in tqdm(files, desc="Scanning files"):
        file_path = os.path.join(scan_dir, filename)

        if not os.path.isdir(file_path) and not filename.lower().startswith("search_log"):
            try:
                search(file_path, filename, True)
            except: continue

else:
    with tqdm(total=len(scan_file_lines) + 1, desc="Scanning files") as pbar:
        file_path = os.path.join(scan_dir)
        search(file_path, file_path, pbar=pbar)

    pbar.close()


print(f"\n{occurences} total occurences, full list of files and line numbers listed in search_log.log")
