from datetime import datetime, timedelta
import json
def mergeJson():
    print("Started Reading JSON file")
    dex = []
    for i in range(0,450):
        try:
            d = datetime.today() - timedelta(days=i)
            form = d.strftime("%Y-%m-%d")
            print(form)
            with open(("Past Days\\" + form + ".json"), "r") as read_file:
                print(form)
                developer = json.load(read_file)
                for x in developer['data']:
                    dex.append(x)
        except:
            print("the file " + "")

    # Turning dict to file
    with open('result.json', 'w') as fp:
        json.dump(dex, fp)

mergeJson()
