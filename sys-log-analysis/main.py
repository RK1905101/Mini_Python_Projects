import os
import re
import sys
import operator
import csv

error_counter = {}
error_user = {}
info_user = {}


# This function will read each line of the syslog.log file and check if it is an error or an info message.
def search_file():
    with open('data/syslog.log', "r") as myfile:
        for line in myfile:
            if " ERROR " in line:
                find_error(line)
                add_user_list(line, 1)
            elif " INFO " in line:
                add_user_list(line, 2)
    return


# If it is an error it will read the error from the line and increment into the dictionary
def find_error(str):
    match = re.search(r"(ERROR [\w \[]*) ", str)
    if match is not None:
        aux = match.group(0).replace("ERROR ", "").strip()
        if aux == "Ticket":
            aux = "Ticket doesn't exist"
        if not aux in error_counter:
            error_counter[aux] = 1
        else:
            error_counter[aux] += 1
    return


# This whill read the user from the string and add to the error or the info counter depending on the op number
def add_user_list(str, op):
    match = re.search(r'\(.*?\)', str)
    user = match.group(0)
    userA = user.strip("()")
    if op == 1:
        if not userA in error_user:
            error_user[userA] = 1
        else:
            error_user[userA] += 1
    elif op == 2:
        if not userA in info_user:
            info_user[userA] = 1
        else:
            info_user[userA] += 1
    return


# This function will read the list, arrange it and return a tuple with the dictionary items
def sort_list(op, list):
    if op == 1:
        s = sorted(list.items(), key=operator.itemgetter(1), reverse=True)
    elif op == 2:
        s = sorted(list.items(), key=operator.itemgetter(0))
    return s


# This is an extra function which will read the value of a user in the error dictionary and return its value if key exists
def getErrValue(keyV):
    for key, value in error_user:
        if key is keyV:
            return value
    return 0


# This function writes both csv files
def write_csv(op):
    if op == 1:
        with open('data/user_statistics.csv', 'w', newline='') as output:
            fieldnames = ['Username', 'INFO', 'ERROR']
            csvw = csv.DictWriter(output, fieldnames=fieldnames)
            csvw.writeheader()
            for key, value in info_user:
                valError = getErrValue(key)
                csvw.writerow({'Username': key, 'INFO': value, 'ERROR': valError})
    if op == 2:
        with open('data/error_message.csv', 'w', newline='') as output:
            fieldnames = ['Error', 'Count']
            csvw = csv.DictWriter(output, fieldnames=fieldnames)
            csvw.writeheader()
            for key, value in error_counter:
                csvw.writerow({'Error': key, 'Count': value})
    return


# This function adds zero to the other dictionary in case that user is not a key, it will add a key with the user and value 0
def add_zeros():
    for user in error_user.keys():
        if user not in info_user:
            info_user[user] = 0
    for user in info_user.keys():
        if user not in error_user:
            error_user[user] = 0
    return


# This will execute the functions
search_file()
add_zeros()
error_counter = sort_list(1, error_counter)
error_user = sort_list(2, error_user)
info_user = sort_list(2, info_user)
write_csv(1)
write_csv(2)
