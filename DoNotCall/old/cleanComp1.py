# importing the module
import numpy as np

f = open("compareSort.csv", "r")

lines = f.readlines()
for i in range(100, 1000, 2):
    lines.append(lines[i])

# lines.remove(lines[0]) # remove header
np.sort(lines)

f.close()
fq = open("remLogs.txt", "w")
fs = open("compareSorts.csv", "w")
print("Lines Length" ,str(len(lines)))
newArray =[]
while len(lines) > 2:
    cur = lines[0]
    if cur == lines[1]:
        fq.write("Removed " + lines[1])
        fq.flush()
        lines.remove(lines[1])
    else:
        fs.write(cur)
        fs.flush()
#        print(str(len(newArray)), str(len(lines)))
        newArray.append(cur)
        lines.remove(cur)

fq.close()
print("New Line Length" , str(len(newArray)))
for line in newArray:
    fs.write(line)

fs.flush()
fs.close()


#newArray = (lines.sort())
#print(newArray)
#print(lines)
#print(len(lines))
#for line in lines:
#    bisect.insort(newArray, line)
#    if (len(newArray) % 10000 == 0):
#        print(len(newArray))
