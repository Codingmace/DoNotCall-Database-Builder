# Compresses the database to csv file
import json
import os

def prepDatabase():
    compsF = open("compare.csv", "w")
    compsF.write("Number,Id,Area\n")
    compsF.flush()
    filename = "goodNumbers.json"
    try:
        with open(filename, "r") as read_file:
            developer = json.load(read_file)
            for x in developer:
                newStr = x['number'] + "," + x['id'] + "," + x['area-code']
                compsF.write(newStr + "\n")
        filename = "badNumbers.json"
        with open(filename, "r") as read_file:
            developer = json.load(read_file)
            for x in developer:
                newStr = x['number'] + "," + x['id'] + "," + x['area-code']
                compsF.write(newStr + "\n")

    except:
        print(filename + " is having an issue")
        compsF.close()
        
    compsF.flush()
    compsF.close()
prepDatabase()
