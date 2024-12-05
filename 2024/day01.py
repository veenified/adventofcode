# day01.py
from utils.utils import get_input

# Test input
testInput = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

# get problem input
problemInput = get_input(2024, 1)

# dayInput = testInput
dayInput = problemInput

# split testInput into two lists, leftList and rightList
leftList = []
rightList = []
for line in dayInput.split("\n"):
    if line.strip():  # Only process non-empty lines
        leftList.append(int(line.split("   ")[0]))
        rightList.append(int(line.split("   ")[1]))

# sort both lists
leftList.sort()
rightList.sort()

# write the absolute value difference between the two lists to a new list
differenceList = []
for i in range(len(leftList)):
    differenceList.append(abs(leftList[i] - rightList[i]))

# find the sum of the differenceList
print(f"Distance (Part 1): {sum(differenceList)}")

# Part 2
# calculate a map of the distinct items in rightList and their counts
rightListMap = {}
for item in rightList:
    rightListMap[item] = rightListMap.get(item, 0) + 1

# for every item in leftList, multiply by the count of the corresponding item in rightListMap
total = 0
for item in leftList:
    total += item * rightListMap.get(item, 0)

print(f"Similarity Score (Part 2): {total}")
