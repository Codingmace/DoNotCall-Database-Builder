import os
import json
import requests
from datetime import datetime, timedelta, date
import time
import send2trash

# A connection error occured, Add a validator for input
# Need to check that the folders are complete before crushing them
# Could have an issue with removing the folders. check back in a little.
# Need to move it to the Log for printouts
# Add timeout for the request because it is taking too long sometimes
# Missed all the dates in the missed.zip file when creating the database. Also not sure if it was in the toRead File


# Consistant Variables
baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
fileLog = open("log.txt", "a")
waitBetweenRequest = False
waitBetweenFail = False
waitBeforeStart = False
waitBetweenResponse = False



class Node:
    def __init__(self, value, nextNode=None):
        self.id = value['id']
        self.numb = value['number']
        self.area = value['area-code']
        self.good = value['number'][0:3] == value['area-code']
        self.nextNode = nextNode

    def getId(self):
        return self.id

    def getNumb(self):
        return self.numb

    def getArea(self):
        return self.area


def getDay(): # Gets dateTime Y,M,D
    return datetime.today().strftime("%Y-%m-%d")

def getTimeNow(): # Gets DateTime Without msec
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

def validResponse(statusCode):
    if (statusCode == 200):
        if waitBetweenResponse:
            time.sleep(.85) # Don't over request system
        return True
    elif (statusCode == 429):
        print("Rate has been exceeded")
    elif (statusCode == 404):
        print("API server cannot be reached")
    elif (statusCode == 403):
        print("Api key missing or invalid")
    elif (statusCode == 400):
        print("URL Does not use HTTPS:")
    return False

def getResponseMessage(statusCode):
    if (statusCode == 200):
        return "Good"
    elif (statusCode == 429):
        return "Rate has been exceeded"
    elif (statusCode == 404):
        return "API server cannot be reached"
    elif (statusCode == 403):
        return "Api key missing or invalid"
    elif (statusCode == 400):
        return "URL Does not use HTTPS:"
    return False

def dateOffset(date1, date2): # Just year-month-day
    split1 = date1.split("-")
    split2 = date2.split("-")
    f_date = date(int(split1[0]), int(split1[1]), int(split1[2]))
    l_date = date(int(split2[0]), int(split2[1]), int(split2[2]))
    delta = l_date - f_date
    return delta.days

def cleanJson(data):
    del data['meta']
    del data['links']
    for element in data['data']:
        del element['type']
        del element['relationships']
        del element['meta']
        del element['links']
        element['number'] = element['attributes']['company-phone-number']
        element['area-code'] = element['attributes']['consumer-area-code']
        del element['attributes']
    return data

def createFolder(folderpath):
    if os.path.exists(folderpath):
        print(folderpath + " already Exists")
    else:
        fileLog.write("[" + getTimeNow() + "] Creating Dir: " + folderpath + "\n")
        fileLog.flush()
        os.makedirs(folderpath)

def createDatabase(dncApiKey, offset):
    createFolder("Done")
#    print("We are grabbing the days all the way back to February 14, 2020")
    currentDay = datetime.today()
    curDay = open("Done/lastDate.txt", "w") # Last date updated
    curDay.write(getDay())
    curDay.flush()
    curDay.close()
    moreDays = True
    subDays = open("Done/toRead.txt", "a") # For the sub parts
    while moreDays:
        d = currentDay - timedelta(days=offset)
        form = d.strftime("%Y-%m-%d")
        if os.path.exists(str("Base\\" + form+".json")):
            print(form + " already exists")
            offset += 1
            continue # Don't want to recall a file that already exists
        fileLog.write("[" + getTimeNow() + "] Creating Day: " + form + "\n")
        fileLog.flush()
        response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + form + "\"")
        print(response.text)
        if form == "2020-02-14":
            moreDays = False
            continue
        if d.year <= 2020 and d.month <= 1: # Anything before January 2020
            moreDays = False
            continue
        if not validResponse(response.status_code):
            subDays.close()
            fileLog.write("[" + getTimeNow() + "] Quitting at: " + form + "\n")
            fileLog.flush()
            return offset # If done
        data = response.json() # Got successful information
        response.close()
        offset += 1
        recordCount = data['meta']['record-total']
        if recordCount == 0:
            fileLog.write("[" + getTimeNow() + "] Invalid Day: " + form + "\n")
            fileLog.flush()
            continue
        output = open(str("Base\\" +form +".json"), "w")
        leftOver = int(recordCount) % 50
        recordCount += 50 - leftOver # To accomidate for the left over ones
        subDays.write(form + " " + str(recordCount) + "\n")
        # Parse Json
        data = cleanJson(data)

        # Write it all to a file
        json.dump(data, output)
        output.flush()
        output.close()
    subDays.close()
    return -1 # Finished

def initalizeDatabase():
    f = open("DncApiKey.txt" , "r")
    lines = f.readlines()
    f.close()
    offset = 1 # 1 to skip today because that is not published
    if os.path.exists("Done/toRead.txt"): # Read last line to know where left off
        with open('Done/toRead.txt', 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
            currentDay = datetime.today()
            offset = dateOffset(last_line.split(" ")[0], currentDay.strftime("%Y-%m-%d"))
            # Could do without split but just want data neater

    # Add a part to continue where left off in the toRead File
    for line in lines:
        offset = createDatabase(line.strip(),offset)
        createdDatabase = offset == -1
        if not createdDatabase:
            offset += 1
        else:
            return "The Basic database has been successfully created"
    return "Their was an issue and I couldn't finish"

def updateDatabase(dncApiKey):
    todayDate = getDay()
    offset = 0
    if os.path.exists("Done/lastDate.txt"):
        lastDate = open("Done/lastDate.txt", "r") # last update day
        endDate = lastDate.readline().strip()
        fileLog.write("[" + getTimeNow() + "] Starting Date: " + endDate + "\n")
        fileLog.flush()
        offset = dateOffset(endDate , todayDate)
    else:
        timeNow = getTimeNow()
        fileLog.write("[" + timeNow + "] That File does not exists")
        fileLog.write("Solution: Go to the Done folder and create a file named lastDate.txt")
        fileLog.write("In that file put the last update in Year-Month-Day format")
        fileLog.flush()
        fileLog.close() # Need to change this later
        f = open("Done/lastDate.txt", "w")
        f.write(todayDate)
        f.flush()
        f.close()
        return "Could not update. Read Log File for more information"

    moreDays = True
    subDays = open("Done/toRead.txt", "a") # For the sub parts
    
    while moreDays:
        print(offset)
        d = datetime.today() - timedelta(days=offset)
        form = d.strftime("%Y-%m-%d")
        if os.path.exists(str("Base\\" + form+".json")):
            print(form + " already exists")
            offset -= 1
            continue # Don't want to recall a file that already exists
        if offset <= 1: # Last possible day
            moreDays = False
        response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + form + "\"")
        if not validResponse(response.status_code):
            subDays.close()
            fileLog.write("[" + getTimeNow() + "] Response: " + getResponseMessage(response.status_code) +"\n")
            fileLog.flush()
            fileLog.write("[" + getTimeNow() + "] Exiting at: " + form + "\n")
            fileLog.flush()
            return "Please check Log File for more detail" # If done

        # Got successful information
        data = response.json()
        response.close()
        offset -= 1
        recordCount = data['meta']['record-total']
        if recordCount == 0:
            fileLog.write("[" + getTimeNow() + "] Invalid Day: " + form + "\n")
            fileLog.flush()
            continue
        output = open(str("Base\\" +form +".json"), "w")
        leftOver = int(recordCount) % 50
        recordCount += 50 - leftOver # To accomidate for the left over ones
        subDays.write(form + " " + str(recordCount) + "\n")
        # Parse Json
        data = cleanJson(data)

        # Write it all to a file
        json.dump(data, output)
        output.flush()
        output.close()
    
    subDays.close()
    curDay = open("Done/lastDate.txt", "w") # Last date updated
    curDay.write(todayDate)
    curDay.close()
    fileLog.write("[" + getTimeNow() + "] Updating Last Date: " + todayDate + "\n")
    fileLog.write("[" + getTimeNow() + "] Finish Update\n")
    fileLog.flush()
    return "I have made it to the end."


def maximum(fileList):
    numbers = []
    if len(fileList) <= 1: # Might be issue if only 1 file was written
        return 0 # Just rewrite the file
    for name in fileList:
        if "-" in name and ".json" in name:
            name = name.replace(".json", "").split("-")[1]
            numbers.append(int(name))
        else:
            fileLog.write("[" + getTimeNow() + "] Problem File: " + name + "\n")
            print("We have a problem with file " + name)
    return max(numbers)

def richer(dncApiKeys):
    count = 0
    while len(dncApiKeys) > 0:
        subDays = open("Done/toRead.txt", "r") # For the sub parts
        lines = subDays.readlines()
        print(len(lines))
        currentDir = "Base/"
        if len(lines) == 0:
            fileLog.write("[" + getTimeNow() + "] No Update Done\n")
            fileLog.flush()
            return "No new Dates"
#            return "No new dates found. I suggest running Update"
        # Check if the folder exists. Maybe rewrite the file. For now ignoring it
        for line in lines:
            # Check to see if file already exist so I don't waste time
            splits = line.split(" ")
            offsetCount = 0
            currentDir = "Base/" + splits[0]
            if os.path.exists(currentDir): # Check if everything there
                if os.path.exists(currentDir + "/" + splits[1] +".json"): # Last file exists
                    fileLog.write("[" + getTimeNow() + "] Skipping Done: " + splits[1] + "\n")
                    fileLog.flush()
                    continue
                else: # Continue where left off
                    fileLog.write("[" + getTimeNow() + "] Continue Day: " + splits[0] + "\n")
                    subFiles = os.listdir(currentDir)
                    offsetCount = maximum(subFiles)
            else:
                fileLog.write("[" + getTimeNow() + "] Creating Folder: " + currentDir + "\n")
                fileLog.flush()
                os.makedirs(currentDir)
            lastEntry = int(splits[1])
            while (offsetCount < lastEntry):
                if len(dncApiKeys) == 0:
                    return "Did not finish. Please ReRun"
                curIndex = count % len(dncApiKeys)
                dncApiKey = dncApiKeys[curIndex].strip()
                count += 1
                response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + splits[0] + "\"&offset=" + str(offsetCount))
                if waitBetweenRequest:
                    time.sleep(1)
                if not validResponse(response.status_code):
                    if waitBetweenFail:
                        time.sleep(120)
                    print(dncApiKeys)
                    print(dncApiKey)
                    try:
                        dncApiKeys.remove(dncApiKey)
                    except:
                        fileLog.write("[" + getTimeNow() + "] Something Went Wrong\n")
                    fileLog.write("[" + getTimeNow() + "] Removed Key: " + dncApiKey + "\n")
                    fileLog.write("[" + getTimeNow() + "] Keys Left: " + str(len(dncApiKeys)) + "\n")
                    fileLog.flush()
                    continue
                data = response.json()
                response.close()
                data = cleanJson(data)
                output = open(currentDir + "/" + str(offsetCount) + "-" + str(offsetCount + 50) + ".json", "w")
                json.dump(data, output)
                output.flush()
                output.close()
                offsetCount += 50
            fileLog.write("[" + getTimeNow() + "] Finished With: " + splits[0] + "\n")
            fileLog.flush()
        return "Awesome. It actually finished"

def FullDayData():
    f = open("DncApiKey.txt" , "r")
    lisp = f.readlines()
    lines= []
    for line in lisp:
        lines.append(line.strip())
    lx = lines
    richer(lx) #Is deleting permentantly so loop is useless.
    return "Done"

def clean(phoneNumber):
    # I could have just done non digits. Wow
    phoneNumber = phoneNumber.replace("+", "").replace("-","").replace("(","").replace(")","")
    if len(phoneNumber) == 10:
        return str(phoneNumber)
    elif len(phoneNumber) == 7:
        return "area missing"
    elif len(phoneNumber) < 10:
        return "too short"
    else: # Could potentially be a double hit on a number
        return "too long"

def crusher(foldername):
    print("Merging the files in the folder name")
    fullpath = "Base/" + foldername
    ar = os.listdir(fullpath)
    print(ar)
    dex = []
    for a in ar: # All the files merging
        try:
            with open(("Base\\" + foldername + "\\" + a), "r") as read_file:
                developer = json.load(read_file)
                for x in developer['data']:
                    number = clean(x['number'])
                    if number == "too short" or number == "too long":
                        continue
                    elif number == "area missing":
                        x['number'] = x['area-code'] + number
                    dex.append(x)
                    
        except:
            return "Leaving the file alone because an issue occured"
            
    # Turning dict to file
    with open("Done/" + foldername + ".json", 'w') as fp:
        json.dump(dex,fp)
    fileLog.write("[" + getTimeNow() + "] Merged: " + foldername + "\n")
    fileLog.flush()
                    
    return "Successfully merged the file"

def crushDatabase():
    folders = os.listdir("Base/") # For extra verification we can verify all entries are there.
    for foldname in folders:
        if os.path.isdir("Base/" + foldname):
            crusher(foldname)
        else:
            continue # It is a file so ignore


def dupCleanDatabase():
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
    
    # Get rid of finished folders
    doneJson = os.listdir("Done")
    for file in doneJson:
        fileLog.write("[" + getTimeNow() + "] Removing: " + file + "\n")
        fileLog.flush()
        if ".json" in file:
            dateString = file.replace(".json","")
            if os.path.exists("Base/" + file):
                send2trash.send2trash("Base/" + file)
            if os.path.exists("Base/" + dateString):
                send2trash.send2trash("Base/" + dateString)
        else: # Not a json file. Ignore
            continue

    myNewList = donCleanDatabase(mySet)
    # Write cleaned Readme
    f2 = open("Done/toRead.txt", "w")
    for s in myNewList:
        f2.write(s)
    f2.flush()
    f2.close()


def donCleanDatabase(mySet): # Removing the done in toReadFile
    createFolder("Done/Completed")
    oq = os.listdir("Done/")
    removeList = []
    lines = []
    for m in mySet:
        lines.append(m)
    for i in oq:
        if "json" not in i: # Remove non Json Files
            oq.remove(i)
        else:
            os.rename("Done/" + i, "Done/Completed/" + i)
            fileLog.write("[" + getTimeNow() + "] Done: " + i + "\n")
            fileLog.flush()        
            removeList.append(i.replace(".json",""))
            
    for a in removeList:
        for line in lines:
            if a == line.split(" ")[0]:
                lines.remove(line)
                fileLog.write("[" + getTimeNow() + "] Removed: " + a + "\n")
                fileLog.flush()
    return lines

def rebase():
    baseDir = "Done/Completed/"
    mergeFiles = os.listdir(baseDir)
    goodNumbers = [] # Good number dict
    badNumbers = [] # Bad number dict
    goodNumb = [] # Same area code
    badNumb = [] # Different Area Code
    for fi in mergeFiles: # Load Numbers
        try:
            with open(baseDir + fi, "r") as read_file:
                developer = json.load(read_file)
                for x in developer:
                    n = Node(x)
                   # print("this")
                    if n.good:
                        goodNumbers.append(x) # Technically can delete area-code
                        goodNumb.append(n)
                    else:
                        badNumbers.append(x)
                        badNumb.append(n)
        except:
            fileLog.write("[" + getTimeNow() + "] File Issue: " + fi + "\n")
            fileLog.flush()
    # Go through the numbers and sort
    print(str(len(goodNumb)))
    print(str(len(badNumb)))
    # Turning dict to file
    with open('badNumbers.json', 'w') as fp:
        json.dump(badNumbers, fp)

    with open('goodNumbers.json', 'w') as fp:
        json.dump(goodNumbers, fp)

def main():
    print("Welcome to the Do Not Call Database Builder")
    running = True
    while running:
        print("Here is what we can do")
        print("1. Create a database")
        print("2. Update Database")
        print("3. More data in database")
        print("4. Clean Database")
        print("5. Crush Database")
        print("6. Mega Good-Bad Build")
        print("7. Quit")
        selection = 3
        try:
            if waitBeforeStart:
                time.sleep(600)
            selection = int(input("What are we doing: "))
        except:
            print("That doesn't seem to be an int")
        if selection == 1:
            print("Creating the database")
            fileLog.write("[" + getTimeNow()+"] Selection: Create Database\n")
            fileLog.flush()
            print(initalizeDatabase())
        elif selection == 2:
            print("Updating the database")
            fileLog.write("[" + getTimeNow() + "] Selection: Update Database\n")
            fileLog.flush()
            f = open("DncApiKey.txt" , "r")
            line = f.readline() # only read one key
            f.close()
            print(updateDatabase(line.strip()))
        elif selection == 3:
            print("Adding more data")
            fileLog.write("[" + getTimeNow() + "] Selection: Enrich Database\n")
            fileLog.flush()
            print(FullDayData())
        elif selection == 4:
            print("Cleaning Database")
            fileLog.write("[" + getTimeNow() + "] Selection: Clean Database\n")
            fileLog.flush()
            dupCleanDatabase() # Duplicates in toRead file
        elif selection == 5:
            print("Crushing Database")
            fileLog.write("[" + getTimeNow() + "] Selection: Update Database\n")
            fileLog.flush()
            crushDatabase()
        elif selection == 6:
            print("Merging all done files")
            fileLog.write("[" + getTimeNow() + "] Selection: Mega Crush")
            fileLog.flush()
            rebase()
        elif selection == 7:
            print("Quitting")
            fileLog.write("[" + getTimeNow() + "] Selection: Exit\n")
            fileLog.flush()
            fileLog.close()
            running = False
        else:
            fileLog.write("[" + getTimeNow() + "] Selection: Invalid\n")
            fileLog.flush()
            print("That is not an option")


main()
