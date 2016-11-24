#!/usr/bin/python3

# by John Kennedy

import boto.ec2
import time
import logs
import os
import subprocess


# Simple menu to start the new instance.

def menu():
    subprocess.run(["clear"], shell=True)
    logs.ec2('''
***********************************************
                   MENU
    Please choose one of the following:
***********************************************
    1: Launch new instance
    2: exit
''')

    options = ["1", "2"]
    ans = (input(">> "))

    if ans == "1":
        logs.ec2("OK")
        logs.ec2.debug("starting new_instance()")
        key_name()

    elif ans == "2":
        logs.ec2("GoodBye")
        exit()

    else:
        logs.wrong()
        menu()



# Function used to get the key name &
# to find the key in the current directory.

def key_name():
    logs.ec2("Is your key in this directory? [Y/N]")
    options = ["y", "n"]
    ans = (input(">> "))

    if ans == "y":
        logs.ec2("Press enter the name of your key & do not include .pem extension")
        global key # global is used for the object to be seen in other functions
        key = input('>> ')
        while key == "":  # Loop until until user types an answer.
            key = input('>> ')

        if os.path.exists(key + ".pem"):
            logs.ec2.info("key found")
            logs.ec2.debug("keyname is " + key)
            region()

        else:
            logs.ec2.warn("Your KEY is NOT in YOUR current directory, Please put key in Current directory NOW")
            logs.wrong()
            key_name()

    elif ans == "n":
        logs.ec2.warn("Please place your key in your current directory to continue")
        key_name()

    else:
        logs.wrong()# Will print "Please try again" & will reprint the function again.
        key_name()



# Function for the user to state which region they use on AWS

def region():
    logs.ec2('''
Please state your region
    1. us-west-2"
    2. eu-west-1
    ''')
    options = ["1", "2"]
    ans = (input(">> "))
    global region
    global conn

    if ans == "1":
        logs.ec2("OK")
        region = "us-west-2"
        logs.ec2.debug("using " + region + " as the region")
        conn = boto.ec2.connect_to_region(region)
        security_group()

    elif ans == "2":
        logs.ec2("OK")
        region = "eu-west-1"
        logs.ec2.debug("using " + region + " as the region")
        conn = boto.ec2.connect_to_region(region)
        security_group()

    else:
        logs.wrong()
        region()



# Function to declare new or existing security group for new instance

def security_group():
    logs.ec2('''
Please choose the following:
    1: Choose an existing security group.
    2: Create a new security group.
''')
    options = ["1", "2"]
    ans = (input(">> "))
    global sec

    if ans == "1":
        logs.ec2("State the name of the security group")
        sec=input(">> ")
        while sec == "":
            sec=input(">> ")
        logs.ec2.debug("security group is " + sec)
        tag_name()

    elif ans == "2":
        logs.ec2("State the name of the security group")
        sec = input(">> ")
        secgroup = conn.create_security_group(sec, 'Only HTTP and SSH')
        secgroup.authorize('tcp', 80, 80, '0.0.0.0/0')  # HTTP
        secgroup.authorize('tcp', 22, 22, '0.0.0.0/0')  # SSH
        logs.ec2.debug("security group is " + sec)
        tag_name()

    else:
        logs.wrong()
        security_group()



# Function used to enter a tagname for new instance

def tag_name():
    logs.ec2("Please state your tag name")
    global tag
    tag=input('>> ')
    while tag == "":  # Loop until it is a blank line
        tag = input('>> ')
    logs.ec2("OK")
    logs.ec2.debug("Tag Name is: " + tag)
    logs.ec2.debug("Tag Name is: " + tag)
    new_instance()



# Function used to create the new instance

def new_instance():
    logs.ec2("Creating a new instance!!!")
    time.sleep(5)
    logs.ec2.debug("using " + region + " as the region")
    conn = boto.ec2.connect_to_region(region)
    reservation = conn.run_instances('ami-b04e92d0', key_name=key, instance_type='t2.micro', security_groups=[sec])
    print("tagging your instance now")
    time.sleep(5)
    global instance
    instance = reservation.instances[0]
    instance.add_tag('Name', tag)
    logs.ec2.debug("waiting for instance")
    while instance.update() != "running":
        time.sleep(6)
        instance.update()
    print("Instance Running")
    connect_instance(key, instance)



# Function to ask the user if they want to copy the check_webserver.py script to the
# new instance and execute it.

def connect_instance(key_name, instance):
    logs.ec2("Do you want to copy & run check_webserver.py script? [Y/N]")
    options = ["y", "n"]
    ans = (input(">> "))

    if ans == "y":
        logs.ec2("OK copying check_webserver.py now")
        logs.ec2("please ensure check_webserver.py & logs.py are in this directory")
        dns = instance.public_dns_name
        time.sleep(45)# Provide sufficient time to ensure the ssh is ready on the new instance

        logs.ec2.debug("Copying check_webserver")
        x = subprocess.run(
            ["scp -o  StrictHostKeyChecking=no -i" + key_name + ".pem check_webserver.py ec2-user@" + dns + ":."],
            shell=True, stdout=subprocess.DEVNULL)

        logs.ec2.info("copied check_webserver successfully")# scp statement used to copy check_webserver.py to the new instance
        while x.returncode != 0:
            print(x.returncode) # if the scp was not successful, it will try again until the returncode = 0
            time.sleep(8)

        logs.ec2.debug("Copying logs.py")
        y = subprocess.run(
            ["scp -o  StrictHostKeyChecking=no -i" + key_name + ".pem logs.py ec2-user@" + dns + ":."],
            shell=True, stdout=subprocess.DEVNULL)

        logs.ec2.info("copied logs.py successfully")
        while y.returncode != 0:
            print(y.returncode)
            time.sleep(8)

        logs.ec2.debug("Installing Python")
        z = subprocess.run(
            ["ssh -t -o  StrictHostKeyChecking=no -i" + key_name + ".pem ec2-user@" + dns + " " + 'sudo yum -y install python35'],
            shell=True, stdout=subprocess.DEVNULL) # this ssh statement is used

        logs.ec2.info("installed python successfully")
        while z.returncode != 0:
            print(z.returncode)
            time.sleep(8)

        logs.ec2("Running check_webserver.py now")
        time.sleep(3)
        cmd = subprocess.run(
            ["ssh -i" + key_name + ".pem ec2-user@" + dns + ' ./check_webserver.py'],
            shell=True)
        terminate_instance()
        while cmd.returncode != 0:
            print(cmd.returncode)
            time.sleep(8)

    elif ans == "n":
        logs.ec2("OK")
        terminate_instance()

    else:
        logs.wrong()
        connect_instance(key_name, instance)



# Function to state whether to terminate/stop the new instance

def terminate_instance():
    logs.ec2('''
With your new instance Do you want to:
    1: Terminate your instance
    2: Stop your instance
    3: Return to the main menu
    ''')
    options = ["1", "2", "3"]
    ans = (input(">> "))

    if ans == "1":
        logs.ec2("Terminating instance now")
        instance.terminate()
        instance.update()
        menu()

    elif ans == "2":
        logs.ec2("Stopping instance now")
        instance.stop()
        instance.update()
        menu()

    elif ans== "3":
        logs.ec2("Returning to main menu")
        menu()

    else:
        logs.wrong()
        terminate_instance()



# main function to run all other functions

def main():
    menu()
    key()
    region()
    security_group()
    new_instance()
    connect_instance()
    terminate_instance()


if __name__ == '__main__':
    main()
