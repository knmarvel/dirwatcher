#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An enhanced version of the 'echo' cmd line utility"""

__author__ = "knmarvel"


import argparse
import os

old_files = {}
new_files = {}


def check_for_magic(magic, search_dir, file_type):
    """Given a magic string, a directory, and a file type,
    returns a dictionary of all files of the file type in
    the directory that contain the string with the last line
    of the file."""
    f_w_magic = {}
    if os.path.exists(search_dir):
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


def dirwatcher(interval, magic, search_dir, file_type):
    return check_for_magic(magic, search_dir, file_type)


def create_parser(*args, **kwargs):
    """Defines and provides help for commandline arguments"""
    parser = argparse.ArgumentParser(
        description="Periodically check files for a certain string.")
    parser.add_argument("interval",
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
