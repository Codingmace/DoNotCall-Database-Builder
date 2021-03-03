def crushDatabase(foldername):
    print("Merging the files in the folder name")
    fullpath = "Base/temp/" + foldername
    ar = os.listdir(fullpath)
    for a in ar: # All the files merging
    try:
        with open(("Past Days\\" + form + ".json"), "r") as read_file:
            developer = json.load(read_file)
            for x in developer['meta']:
                dex.append(x)
    except:
        return "Leaving the file alone because an issue occured"
        
    dex = []

    # Turning dict to file
    with open("Done/" + foldername+".json", 'w') as fp:
        json.dump(dex,fp)
    
    return "Successfully merged the file"
