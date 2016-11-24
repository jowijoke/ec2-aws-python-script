#!/usr/bin/python3
import logging
import time
import subprocess

# set up logging to a file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', # display time, log level and message formot for log file
                    datefmt='%m-%d %H:%M',
                    filename='ec2.log',# name of log file
                    filemode='w')# this ensures the log file is no longer appended to, so the messages from earlier runs are lost.

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# setting a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s: %(message)s')

# telling the handler to use this format
console.setFormatter(formatter)

# adding the handler to the root logger
logging.getLogger('').addHandler(console)



def wrong():
    print("please try again")# simple function to reduce repetition. Used when a user types the wrong input
    time.sleep(2)
    subprocess.run(["clear"], shell=True) # bash command to clear the screen.



class ec2:

    def __init__(self, msg):
        print(msg)# default constructor to print the message but not stored in the log file

    def info(self):
        logging.info(self)# Display to ec2.log file & console.

    def warn(self):
        logging.warning(self)

    def debug(self):
        logging.debug(self)# any msg labeled debug won't be displayed on the console but will be recorded for the ec2.log file.
