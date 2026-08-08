import random


def simpleSort(list):
    sortedList = []
    while len(list) > 0:
        minElem = list[0]
        for num in list:
            if num < minElem:
                minElem = num
        list.remove(minElem)
        sortedList.append(minElem)
    return sortedList


# create list of 10 random numbers
list = []
for i in range(0, 10):
    list.append(random.randint(0, 100))

# sort the lists
list = simpleSort(list)
print(list)
