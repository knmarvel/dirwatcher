#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An enhanced version of the 'echo' cmd line utility"""

__author__ = "knmarvel"


import argparse
import sys
import os


def check_for_string(magic, search_dir, file_type):
    files_with_magic = []
    if os.path.exists(search_dir):
        for root, dirs, filenames in os.walk(search_dir):
            for filename in filenames:
                if file_type in filename:
                    with open(filename, "r") as file:
                        file = file.read().splitlines()
                        for line in file:
                            if magic in line:
                                files_with_magic.append(
                                    [filename, file.index(line)])
    return len(files_with_magic) > 0


def dirwatcher(interval, magic, search_dir, file_type):
    return check_for_string(magic, search_dir, file_type)


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
