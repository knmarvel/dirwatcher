#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An enhanced version of the 'echo' cmd line utility"""

__author__ = "knmarvel"


import argparse
import os
import time
import datetime

old_files = {}


def check_for_magic(magic, search_dir, file_type):
    """Given a magic string, a directory, and a file type,
    returns a dictionary of all files of the file type in
    the directory that contain the string with the last line
    of the file."""
    f_w_magic = {}
    for root, dirs, filenames in os.walk(search_dir):
        for filename in filenames:
            if filename.endswith(file_type):
                with open(root + "/" + filename, "r") as file:
                    file = file.read().splitlines()
                    for line in file:
                        if magic in line:
                            if filename in f_w_magic:
                                if f_w_magic[filename] < file.index(line):
                                    f_w_magic[filename] = file.index(line)
                            else:
                                f_w_magic[filename] = file.index(line)
    return f_w_magic


def print_difference(new_files):
    """checks dictionary of currently found files against previously
    found files and prints any differences"""
    global old_files
    if new_files != old_files:
        for file in new_files:
            if file in old_files:
                if new_files[file] != old_files[file]:
                    print("Magic text found in later line in file",
                          file, " at line ", new_files[file])
            else:
                print("New file", file, "found with magic text at line ",
                      new_files[file])
        for file in old_files:
            if file not in new_files:
                print("File", file, "deleted")
        old_files = new_files


def display_start_banner(interval, magic, search_dir, file_type):
    """prints starting banner"""
    title_text = "Welcome to Kano's dirwatcher"
    line1 = f'every {interval} seconds, dirwatcher will tell you if "{magic}"'
    line2 = f' is in any {file_type} files in directory "{search_dir}"'
    spaced_text = ' %s ' % title_text
    print(spaced_text.center(100, "="))
    print((line1 + line2).center(100, "~"))
    print(f'Time started: {datetime.datetime.now()}')
    print("".center(100, "="))


def display_end_banner():
    """prints ending banner"""
    title_text = f"You've ended dirwatcher at {datetime.datetime.now()}"
    line1 = f'Have a good rest of your life'
    spaced_text = ' %s ' % title_text
    print(spaced_text.center(100, "="))
    print((line1).center(100, "~"))
    print("".center(100, "="))


def dirwatcher(interval, magic, search_dir, file_type):
    running = True

    display_start_banner(interval, magic, search_dir, file_type)

    while running:
        try:
            if os.path.exists(search_dir):
                new_files = check_for_magic(magic, search_dir, file_type)
                print_difference(new_files)
            else:
                print("No such directory.")
            time.sleep(interval)
            continue
        except KeyboardInterrupt as ki:
            print("Stopped: ", repr(ki))
            display_end_banner()
            running = False
        except EOFError as eofe:
            print("Stopped: ", repr(eofe))
            display_end_banner()
            running = False


def create_parser(*args, **kwargs):
    """Defines and provides help for commandline arguments"""
    parser = argparse.ArgumentParser(
        description="Periodically check files for a certain string.")
    parser.add_argument("interval",
                        type=int,
                        help="integer representing seconds between polls")
    parser.add_argument("magic",
                        help="text string to find in the directories")
    parser.add_argument('-d',
                        help="directory to watch")
    parser.add_argument("-t",
                        help="file type to search")
    return parser.parse_args()


def main():
    args = create_parser()
    answer = dirwatcher(args.interval, args.magic, args.d, args.t)
    print(answer)
    return answer


if __name__ == "__main__":
    main()
