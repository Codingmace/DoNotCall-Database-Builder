# Combine all the ones in the completed folder
# Write them to the database that exist if it is their
import json
import os

class Node:
    def __init__(self, value, nextNode=None):
        self.id = value['id']
        self.numb = value['number']
        self.area = value['area-code']
#        print("That")
        self.good = value['number'][0:3] == value['area-code']
#        self.good = numb[0:3] == area
#        print("HE")
        self.nextNode = nextNode

    def getId(self):
        return self.id

    def getNumb(self):
        return self.numb

    def getArea(self):
        return self.area

    def goodBad(self):
        if numb[0:3] == area:
            return True
        else:
            return False
    
def mergeJson():
    baseDir = "Done/Completed/"
    mergeFiles = os.listdir(baseDir)
    listNumbers = []
    allNumb = [] # All the numbers as nodes
    goodNumb = [] # Same area code
    badNumb = [] # Different Area Code
    for fi in mergeFiles: # Load Numbers
        try:
            with open(baseDir + fi, "r") as read_file:
                developer = json.load(read_file)
                for x in developer:
                    n = Node(x)
                   # print("this")
                    if n.good:
                        goodNumb.append(n)
                    else:
                        badNumb.append(n)
        except:
            print("the file is having an issue " + fi)
            input("Input something to continue ")
    # Go through the numbers and sort
    print(str(len(goodNumb)))
    print(str(len(badNumb)))
    # Turning dict to file
#    with open('result.json', 'w') as fp:
#        json.dump(goodNumb, fp)

mergeJson()
