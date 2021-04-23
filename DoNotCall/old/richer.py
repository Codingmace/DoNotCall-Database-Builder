import requests
import json
import os

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

def createFolder(folderpath):
    if os.path.exists(folderpath):
        print(folderpath + " already Exists")
    else:
        os.makedirs(folderpath)
        
def richer(dncApiKey):
    print("Does the enrichment of the data")
    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
    subDays = open("Done/toRead.txt", "r") # For the sub parts
    lines = subDays.readlines()
    currentDir = "Base/"
    # Chec if the folder exists. Maybe rewrite the file. For now ignoring it
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
            response = requests.get(baseUrl + dncApiKey + "&created_date=\"" + splits[0] + "\"&offset=" + str(offsetCount))
            if not validResponse(response.status_code):
                return "Did not finish. Please Rerun"
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
    lines = f.readlines()
    for line in lines:
        print("Using Key "+ line)
        print(richer(line))
        

FullDayData() 
