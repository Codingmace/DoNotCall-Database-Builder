import numpy as np

def contains(arrayItem, it, qt):
    try:
        if qt[it] == arrayItem:
            return True
        if qt[it-1] == arrayItem:
            return True
        if qt[it+1] == arrayItem:
            return True
    except:
        return False

def main():
    f = open("compare.csv", "r")
    logs = open("Logs.txt", "a")
    lines = f.readlines()
    f.close()
    if "Number" in lines[0]:
        lines.remove(lines[0]) # remove header
    sortingArray = []
    newArray = []
    rem = 0 # Removed numbers
    zeros = 0 # Zeros removed
    for line in lines:
        splits = line.strip().split(",")
        newLine = splits[0] + "," + splits[1] # Removing area
        if splits[0].isdigit(): # Check if valid number
            curNumb = int(splits[0])
            if curNumb <= 2000000000:
                if curNumb == 0:
                    zeros += 1
                else:
                    rem += 1
            else: # Valid Number
                newArray.append(newLine)
                sortingArray.append(int(splits[0]))

    logs.write("Zeros Removed: " + str(zeros) +"\n")
    logs.write("Invalid Numbers Removed: " + str(rem) + "\n")
    logs.flush()

    sortings = np.array(sortingArray) # Found it worked with 2 statements instead of 1
    sortings = np.argsort(sortings,kind='heapsort')
    c = 0
#    fx = open("orderNumb.txt", "w") # Don't have to write anymore
#    for x in sortings:
#        fx.write(str(x) + "\n")
#    fx.flush()
#    fx.close()

    qt = ['None'] * len(newArray) # Improved array writting to
    fs = open("compareSort.csv", "w")
    it = 0
    counters = 0
    for ax in sortings:
        curLine = newArray[ax] + "\n"
        if contains(newArray[ax], it, qt): # Already recored
            counters+= 1
        else: # Not recorded so adding
            fs.write(curLine)
            qt[it] = newArray[ax]
            it += 1

    fs.flush() # Closing files
    fs.close()
    logs.write("Duplicate Count: " + str(counters))
    logs.write("Final Size: " + str(len(qt)))

    logs.close()

main()
