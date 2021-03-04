import os
from datetime import datetime, timedelta, date
import requests
import json

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

def dateOffset(date1, date2): # Just year-month-day
    split1 = date1.split("-")
    split2 = date2.split("-")
    f_date = date(int(split1[0]), int(split1[1]), int(split1[2]))
    l_date = date(int(split2[0]), int(split2[1]), int(split2[2]))
    delta = l_date - f_date
    return delta.days


def updateDatabase(dncApiKey):
    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
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
    curDay.write(currentDay.strftime("%Y-%m-%d"))
    curDay.close()

    print("Rewritting the lastDate file as we are up to date")
    return "I have made it to the end."
    

    # Add a part to continue where left off in the toRead File
print(updateDatabase("xQEdbYXrktEA8OoKp835FM8GZ4yWife24A5JjepE"))
