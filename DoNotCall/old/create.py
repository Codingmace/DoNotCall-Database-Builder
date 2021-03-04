import os
import json
import requests
from datetime import datetime, timedelta, date
import time

def validResponse(statusCode):
    if (statusCode == 200):
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
    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
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
        if os.path.exists(str("Base\\" + form+".json")):
            print(form + " already exists")
            offset += 1
            continue # Don't want to recall a file that already exists
        response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + form + "\"")
#        print(response.text)
        if d.year <= 2020 and d.month <= 1:
            moreDays = False
        if not validResponse(response.status_code):
            subDays.close()
            print("Exiting at " + form)
            return offset # If done
#            input("Press any key to close")
#            exit()
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
    print(lines)
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
        line=line.strip()
        offset = createDatabase(line,offset)
        createdDatabase = offset == -1
        if not createdDatabase:
            print("Fuck that didn't work")
            offset += 1
        else:
            print("That was successful and we created the database")
        time.sleep(5) # Probably wait a little time and write where stopped

initalizeDatabase()
print("The code has been tested and works")
