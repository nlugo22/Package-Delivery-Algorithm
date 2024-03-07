# created by: Nicholas Lugo
# nlugo@wgu.edu
# student id: 010493968
import csv
from Graph import *
from Package import Package
from Truck import Truck
from datetime import *


def adjustString(temp):
    tempStr = str(temp)
    tempStr = tempStr.replace('North', 'N')
    tempStr = tempStr.replace('East', 'E')
    tempStr = tempStr.replace('South', 'S')
    tempStr = tempStr.replace('West', 'W')

    return tempStr


# using the distance table to fill in a list of addresses and pull out distances between addresses
with open('data/WGUPS Distance Table.csv') as distance_file:
    distanceCSV = csv.reader(distance_file)
    distanceCSV = list(distanceCSV)

    # pull out all the addresses into a list
    addressList = list()
    distanceList = list()
    start = False
    count = 0
    for item in distanceCSV:
        # skips the empty / header lines and finds where the address data starts
        if item[0] == "DISTANCE BETWEEN HUBS IN MILES":
            start = True
            continue                    # continue to skip the addresses listed across the top of the file

        # grabbing the distance data
        if start:
            # takes out the list of addresses, addresses have a space in front of them so remove that temp[1:]
            temp = item[1]
            temp = temp[1:]
            tempStr = adjustString(temp)

            addressList.append(tempStr)

            # the distance list begins after the addresses so item[2:] skips past the address in the table
            temp = item[2:]
            distanceList.append(temp)

# pull out packages from CSV and put them into a package hashtable
with open('data/WGUPS Package File.csv') as file:
    packageCSV = csv.reader(file)

    packageHash = ChainingHashTable()
    # only take in the csv file starting with the first id -- the csv has headers and other info that we don't want
    start = False
    for item in packageCSV:
        if item[0] == '1':
            start = True

        # put the data into the chaining hash table, there are 7 data values so snip out the others
        if start:
            temp = item[:7]                 # clear out the extra info (additional details are after cell 7

            packageId = temp[0]             # set up a package object
            packageAddress = temp[1]
            packageCity = temp[2]
            packageState = temp[3]
            packageZip = temp[4]
            deliverTime = temp[5]
            packageWeight = temp[6]
            packageAddress = adjustString(packageAddress)
            p = Package(packageId, packageAddress, packageCity, packageState, packageZip, deliverTime, packageWeight)

            # load package into a hash table, key: id, value: package object
            packageHash.insert(int(packageId), p)


# calculates the distance between two vertex
def calculate_distance(start_vertex, end_vertex):
    edge_distance = g.edge_weights[(start_vertex, end_vertex)]
    return edge_distance


def calculate_deliver_time(truck, min_distance, package = None):
    start_time = datetime.strptime(truck.currTime, "%H:%M:%S")
    delivery_time_duration = truck.calculate_delivery_time(min_distance)
    delivery_time = start_time + delivery_time_duration
    truck.currTime = delivery_time.strftime("%H:%M:%S")

    print("Truck departing at :", start_time.time())

    # update package delivery time
    if package is not None:
        package.status = "Delivered"
        package.deliveredAt = delivery_time
        print("Package delivered at: ", truck.currTime)


def returnToHub(truck):

    start_vertex = truck.address
    end_vertex = g.vertexHash.search(0)
    returnDistance = calculate_distance(start_vertex, end_vertex)
    truck.update_miles_traveled(returnDistance)
    calculate_deliver_time(truck, returnDistance)
    path = str(start_vertex.label) + " -> " + str(end_vertex.label)
    print("Truck arrived at: ", truck.currTime)
    print(path)
    print("Truck returned to hub.")
    print("Total distance so far: ", truck.milesDriven)
    print()
    truck.address = end_vertex

# truck is checking nearest neighbors and delivering packages.
def deliverPackages(truck):
    start_time = datetime.strptime(truck.currTime, "%H:%M:%S")
    deliverLast = False
    # pull out the package id's assigned to the truck and turn them into package objects
    notDelivered = []
    for package in truck.packages:
        package = packageHash.search(package)
        if int(package.id) == 9:
            deliverLast = True
            continue
        notDelivered.append(package)

    # empty the list of package ids
    truck.packages.clear()

    # loop through the packages while loop truck packages > 0
    while len(notDelivered) > 0:
        # initializing variables
        nearest_address = None
        min_distance = float('inf')

        start_vertex = truck.address
        end_vertex = None
        index = 0

        for package in notDelivered:
            # the vertex addresses have additional characters, so adding those into package_address
            package_address = package.address + '\n' + '(' + package.zip + ')'

            # special case to make sure 8 and 30 get delivered on time by truck 1
            if int(package.id) == 8 or int(package.id) == 30 or int(package.id) == 9:

                for i in range(len(addressList)):
                    if g.vertexHash.search(i).label == package_address:
                        end_vertex = g.vertexHash.search(i)
                        break
                curr_package = package
                package_index = index
                nearest_address = end_vertex
                min_distance = calculate_distance(start_vertex, nearest_address)
                break
            else:
                # searching the vertexHash for a vertex that matches package_address to assign the end_vertex
                for i in range(len(addressList)):
                    if g.vertexHash.search(i).label == package_address:
                        end_vertex = g.vertexHash.search(i)
                        break
                # end for loop

                # start checking for the nearest neighbor
                temp_distance = calculate_distance(start_vertex, end_vertex)
                if temp_distance < min_distance:
                    nearest_address = end_vertex
                    # store the current loop's info for the smallest found distance so that when it ends this info can be used outside the loop
                    min_distance = calculate_distance(start_vertex, nearest_address)
                    curr_package = package
                    package_index = index
            # keeps track of the index of the package in notDelivered so it can be removed / used later
            index += 1
        # end for loop

        # run the algorithm
        truck.update_miles_traveled(min_distance)
        calculate_deliver_time(truck, min_distance, curr_package)

        # the delivery path the truck took
        path = str(start_vertex.label) + " -> " + str(nearest_address.label)
        print(path)

        print("Total distance so far: ", truck.milesDriven)
        print()

        # remove the package that was delivered
        notDelivered.pop(package_index)

        # update the truck's new address
        truck.address = nearest_address
    # end while loop

    # special case to deliver number 9 that had a wrong address
    if deliverLast:
        package = packageHash.search(9)
        package.address = "410 S State St"
        package.city = "Salt Lake City"
        package.state = "UT"
        package.zip = "84111"
        package_address = package.address + '\n' + '(' + package.zip + ')'
        for i in range(len(addressList)):
            if g.vertexHash.search(i).label == package_address:
                end_vertex = g.vertexHash.search(i)
                break
        min_distance = calculate_distance(truck.address, end_vertex)
        calculate_deliver_time(truck, min_distance)
        truck.update_miles_traveled(min_distance)
        print("Truck arriving at: ", truck.currTime)
        path = str(truck.address.label) + " -> " + str(end_vertex.label)
        print(path)
        print("Total distance so far: ", truck.milesDriven)

g = Graph()
g.makeGraph(g, addressList, distanceList)

# start the trucks at the hub
hub = g.vertexHash.search(0)
deliverAnyTime = [8, 30, 2, 7, 10, 11, 12, 17, 22, 23, 24, 27, 33, 35]
# constraint: 13, 14, 15, 16, 19, 20 on same truck
# share: 39, 13 | 15, 16, 34 | 20, 21 | 7, 29
print("Truck 1 departing. . .")
truck_1_packages = [1, 4, 13, 14, 15, 16, 19, 20, 21, 29, 34, 39, 40]

truck_1 = Truck(truck_1_packages, 0, 18, 0, hub, "00:00:00", "08:00:00")
deliverPackages(truck_1)
returnToHub(truck_1)
truck_1.packages = deliverAnyTime
deliverPackages(truck_1)
print("-----------")

# constraint: 3, 18, 36, 38 on truck 2 only.
# share: 5 and 37 and 38,
print("Truck 2 departing. . .")
truck_2_packages = [3, 5, 18, 36, 37, 38]
truck_2 = Truck(truck_2_packages, 0, 18, 0, hub, "08:00:00", "08:00:00")
deliverPackages(truck_2)
returnToHub(truck_2)
print("-----------")

# constraint: package 9 has wrong info until 10:20
# 6, 32, 28, 25 delayed until 9:05
# share: 8,9,30 | 25,26 | 31, 32 |
print("Truck 3 departing. . .")
truck_3_packages = [6, 25, 26, 28, 31, 32, 9]
truck_3 = Truck(truck_3_packages, 0, 18, 0, hub, truck_2.currTime, truck_2.currTime)
deliverPackages(truck_3)
distance = truck_1.milesDriven + truck_2.milesDriven + truck_3.milesDriven
print("-----------")
print("TOTAL DISTANCE:", distance)


print("Welcome to WGUPS, the industry leader for package deliveries!")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
done = False

while not done:
    # command line interface
    print("---------------------------------------------")
    print("| Choose from the following options:         |")
    print("| [1]: View delivery status of packages.     |")
    print("| [2]: Look up a package given a package id. |")
    print("| [3]: Print all packages.                   |")
    print("| [exit]: Exits the program                  |")
    print("---------------------------------------------")

    # take a user input, put it to lowercase
    user_input = input()
    user_input = user_input.lower()

    # checking selected options
    if user_input == "1":


    # search for a package given its id
    elif user_input == "2":


    # print out all packages
    elif user_input == "3":

    elif user_input == "exit":
        print("Goodbye!")
        done = True
        break
    else:
        print("Invalid option, please try again.")