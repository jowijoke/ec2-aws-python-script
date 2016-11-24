#!/usr/bin/python3

# By John Kennedy

import subprocess
import time
import logs

# Function used to update the EC2 instance

def update_instance():
    logs.ec2("Would you like to update your instance? [Y/N]")
    options = ["y", "n"]
    ans = (input(">> "))

    if ans == "y":
        logs.ec2("ok")
        logs.ec2.debug("updating EC2 instance now")
        update= subprocess.run(["sudo yum -y update"], shell=True, stdout=subprocess.DEVNULL)# subprocess used to send bash command to instance
        y= update.returncode

        if y == 0:
            logs.ec2.info("updated successfully")
            time.sleep(3)
            check_nginx()
        else:
            logs.ec2.info("nothing to update")

    elif ans == "n":
        logs.ec2("OK")
        check_nginx()

    else:
        logs.wrong()
        update_instance()



# Function used to check if nginx is running & if not it will attempt to run it.

def check_nginx():
    logs.ec2.debug("Checking if ngnix is running")
    cmd = subprocess.run(["ps -A | grep nginx | grep -v grep"], shell=True, stdout=subprocess.DEVNULL)# directinng any linux output that isn't needed to DEVNULL.
    # shell = true, helps place one whole linux command using one string. Also allows one to access the shell.
    x = cmd.returncode

    if x == 0: # this linux responce is returned by the 'returncode' command & will return 0 if successful or 1 if not succesful
        logs.ec2.info("nginx is RUNNING")
        time.sleep(3)
        check_mysql()

    else:
        logs.ec2.warn("nginx is NOT RUNNING")
        logs.ec2.warn("Attempting to run nginx now")
        start=subprocess.run(["sudo service nginx start"], shell=True, stdout=subprocess.DEVNULL)# Attempting to start nginx if it's installed
        y=start.returncode

        if y == 1:
            logs.ec2.warn("unable to start nginx")
            time.sleep(3)
            install_nginx()

        elif y==0:
            check_nginx()



# Function to ask whether to install nginx on the instance

def install_nginx():
    logs.ec2("Do you want to install nginx [Y/N]")
    options = ["y", "n"]
    ans = (input(">> "))

    if ans == "y":
        logs.ec2.debug("installing nginx")
        install1 = subprocess.run(["sudo yum -y install nginx"], shell=True, stdout=subprocess.DEVNULL)
        check_nginx() # Once installed the check_nginx function is recalled to run nginx

    elif ans == "n":
        logs.ec2("OK")
        logs.ec2.debug("not installing nginx")
        time.sleep(3)
        check_mysql()

    else:
       logs.wrong()
       install_nginx()



# Function to check mysql is running

def check_mysql():
    logs.ec2.debug("Checking if mysql is running")
    cmd = subprocess.run(["ps -A | grep mysqld | grep -v grep"], shell=True, stdout=subprocess.DEVNULL)
    x = cmd.returncode

    if x == 0: # this linux responce is returned by the 'returncode' command & will return 0 if successful or 1 if not succesful
        logs.ec2.info("mysql is RUNNING")
        time.sleep(3)
        webserver_stat()

    else:
        logs.ec2.warn("mysql is NOT RUNNING")
        logs.ec2.warn("Attempting to run mysql now")
        time.sleep(3)
        start=subprocess.run(["sudo service mysqld start"], shell=True, stdout=subprocess.DEVNULL)
        y=start.returncode

        if y == 1:
            logs.ec2.warn("unable to start mysql.")
            time.sleep(3)
            install_mysql()

        elif y == 0:
            check_mysql()



# Function to install mysql

def install_mysql():
    logs.ec2("Do you want to install mysql? [Y/N]")
    options = ["y", "n"]
    ans = (input(">> "))

    if ans == "y":
        logs.ec2.debug("installing mysql")
        install1 = subprocess.run(["sudo yum -y install mysql-server"], shell=True, stdout=subprocess.DEVNULL)
        check_mysql() # once mysql is installed, check_mysql function is executed again to run mysql

    elif ans == "n":
        logs.ec2("OK")
        logs.ec2.debug("not installing mysql")
        webserver_stat()
        time.sleep(3)

    else:
        logs.wrong()
        install_mysql()



# Menu displayed to show monitoring info about the instance

def webserver_stat():
    logs.ec2('''
*******************************
        EC2  Monitor
*******************************
    Press 1 for vmstat
    Press 2 for netstat
    Press 3 for ps
    Press 4 to exit
*******************************
''')

    options = ["1", "2", "3", "0"]
    ans = (input(">> "))

    if ans == "1":
        vmstat = subprocess.run(["vmstat"])
        webserver_stat()

    elif ans == "2":
        netstat = subprocess.run("netstat")
        webserver_stat()

    elif ans == "3":
        ps = subprocess.run("ps")
        webserver_stat()

    elif ans == "4":
        logs.ec2("GoodBye")
        exit()

    else:
        logs.wrong()
        webserver_stat()



def main():
    update_instance()
    check_nginx()
    install_nginx()
    check_mysql()
    install_mysql()
    webserver_stat()

if __name__ == '__main__':
    main()

