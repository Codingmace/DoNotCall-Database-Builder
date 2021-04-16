# importing the module
import numpy as np

f = open("compare.csv", "r")
logs = open("Logs.txt", "a")
lines = f.readlines()
f.close()
lines.remove(lines[0]) # remove header
sortingArray = []
newArray = []
rem = 0 # Removed numbers
zeros = 0 # Zeros removed
for line in lines:
    splits = line.strip().split(",")
    newLine = splits[0] + "," + splits[1] # Removing area
    if splits[0].isdigit():
        curNumb = int(splits[0])
        if curNumb <= 2000000000:
            if curNumb == 0:
                zeros += 1
            else:
                rem += 1
        else:
            newArray.append(newLine)
            sortingArray.append(int(splits[0]))

logs.write("Zeros Removed: " + str(zeros) +"\n")
logs.write("Invalid Numbers Removed: " + str(rem) + "\n")
logs.flush()
logs.close()
print("Before")

# sortingArray.sort()
# newSort = np.asarray(sortingArray)
sortings = np.array(sortingArray)
# sortings = np.sort(sortings, kind='heapsort')
sortings = np.argsort(sortings,kind='heapsort')
# np.sort(np.asarray(newArray))
c = 0
fx = open("orderNumb.txt", "w")
#print(newSort[0])
for x in sortings:
    fx.write(str(x) + "\n")
fx.flush()
fx.close()
# for i in range (0, 3, 1): 
#     print(str(sortingArray[i]))
# input()
# print("After")
# for i in range (0, 30, 1):
#     print(str(newArray[i]))
# np.sort(newArray)

qt = ['None'] * len(newArray)
fs = open("compareSort.csv", "w")
it = 0
for ax in sortings:
    curLine = newArray[ax] + "\n"
    fs.write(curLine)
    qt[it] = newArray[ax]
    it += 1

improved = []
qcon = 1
curNumbStr = qt[0]
qft = open("optumData.csv","w")
while len(qt) > 1:
    
    if qt[0].split(",")[0] == qt[qcon].split(",")[0]:
        curNumbStr += "," + qt[qcon].split(",")[1].strip()
        qcon += 1
    else: # Not equal
        qft.write(curNumbStr + "\n")
        qft.flush()
        improved.append(curNumbStr)
        qt.remove(qt[0])
        curNumbStr = qt[0]
        qcon = 1
        #input()
       #print(improved)

qft.close()
# for line in newArray:
#    fs.write(line + "\n")

fs.flush()
fs.close()

