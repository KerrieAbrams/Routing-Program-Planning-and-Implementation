# Kerrie Abrams
# Student ID: 010894830
# C950 - Data Structures and Algorithms II
# Task 2: WGPUS Routing Program Implementation

import csv
import datetime
import random
import Package
import CreateHashTable
import Truck

# create new hash table
packageHashTable = CreateHashTable.HashTable()


# parses package info from csv, stores each line of data into a package object and appends it to the hash table
def load_package_data(file_name):
    with open(file_name) as package_file:
        # creates reader object from csv
        package_data = csv.reader(package_file)
        # parses data into separate variables
        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline_time = package[5]
            weight = int(package[6])
            status = "At the hub"
            notes = package[7]
            # creates package object
            package = Package.Package(package_id, address, city, state, zipcode, deadline_time, weight, status, notes)
            # adds package to hash table
            packageHashTable.insert(package_id, package)


# calls the load_package_data function to parse the package information
load_package_data("CSV/WGUPS_Package_File.csv")


# parses address info from csv into a list
def load_file_data(file_name):
    with open(file_name) as file:
        file = list(csv.reader(file))
        return file


# create address list from the CSV using the load_file_data function
CSV_address_list = load_file_data("CSV/WGUPS_Address_File.csv")

# create distance table from the CSV using the load_file_data function
CSV_distance_table = load_file_data("CSV/WGUPS_Distance_Table_File.csv")


# Searches an index list for a given address and returns the corresponding index
def get_index(address, index_list):
    # searches the given index_list for the specified address and returns the index as an integer
    for data in index_list:
        if address in data[1]:
            return int(data[0])


# function to retrieve the distance between locations of two given indexes from a distance matrix
def get_distance(x_index, y_index, matrix):
    distance = matrix[x_index][y_index]
    if distance == "":
        distance = matrix[y_index][x_index]
    return float(distance)


# The following 3 functions are used in the 2-Opt Algorithm.
# creates a random "best tour"
def generate_ran_tour(truck):
    # append packages to best_tour list
    for item in truck.packages:
        truck.best_tour.append(item)
    # shuffle the tour
    random.shuffle(truck.best_tour)


# returns distance for a given tour
def two_opt_distance(tour):
    tour = tour
    total_distance = 0
    # assigns starting location to where the truck begins, which is the hub
    location1 = 0
    for package in tour:
        # look up the package object
        package = packageHashTable.search(package)
        # assign the next location to the first package delivery address
        location2 = get_index(package.address, CSV_address_list)
        # calculate distance between start and next location
        distance = get_distance(location1, location2, CSV_distance_table)
        total_distance += distance
        # reassign starting address to next address
        location1 = location2
    # after tour is complete, return truck to hub and calculate total_distance
    distance = get_distance(location1, 0, CSV_distance_table)
    total_distance += distance
    return total_distance


# The 2-opt swap. Concatenates a new tour from portions of the original tour. The first portion is tour[0] to tour[i]
# The second portion is tour[i + 1] to tour[j] in reverse. The third portion is tour[j + 1] to the end.
# Returns the new tour
def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
    return new_tour


# This function implements the 2 opt algorithm for a given truck.
# First, it generates a random route from the truck package list and calculates the total distance for that route.
# Then, for every possible combination of address pairs, it performs a 2-opt swap and compares the new distance
# to the previous total distance. If there is an improvement, it accepts the swap as the new best tour.
# The algorithm repeats until there is no improvement. The best tour is saved to the truck class as best_tour.
def two_opt_implement(truck):
    # generates random route
    generate_ran_tour(truck)
    # calculates distance of that route
    best_distance = two_opt_distance(truck.best_tour)
    # algorithm assumes there is improvement
    found_improvement = True
    while found_improvement:
        # sets improvement to false so that if no improvement is found, algorithms stops.
        found_improvement = False
        # for every combination of address pairs, perform the following:
        for i in range(len(truck.best_tour) - 1):
            for j in range(i + 1, len(truck.best_tour)):
                # 2 opt swap
                new_tour = two_opt_swap(truck.best_tour, i, j)
                # calculate new distance
                new_distance = two_opt_distance(new_tour)
                # if new distance is better, reassign best_tour and best_distance to new values
                if new_distance < best_distance:
                    truck.best_tour = new_tour
                    best_distance = new_distance
                    # tell algorithm that improvement was found, allowing it to repeat.
                    found_improvement = True


# The following function actually delivers the packages for a given truck, updating relevant truck and package
# information along the way.
def deliver_packages(truck):
    truck.total_mileage = 0.0
    # assigns starting location to where the truck begins, which is the hub
    for package in truck.best_tour:
        # assign the next location to the first package delivery address
        package = packageHashTable.search(package)
        truck_location = get_index(truck.location, CSV_address_list)
        next_location = get_index(package.address, CSV_address_list)
        # calculate distance between start and next location
        distance = get_distance(truck_location, next_location, CSV_distance_table)
        # move truck to next location
        truck.location = package.address
        # update truck mileage
        truck.total_mileage += distance
        # update current truck time
        truck.current_time += datetime.timedelta(hours=distance / truck.speed)
        # deliver package and update status
        package.arrival_time = truck.current_time
        package.departure_time = truck.departure_time
    # after all deliveries are complete, return truck to hub
    distance = get_distance(get_index(truck.location, CSV_address_list), 0, CSV_distance_table)
    # update truck location
    truck.location = "4001 South 700 East"
    # update truck clock
    truck.current_time += datetime.timedelta(hours=distance / truck.speed)
    # update truck mileage
    truck.total_mileage += distance


# From here to line 220, the 2-opt algorithm is used to calculate the best delivery route for 3 delivery trucks,
# each loaded with a different package list. The packages are delivered using the deliver_packages function
# to update each packages' information as they are delivered. A total_mileage is calculated at the end.

# 3 package lists are created in accordance to the package requirements. 1 for each truck.
package_list1 = [4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39, 40]
package_list2 = [1, 3, 5, 6, 18, 25, 26, 36, 31, 32, 38]
package_list3 = [2, 9, 10, 11, 12, 17, 22, 23, 24, 27, 28, 33, 35]


# 3 truck objects are created with the previously created package lists and address lists
truck1 = Truck.Truck(package_list1, datetime.timedelta(hours=8))
truck2 = Truck.Truck(package_list2, datetime.timedelta(hours=9, minutes=5))
truck3 = Truck.Truck(package_list3, datetime.timedelta(hours=10, minutes=20))


# run the two opt algorithm for truck 1 and 2
two_opt_implement(truck1)
two_opt_implement(truck2)

# truck 1 and truck 2 deliver packages
deliver_packages(truck1)
deliver_packages(truck2)

# With only 2 drivers, only 2 trucks can be driven simultaneously. Truck 3 must wait for one of the other two return.
# The following 2 lines of code ensure truck3 departs at or after scheduled departure time.
# If both trucks arrive after the scheduled departure time, truck 3 departs as soon as one of the other trucks arrives.
if truck3.departure_time < min(truck1.current_time, truck2.current_time):
    # updates truck3 departure time to the truck_time of the truck that arrives earliest
    truck3.departure_time = min(truck1.current_time, truck2.current_time)

# Prior to truck 3 departing, WGUPS receives the correct delivery address for package 9.
# The following 5 lines of code update the delivery address.
package9 = packageHashTable.search(9)
package9.address = "410 S State St"
package9.zipcode = "84111"
# update hashtable
packageHashTable.insert(9, package9)

# Now truck 3 can leave.
# run the algorithm for truck 3
two_opt_implement(truck3)
# truck 3 delivers packages
deliver_packages(truck3)

# calculate the total mileage for all trucks. The values used are returned from the deliver_packages function
total_mileage = round(truck1.total_mileage + truck2.total_mileage + truck3.total_mileage, 1)


# The following two functions are used in the main class to display package information for each truck.
# They will update each package's status information to display correctly for a given time.

# Updates status of a package to correctly display for a given time. Prints that packages.
# If package is package 9 and the given time is prior to 10:20, set the address to the incorrect address.
def print_package(package, user_time):
    # update package 9 address if necessary.
    if package.package_id == 9 and user_time < datetime.timedelta(hours=10, minutes=20):
        package.address = "300 State St"
        package.zipcode = "84103"
    # update package status for given time
    package.update_status(user_time)
    # print package info
    print(package)


# prints truck information and header for package information, then prints all package information for all packages
# for a given truck.
def print_trucks(truck, num, user_time):
    # print truck information and  headers
    print("\nTruck %d" % num)
    print(truck)
    print(''.center(170, '-'))
    print(
        f"{'Package ID': ^10} | {'Address': ^40} | "
        f"{'City': ^20} | {'State': ^8} | {'Zipcode': ^10} | {'Deadline': ^10} | "
        f"{'Weight': ^8} | {'Status': ^21} | {'Special Notes': ^20}"
    )
    # prints every package in the order that they are delivered
    for package_id in truck.best_tour:
        # search for package object with package id
        package = packageHashTable.search(package_id)
        # call print_package to actually print out the package
        print_package(package, user_time)


# The following code creates a user interface for the WGUPS routing program and displays the total mileage calculated
# from delivering all packages of all three trucks.
# It allows the user to check the status of a package for a specified time. Or allows the user to see the status
# of all packages for the specified time.
class Main:
    # Displays program header
    print(f"{'WGUPS ROUTING PROGRAM':^170s}")
    # Displays total mileage of routes
    print(f"{'Total Mileage of Routes: ':>93s}{total_mileage}{' mi'}")

    # The first prompt. User can choose to check the status of a package. The program exits if they answer no.
    user_prompt = input("Would you like to check the status of a package?\nEnter Yes or No: ")
    if user_prompt == "y" or user_prompt == "Yes" or user_prompt == "yes":
        # If user answers yes, the program will ask for the time. It will terminate if the input is invalid.
        try:
            user_time = input("Please enter the time (HH:MM): ")
            # program receives the time and stores it to user_time
            (h, m) = user_time.split(":")
            user_time = datetime.timedelta(hours=int(h), minutes=int(m))
            # program then asks the user if they would like to view all or one package.
            # program terminates if input is invalid
            user_request = input("Would you like to view one or all packages?\nEnter One or All: ")
            if user_request == "One" or user_request == "one":
                # if the user asks for one package, they program requests the package ID
                # then prints the requested package
                try:
                    user_package = input("Please enter the package ID: ")
                    package = packageHashTable.search(int(user_package))
                    print(
                        f"{'Package ID': ^10} | {'Address': ^40} | "
                        f"{'City': ^20} | {'State': ^8} | {'Zipcode': ^10} | {'Deadline': ^10} | "
                        f"{'Weight': ^8} | {'Status': ^21} | {'Special Notes': ^20}"
                    )
                    print_package(package, user_time)
                # if the package ID is not found, the program will inform the user and terminate
                except AttributeError:
                    print("Package not found. Please enter a number [1-40], goodbye")
                    exit()
            elif user_request == "All" or user_request == "all":
                # if the user requests all the packages, the program displays all packages for each truck.
                print_trucks(truck1, 1, user_time)
                print_trucks(truck2, 2, user_time)
                print_trucks(truck3, 3, user_time)
            else:
                print("Invalid input, goodbye.")
                exit()
        except ValueError:
            print("Invalid time input, goodbye")
            exit()
    elif user_prompt == "n" or user_prompt == "No" or user_prompt == "no":
        print("Thank you, goodbye")
        exit()
    else:
        print("Invalid input, goodbye.")
        exit()
