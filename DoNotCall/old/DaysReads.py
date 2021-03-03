from datetime import datetime, timedelta
import json

def mergeJson():
    print("Started Reading JSON file")
    dex = []
    for i in range(0,450):
        try:
            d = datetime.today() - timedelta(days=i)
            form = d.strftime("%Y-%m-%d")
            with open(("Past Days\\" + form + ".json"), "r") as read_file:
                developer = json.load(read_file)
#                print(developer)
                for x in developer['meta']:
#                    print(x)
                    dex.append(x)
        except:
            print("the file " + "")

    # Turning dict to file
    with open('result.txt', 'w') as fp:
        for a in dex:
            print(a['record-total'])
            fp.write(str(a['record-total']) + "\n")


mergeJson()
