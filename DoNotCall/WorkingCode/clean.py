import send2trash
import os

def cleanDatabase():
    # Clean up Read File of duplicates
    f = open("Done/toRead.txt", "r")
    lines = f.readlines()
    f.close()
    if os.path.exists("Done/toRead.txt.old"):
        send2trash.send2trash("Done/toRead.txt.old")
    os.rename("Done/toRead.txt", "Done/toRead.txt.old")
    mySet = set([]) # Get rid of duplicates
    for line in lines:
        mySet.add(line)
    # Write cleaned Readme
    f2 = open("Done/toRead.txt", "w")
    for s in mySet:
        f2.write(s)
    f2.flush()
    f2.close()
    # Get rid of finished folders
    doneJson = os.listdir("Done")
    print(doneJson)
    input()
    for file in doneJson:
        if ".json" in file:
            dateString = file.replace(".json","")
            if os.path.exists("Base/" + file):
                send2trash.send2trash("Base/" + file)
            if os.path.exists("Base/" + dateString):
                send2trash.send2trash("Base/" + dateString)
        else: # Not a json file. Ignore
            continue
    sz = os.path.getsize("Done/2021-02-28.json")

cleanDatabase()
