![Kano's logo](https://i.imgur.com/Yc5nxbI.png) 

# Dirwatcher
Long running program that monitors the text of a directory's files. 
![Directory](https://imgur.com/YtC7fW5.png)

## Overview
An assignment from [Kenzie Academy](https://kenzie.academy). Here are the goals for this program: 

For this assessment you will create your own small long-running program named `dirwatcher.py`.  This will give you experience in structuring a long-running program, which will help you with the SlackTweet project later on. The `dirwatcher.py` program should accept some command line arguments that will instruct it to monitor a given directory for text files that are created within the monitored directory.  Your `dirwatcher.py` program will continually search within all files in the directory for a 'magic' string which is provided as a command line argument.  This can be implemented with a timed polling loop.  If the magic string is found in a file, your program should log a message indicating which file and line number the magic text was found.  Once a magic text occurrence has been logged, it should not be logged again unless it appears in the file as another subsequent line entry later on.

Files in the monitored directory may be added or deleted or appended at any time by other processes.  Your program should log a message when new files appear or other previously watched files disappear.  Assume that files will only be changed by appending to them.  That is, anything that has previously been written to the file will not change.  Only new content will be added to the end of the file.  You don't have to continually re-check sections of a file that you have already checked.

Your program should terminate itself by catching SIGTERM or SIGINT (be sure to log a termination message).  The OS will send a signal event to processes that it wants to terminate from the outside.  Think about when a sys admin wants to shutdown the entire computer for maintenance with a `sudo shutdown` command.  If your process has open file handles, or is writing to disk, or is managing other resources, this is the OS way of telling your program that you need to cleanup, finish any writes in progress, and release resources before shutting down.

NOTE that handling OS signals and polling the directory that is being watched are two separate functions of your program.  You won't be getting an OS signal when files are created or deleted.

## Installation
-Fork and clone from [Github](https://github.com/knmarvel/dirwatcher)

## Available Scripts
```zsh
python dirwatcher.py PI MAGIC -d DIR -e EXT
```

where 
- PI stands for your integer polling interval, measured in seconds
- MAGIC stands for the string you're searching for
- DIR stands for the directory you want to search
- EXT stands for the file extension you want to look for

## Helper functions:
- logger(message): 
    """Sets up log messages for the program"""
- check_for_magic(magic, search_dir, ext):
    """Given a magic string, a directory, and a file type,
    returns a dictionary of all files of the file type in
    the directory that contain the string with the last line
    of the file."""
- check_for_add(new_files):
    """Prints a statement about files added with magic text
    or files with magic text appended at a later line"""
- check_for_deletion(new_files):
    """Logs a delete statement if a file with magic text is deleted."""
- log_difference(new_files):
    """checks dictionary of currently found files against previously
    found files and prints any differences"""
- display_start_banner(interval, magic, search_dir, ext):
    """logs starting banner"""
- display_end_banner(reason):
    """logs ending banner"""
- receive_signal(sig_num, frame):
    """Handler for SIGTERM, SIGQUIT, and SIGINT"""
- create_parser(*args, **kwargs):
    """Defines and provides help for commandline arguments""

## Author
[Kano Marvel](https://github.com/knmarvel)
