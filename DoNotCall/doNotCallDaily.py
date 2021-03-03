import requests
import json
import time
from datetime import datetime, timedelta
# from variables import dncApiKey

# https://www.ftc.gov/developer
def clean(phoneNumber):
    # I could have just done non digits. Wow
    phoneNumber = phoneNumber.replace("+", "").replace("-","").replace("(","").replace(")","")
    if len(phoneNumber) == 10:
        return str(phoneNumber)
    elif len(phoneNumber) < 10:
        return "too short"
    else:
        return "too long"

def doNotCallList(phoneNumber):
    baseUrl = "https://api.ftc.gov/v0/dnc-complaints?api_key="
    number = clean(phoneNumber)
    if (number == "too short" or number == "too long"):
        print("That doesn't work")
        exit()

    apiKey = "yMQK54tjjKehjvhp3s7GRKP9ajoLjxgmpPv5d0E2"
    dncApiKey = apiKey
    areaCode = number[0:3]
    print(areaCode)
    areaCode = "243"
    startDate = "2021-01-20"
    endDate  = "2021-02-03"
    createdStart = "created_date_from=\"" + startDate + "\""
    createdEnd = "created_date_to=\"" + endDate + "\""
    creates = createdStart + "&" + createdEnd
    extendUrl = "offset="
    extendUrl2 = "area_code=" + areaCode
    state = "Texas"
    city = "dallas"

    
#    apiDoc = open("APIKey.txt", "r")
#    apiKey = apiDoc.readline() # Fix this by getting more keys
#    apiKey = "1MIqfBRshPMveerYAHsjso0BMUuRFP2GwpfXLpfW"
    # NEED TO REMOVE BECAUSE YOU CANNOT HAVE MORE THAN 1 VALID KEY AT A TIME

    errors = open("log.txt","a") # Adjust to be correct folder and not override eachother
    print("Check the logs first for something.")
    
    # Read in from the API
#        response = requests.get(baseUrl+ dncApiKey + "&" + extendUrl + str(offset) +"&" + extendUrl2 + "&" + creates)
    
    for offset in range(100, 300, 1):
        d = datetime.today() - timedelta(days=offset)
        form = d.strftime("%Y-%m-%d")
        print(offset)
        response = requests.get(baseUrl+dncApiKey + "&created_date=\"" + form + "\"")
#        response = requests.get(baseUrl+dncApiKey)

        if (response.status_code == 429):
            print("Rate has been exceeded")
        elif (response.status_code == 404):
            print("API server cannot be reached")
        elif (response.status_code == 403):
            print("Api key missing or invalid")
        elif (response.status_code == 400):
            print("URL Does not use HTTPS:")
        if not (response.status_code == 200):
            print("We are out of responses. Ended on offset of " + str(offset))
            errors.write("Out of request, "+ str(offset) + "\n")
            errors.flush()
            errors.close()
            exit()

        data = response.json()
        print(response.status_code)
        output = open(str("Data\\" +form +".json"), "w")
#        output = open(str("Data\\" + str(int(time.time()))+".json"), "w")
        print(data)

        # Parse Json
        del data['meta']['records-this-page']
        del data['links']

        for element in data['data']:
            del element['type']
            del element['relationships']
            del element['meta']
            del element['links']

            element['number'] = element['attributes']['company-phone-number']
            element['area-code'] = element['attributes']['consumer-area-code']

            del element['attributes']
            temp = element['id'] + " " + element['number'] + "\n"


        # Write it all to a file
        json.dump(data, output)
        errors.flush()
        output.flush()
        output.close()
    #    time.sleep(90)

    errors.close()

#doNotCallList("9728988473")
doNotCallList("8588988473")

def updateLogs():
    print("merge the Json data from each")
    print("Request as much as possible at that point")



