# Get all the information on the database about a phone number.
import json
import os

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

    
def reBase():
    allNumb = "result.json"
    goodNumbers = [] # Good number dict
    badNumbers = [] # Bad number dict
    goodNumb = [] # Same area code
    badNumb = [] # Different Area Code
    try:
        with open(allNumb, "r") as read_file:
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
        print("the file is having an issue ")
        
    # Go through the numbers and sort
    print(str(len(goodNumb)))
    print(str(len(badNumb)))
    # Turning dict to file
    with open('badNumbers.json', 'w') as fp:
        json.dump(badNumbers, fp)

    with open('goodNumbers.json', 'w') as fp:
        json.dump(goodNumbers, fp)


if os.path.exists("result.json"):
    seperate()

goodNumbers = []
badNumbers = []
# Check valid first.
# If none check bad
# Look all of those little id and request if wanted.
