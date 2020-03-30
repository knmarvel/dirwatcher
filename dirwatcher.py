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


#globals
old_files = {}
running = True


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
            logline1 = f"Magic text found in file {file} found "
            logline2 = f"with magic text at line {new_files[file]}."
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
    """prints starting banner"""
    title_text = "DIRWATCHER"
    title_text = title_text.center(100, "=")
    line = "Welcome to Kano's dirwatcher".center()
    line1 = f'Every {interval} seconds, dirwatcher will tell you if "{magic}"'
    line2 = f' is in any {file_type} files in directory "{search_dir}"'
    time_line = f'\nTime started: {datetime.datetime.now()}'
    end_line = "".center(100, "=")
    text = title_text + "\n" + line1 + line2 + time_line + "\n" + end_line
    logger(text)


def display_end_banner():
    """prints ending banner"""
    title_text = f"You've ended dirwatcher at {datetime.datetime.now()}"
    title_text = ' %s ' % title_text
    title_text = title_text.center()
    line1 = f'\nHave a wonderful day.'
    message = "".center(100, "=") + title_text + line1 + "\n" + "".center(100, "=")
    logger(message)


def receive_signal(sig_num, frame):
    """HANDLER FOR TIGTERM AND SIGINT"""
    global running
    logger("Received " + signal.Signals(sig_num).name)
    running = False


def dirwatcher(interval, magic, search_dir, file_type):
    display_start_banner(interval, magic, search_dir, file_type)
    global running
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
    display_end_banner("Exited program")


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
    args = create_parser()
    dirwatcher(args.int, args.magic, args.dir, args.ext)


if __name__ == "__main__":
    main()
