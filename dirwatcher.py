#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Long running program that monitors a directory's text files."""

__author__ = "knmarvel"


import argparse
import datetime
import logging
import os
import signal
import sys
import time

if sys.version_info[0] != 3:
    raise Exception("This program requires python3 interpreter")


# globals
old_files = {}
running = True
start_time = time.time()


def logger(message):
    """Sets up log messages for the program"""
    logging_format = '%(asctime)s \n %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    logging.info(message)


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
                    for counter, line in enumerate(file):
                        if magic in line:
                            if filename in f_w_magic:
                                if f_w_magic[filename] < counter:
                                    f_w_magic[filename] = counter
                            else:
                                f_w_magic[filename] = counter
    return f_w_magic


def check_for_add(new_files):
    """Prints a statement about files added with magic text
    or files with magic text appended at a later line"""
    global old_files
    for file in new_files:
        if file in old_files:
            if new_files[file] > old_files[file]:
                logline1 = f"Magic text found in file"
                logline2 = f" {file} at line {new_files[file]}"
                logger(logline1 + logline2)
        else:
            logline1 = f"Magic text found in file {file} "
            logline2 = f"with at line {new_files[file]}."
            logger(logline1 + logline2)


def check_for_delete(new_files):
    """Logs a delete statement if a file with magic text is deleted."""
    global old_files
    for file in old_files:
        if file not in new_files:
            logger(f"File {file} deleted")


def print_difference(new_files):
    """checks dictionary of currently found files against previously
    found files and prints any differences"""
    global old_files
    if new_files != old_files:
        check_for_add(new_files)
        check_for_delete(new_files)
        old_files = new_files


def display_start_banner(interval, magic, search_dir, file_type):
    """logs starting banner"""
    title_text = "DIRWATCHER".center(80, "=")
    line = "\nWelcome to Kano's dirwatcher\n".center(80)
    line1 = f'Every {interval} seconds, dirwatcher will tell you if "{magic}"'
    line2 = f' is in any {file_type} files in directory "{search_dir}"'
    time_line = f'\nTime started: {datetime.datetime.now()}\n'
    end_line = "".center(80, "=")
    message = title_text + line + line1 + line2 + time_line + end_line
    logger(message)


def display_end_banner(reason):
    """logs ending banner"""
    line = f"You've ended dirwatcher at {datetime.datetime.now()}"
    line1 = f" because {reason}"
    line2 = f" after running {round(time.time() - start_time, 2)} seconds"
    line3 = f'\nHave a wonderful day.'
    line = line + line1 + line2 + line3
    line = ' %s ' % line
    line = line.center(80)
    message = "".center(80, "=") + line + "\n" + "".center(80, "=")
    logger(message)


def receive_signal(sig_num, frame):
    """Handler for SIGTERM, SIGQUIT, and SIGINT"""
    global running
    logger("Stopped by " + signal.Signals(sig_num).name)
    running = False


def create_parser(*args, **kwargs):
    """Defines and provides help for commandline arguments"""
    parser = argparse.ArgumentParser(
        description="Periodically check files for a certain string.")
    parser.add_argument('-dir',
                        help="directory to watch")
    parser.add_argument("-ext",
                        help="file type to search")
    parser.add_argument("int",
                        type=int,
                        default=1,
                        help="integer representing seconds between polls")
    parser.add_argument("magic",
                        help="text string to find in the directories")
    return parser.parse_args()


def main():
    """Long running program that monitors a directory's text files."""
    global running
    args = create_parser()
    interval = args.int
    magic = args.magic
    search_dir = args.dir
    file_type = args.ext

    display_start_banner(interval, magic, search_dir, file_type)

    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGQUIT, receive_signal)

    while running:
        try:
            if os.path.exists(search_dir):
                new_files = check_for_magic(magic, search_dir, file_type)
                print_difference(new_files)
            else:
                logger("No such directory.")
            time.sleep(interval)
            continue
        except KeyboardInterrupt as k:
            logger("Stopped by " + repr(k))
            display_end_banner(repr(k))
            running = False
        except Exception as e:
            logger("Stopped by " + repr(e))
            display_end_banner(repr(e))
            running = False
    display_end_banner("your computer terminated the program")


if __name__ == "__main__":
    main()
