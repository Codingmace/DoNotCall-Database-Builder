# Get all the information on the database about a phone number.
# import json
import os
# Improvement
# Sort numbers before search (Quick already)
# Create a database of numbers linked to multiple ID's


def searchNumber():
    phoneNumber = "000-000-0000"
    done = False
    allNumbers = []
    filename = "compare.csv"
    searchAll= "Y" # Including bad numbers; Implement later on

    if os.path.exists(filename):
        print("Reading in " + filename)
    else:
        print("That file doesn't exist. Check and run the function again")
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
            # Call prep database here
    listNumbers = []
    dupCount = 0
    with open(filename , "r") as read_file:
        lines = read_file.readlines()
        lines.remove(lines[0]) # Remove the header
        for line in lines:
            splits = line.strip().split(",")
            listNumbers.append(line)
            allNumbers.append(splits)
#            if(splits[0] == "7179833229"):
#                print(line)
#            if splits[2] == "717":
#                if line not in listNumbers:
#                    listNumbers.append(line)
#                    allNumbers.append(splits)
#                    if len(listNumbers) % 1000 == 0:
#                        print("Lengthe of list" ,  len(listNumbers))
#                else:
#                    dupCount += 1
#                    print("Dup", dupCount,"listSize", len(listNumbers))
            
    print("Loaded ", str(len(listNumbers)) + " entries")
    print("Duplicate Count", str(dupCount))
    
    while (not done):
        phoneNumber = "7179833229"
        done = True
#        phoneNumber = input("Enter Phone Number (q to quit, h for help): ")
        phoneNumber = phoneNumber.replace("+", "").replace("-","").replace("(","").replace(")","")
        if phoneNumber == "q":
            print("Ok now we quit")
            done = True
            continue
        elif phoneNumber == "h":
            print("Here would go help but I have not done it yet")
            print("Well you enter a number and it will search for it.")
            print("If one is found then it will ask to display the records.")
            print("If not then it is not found for 2 reasons.")
            print("1. It is not spam or been reported as spam")
            print("2. The database is outdated.")
            continue
        if len(phoneNumber) == 10:
            print("That is a valid phone number. Searching for it now")
            idList = []
            for e in allNumbers:
                if e[0] == phoneNumber:
                    if e[1] in idList: # Faster to find duplicates here
                        print("Shit something went wrong")
                    else:
                        idList.append(e[1])

# Verify for duplicates here
            if len(idList) == 0:
                print("The number " + phoneNumber + " had no results found")
                continue
            if len(idList) > 0:
                print("Found " + str(len(idList)) + " entries for the number "+ phoneNumber)
                extendedInfo = "Y"
                
                extended = input("Would you like all the information (Y/N)? ")
                if extended.lower() == "y":
                    for i in idList:
                        print("Id 1: " + i)
                        print("Write request here. Very easy")
                        print("Print out the request")
                elif extended.lower() == "n":
                    print("Ok I think my work here is done then")
                else:
                    print("Well that isn't an option. So I guess I am done")
        else:
            print("That is an invalid phone number. Try again")
            



searchNumber()
