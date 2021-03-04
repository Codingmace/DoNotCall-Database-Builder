
import os
import json

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
crushDatabase()
