# Get all the information on the database about a phone number.
import json
import os
# Improvement
# Sort numbers before search (Quick already)
# Create a database of numbers linked to multiple ID's


def searchNumber():
    phoneNumber = "000-000-0000"
    done = False
    allNumbers = []
    filename = "result.json"
#    searchAll = input("Would you like to search bad Database (Y/N)? ")
    searchAll= "N"
    if searchAll == "Y" or searchAll == "y":
        print("Ok loading up all numbers")
    elif searchAll == "N" or searchAll == "n":
        print("Ok just good numbers. Awesome")
        filename = "goodNumbers.json"
    else:
        print("That is not valid. I guess I will do everything")

    if os.path.exists(filename):
        print("Reading in " + filename)
    else:
        print("That file doesn't work. Verifying files")
        if os.path.exists("result.json"):
            print("combine file exists")
        else:
            print("combine file doesn't exists")
        if os.path.exists("goodNumbers.json"):
            print("good file exists")
        else:
            print("good file doesn't exist")
        if os.path.exists("badNumbers.json"):
            print("bad files exists")
        else:
            print("bad files doesn't exists")
        if os.path.exists("goodNumbers.json") and os.path.exists("badNumbers.json"):
            print("Combining files to hopefully solve the issue")
            # Here combine the files
            # For now making it just good file because I am lazy and want to test it.
            filename = "goodNumbers.json"

    try:
        with open(filename, "r") as read_file:
            developer = json.load(read_file)
            for x in developer:
                allNumbers.append(x)
    except:
        print("the file is having an issue ")

    print("Loaded ", str(len(allNumbers)) + " entries")
    
    while (not done):
        phoneNumber = input("Enter Phone Number (q to quit, h for help): ")
        phoneNumber = phoneNumber.replace("+", "").replace("-","").replace("(","").replace(")","")
        if phoneNumber == "q":
            print("Ok now we quit")
            done = True
            continue
        elif phoneNumber == "h":
            print("Here would go help but I have not done it yet")
            continue
        if len(phoneNumber) == 10:
            print("That is a valid phone number. Searching for it now")
            idList = []
            for e in allNumbers:
#                print(e)
                if e['number'] == phoneNumber:
                    idList.append(e)
                
            print("Found " + str(len(idList)) + " entries for the number "+ phoneNumber)
            if len(idList) > 0:
                extended = input("Would you like all the information (Y/N)? ")
                if extended.lower() == "y":
                    print("Ok printing out " + str(len(idList)) + " entries")
    
                    print("##############################")
                    print("HERE I WOULD GET VALUE BASED ON ID")
                    print("I HAVE NOT TESTED FULLY SO NOT IMPLEMENTED")
                    print("####################################################\n")
                
                elif extended.lower() == "n":
                    print("Ok I think my work here is done then")
                else:
                    print("Well that isn't an option. So I guess I am done")
        else:
            print("That is an invalid phone number. Try again")
            



searchNumber()
