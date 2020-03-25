#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An enhanced version of the 'echo' cmd line utility"""

__author__ = "knmarvel"


import argparse
import sys


def dirwatcher():



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
    


if __name__ == "__main__":
    main()
