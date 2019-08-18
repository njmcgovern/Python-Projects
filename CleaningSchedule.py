# Nathan McGovern 2019
# UIUC Computer Engineering

import random

fileName = "CleaningSchedule"
inHouseMember = []
outOfHouseMember = []
daysOfWeek = ['Monday', 'Tuesday', 'Wednesday',
'Thursday', 'Friday', 'Saturday', 'Sunday']
numberInHouse = 0
numberOutOfHouse = 0
numberOfDays = 7
Floor1 = []
Saturday = []


fileName = fileName + input("Fall, Spring, or Summer: ") + input("Curernt Year: ")
b = input("Enter the names of brothers living in house: ")
c = input("Enter the names of brothers not living in house: ")
inHouseMember = b.split(', ')
outOfHouseMember = c.split(', ')
numberInHouse = len(inHouseMember)
numberOutOfHouse = len(outOfHouseMember)

try:
    file = open(fileName, 'w')
    for week in range(1, 16):
        print("\nWeek {}".format(week))
        for day in daysOfWeek:
            print(day)

            Floor1.append(random.choice(inHouseMember))
            f1 = random.choice(inHouseMember)
            f2 = random.choice(inHouseMember)
            f3 = random.choice(inHouseMember)
            while f1 == Floor1[0]:
                f1 = random.choice(inHouseMember)
            Floor1.append(f1)
            while f2 == Floor1[0] or f2 == Floor1[1]:
                f2 = random.choice(inHouseMember)
            while f3 == f2 or f3 == Floor1[0] or f3 == Floor1[1]:
                f3 = random.choice(inHouseMember)

            print("Floor 1: ", Floor1[0], Floor1[1])
            print("Floor 2: ", f2)
            print("Floor 3: ", f3)
            Floor1.clear()

        for brother in range(0, 14):
            if len(Saturday) == 0:
                Saturday.append(random.choice(outOfHouseMember))
                continue
            if brother%3 != 0:
                s = random.choice(outOfHouseMember)
                while s in Saturday:
                    s = random.choice(outOfHouseMember)
            else:
                s = random.choice(inHouseMember)
                while s in Saturday:
                    s = random.choice(inHouseMember)

            Saturday.append(s)
        print("\nSaturday Cleaning Schedule")
        print("Floor 1: ", Saturday[0:5])
        print("Floor 2: ", Saturday[5:9])
        print("Floor 3: ", Saturday[9:])
        Saturday.clear()

finally:
    file.close()
