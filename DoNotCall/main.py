import os
import json
import requests
from datetime import datetime, timedelta, date
import time
import send2trash

# A connection error occured, Add a validator for input
# Need to check that the folders are complete before crushing them
# Update richer for multiple keys
# Could have an issue with removing the folders. check back in a little.
# Need to move it to the Log for printouts

# Consistant Variables
baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="

def validResponse(statusCode):
    if (statusCode == 200):
#        time.sleep(.65) # So we don't overrequest from the system
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
        os.makedirs(folderpath)

def createDatabase(dncApiKey, offset):
#    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
    createFolder("Done")
    print("We are grabbing the days all the way back to February 14, 2020")
    currentDay = datetime.today()
    curDay = open("Done/lastDate.txt", "w") # Last date updated
    curDay.write(currentDay.strftime("%Y-%m-%d"))
    curDay.flush()
    curDay.close()
    moreDays = True
    subDays = open("Done/toRead.txt", "a") # For the sub parts
    while moreDays:
        d = currentDay - timedelta(days=offset)
        form = d.strftime("%Y-%m-%d")
        print(form)
        if os.path.exists(str("Base\\" + form+".json")):
            print(form + " already exists")
            offset += 1
            continue # Don't want to recall a file that already exists
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
            print("Exiting at " + form)
            return offset # If done
        # Got successful information
        data = response.json()
        response.close()
        offset += 1
        recordCount = data['meta']['record-total']
        if recordCount == 0:
            print("The day " + form + " is invalid but still recorded.")
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
        # Probably wait a little time and write where stopped
#        input("Press any key to exit: ")
    return "Their was an issue and I couldn't finish"

def updateDatabase(dncApiKey):
#    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
    todayDate = datetime.today().strftime("%Y-%m-%d")
    offset =0
    if os.path.exists("Done/lastDate.txt"):
        lastDate = open("Done/lastDate.txt", "r") # last update day
        endDate = lastDate.readline().strip()
        print("The last day the database was updated was " + endDate)
        offset = dateOffset(endDate , todayDate)

    else:
        fileLog = open("log.txt", "a")
        timeNow = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        fileLog.write(timeNow + " That File does not exists")
        fileLog.write("Solution:\nGo to the Done folder and create a file named lastDate.txt")
        fileLog.write("In that file put the last update in Year-Month-Day format")
        fileLog.flush()
        fileLog.close()
        f = open("Done/lastDate.txt", "w")
        f.write(todayDate)
        f.flush()
        f.close()
        return "Could not update. Read Log File for more information"

    moreDays = True
    subDays = open("Done/toRead.txt", "a") # For the sub parts
    
    while moreDays:
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
            print("Exiting at " + form)
#            ("Add to the log file information about where left off
            return "Please check Log File for more detail" # If done

        # Got successful information
        data = response.json()
        response.close()
        offset -= 1
        recordCount = data['meta']['record-total']
        if recordCount == 0:
            print("the day is invalid but still recorded. Skip")
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

    print("Rewritting the lastDate file as we are up to date")
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
            print("We have a problem with file " + name)
            input()
    return max(numbers)

def richer(dncApiKeys):
    count= 0
    while len(dncApiKeys) > 0:
        print("Does the enrichment of the data")
        baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
        subDays = open("Done/toRead.txt", "r") # For the sub parts
        lines = subDays.readlines()
        currentDir = "Base/"
        # Check if the folder exists. Maybe rewrite the file. For now ignoring it
        for line in lines:
            # Check to see if file already exist so I don't waste time
            splits = line.split(" ")
            offsetCount = 0
            currentDir = "Base/" + splits[0]
            if os.path.exists(currentDir): # Check if everything there
                if os.path.exists(currentDir + "/" + splits[1] +".json"): # Last file exists
                    print("Skip this folder because it is already done")
                    continue
                else: # Continue where left off
                    print("Continue at the biggest number file in that folder")
                    subFiles = os.listdir(currentDir)
                    offsetCount = maximum(subFiles)
            else:
                print("It doesn't exist so creating it myself")
                os.makedirs(currentDir)
            lastEntry = int(splits[1])
            while (offsetCount < lastEntry):
                if len(dncApiKeys) == 0:
                    return "Did not finish. Please ReRun"
                curIndex = count % len(dncApiKeys)
                dncApiKey = dncApiKeys[curIndex].strip()
                count += 1
                response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + splits[0] + "\"&offset=" + str(offsetCount))
                #time.sleep(1)
                if not validResponse(response.status_code):
                    time.sleep(240)
                    print(dncApiKeys)
                    print(dncApiKey)
                    try:
                        dncApiKeys.remove(dncApiKey)
                    except:
                        try:
                            dncApiKeys.remove(curIndex)
                        except:
                            print("That fucked up")
                            return "This fucked up"
                    print("Removed Key " + dncApiKey + ". " + str(len(dncApiKeys))+" keys left")
                    continue
#                    return "Did not finish. Please Rerun"
                data = response.json()
                response.close()
                data = cleanJson(data)
                output = open(currentDir + "/" + str(offsetCount) + "-" + str(offsetCount + 50) + ".json", "w")
                json.dump(data, output)
                output.flush()
                output.close()
                offsetCount += 50
            print("Finished with " + splits[0])
        return "Awesome. It actually finished"

def FullDayData():
    f = open("DncApiKey.txt" , "r")
    lisp = f.readlines()
    lines= []
    for line in lisp:
        lines.append(line.strip())
    for i in range(0, 10):
        lx = lines
        richer(lx) #Is deleting permentantly so loop is useless.
#        time.sleep(60)
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
                        print(x)
                        continue
                    elif number == "area missing":
                        x['number'] = x['area-code'] + number
                    dex.append(x)
                    
        except:
            return "Leaving the file alone because an issue occured"
            
    # Turning dict to file
    with open("Done/" + foldername + ".json", 'w') as fp:
        json.dump(dex,fp)
    
    return "Successfully merged the file"

def crushDatabase():
    folders = os.listdir("Base/") # For extra verification we can verify all entries are there.
    for foldname in folders:
#        print(foldname)
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
    print(doneJson)
    input()
    for file in doneJson:
        print(file)
        if ".json" in file:
            dateString = file.replace(".json","")
            print(dateString)
            if os.path.exists("Base/" + file):
                send2trash.send2trash("Base/" + file)
            if os.path.exists("Base/" + dateString):
                send2trash.send2trash("Base/" + dateString)
        else: # Not a json file. Ignore
            print("That doesn't work")
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
            print("File: " + i + " is done")
            removeList.append(i.replace(".json",""))
            
    for a in removeList:
        for line in lines:
            if a == line.split(" ")[0]:
                lines.remove(line)
                print("Removed: "+ a)
    return lines

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
        print("6. Quit")
        selection = 7
        try:
            selection = int(input("What are we doing: "))
#            time.sleep(600)
        except:
            print("That doesn't seem to be an int")
        if selection == 1:
            print(initalizeDatabase())
            print("Creating the database")
        elif selection == 2:
            f = open("DncApiKey.txt" , "r")
            lines = f.readlines()
            for line in lines:
                print(updateDatabase(line.strip()))
            print("Updating the database")
        elif selection == 3:
            print("Adding more data")
            print(FullDayData())
        elif selection == 4:
            print("Cleaning Database")
            dupCleanDatabase() # Duplicates in toRead file
        elif selection == 5:
            crushDatabase()
            print("Crushing Database")
        elif selection == 6:
            print("Quitting")
            running = False
        else:
            print("That is not an option")


main()
