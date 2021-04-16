# Compresses the database to csv file
import json
import os

def searchNumber():
    phoneNumber = "000-000-0000"
    done = False
    allNumbers = []
    compsF = open("compare.csv", "w")
    compsF.write("Number,Id,Area\n")
    compsF.flush()
    filename = "goodNumbers.json"
    try:
        with open(filename, "r") as read_file:
            developer = json.load(read_file)
            for x in developer:
                allNumbers.append(x)
                newStr = x['number'] + "," + x['id'] + "," + x['area-code']
                compsF.write(newStr + "\n")
        filename = "badNumbers.json"
        with open(filename, "r") as read_file:
            developer = json.load(read_file)
            for x in developer:
                allNumbers.append(x)
                newStr = x['number'] + "," + x['id'] + "," + x['area-code']
                compsF.write(newStr + "\n")

    except:
        print(filename + " is having an issue")
        compsF.close()
        
    compsF.flush()
    compsF.close()

    print("Loaded ", str(len(allNumbers)) + " entries")
    input()
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
