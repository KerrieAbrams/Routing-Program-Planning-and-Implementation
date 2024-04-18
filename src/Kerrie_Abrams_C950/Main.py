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
            # print(package.__str__())
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


# finds and returns the index of a given address
def get_index(address, index_list):
    # searches the given index_list for the specified address and returns the index as an integer
    for data in index_list:
        if address in data[1]:
            return int(data[0])


# function to retrieve distance between locations of two given indexes
def get_distance(x_index, y_index, table):
    distance = table[x_index][y_index]
    if distance == "":
        distance = table[y_index][x_index]
    return float(distance)


# given a package_list, creates a list of unique delivery addresses
def create_address_list(package_list):
    # create new list
    address_list = []
    i = 0
    # append hub address to address
    address = [0, "4001 South 700 East"]
    address_list.append(address)
    # append each unique [index, "address"] from package_list to address_list
    for package_id in package_list:
        package = packageHashTable.search(package_id)
        address = [get_index(package.address, CSV_address_list), package.address]
        if address not in address_list:
            address_list.append(address)
    # reassign indexes for future use in distance matrix
    for address in address_list:
        address[0] = i
        i = i + 1
    return address_list


# for a given truck, creates a distance matrix based on the assigned address list
def address_distance_matrix(truck):
    # creates a list that represents the x values in a matrix
    x_addresses = truck.address_list
    # creates a list that represents the y values in a matrix
    y_addresses = truck.address_list
    # for every combination of addresses, a distance is assigned to the corresponding coordinate
    for x_address in x_addresses:
        for y_address in y_addresses:
            # get original indexes from CSV_address_list
            x_index = get_index(x_address[1], CSV_address_list)
            y_index = get_index(y_address[1], CSV_address_list)
            # get distance between addresses from distance_table and assign to corresponding coordinate
            truck.distance_matrix[x_address[0]][y_address[0]] = get_distance(x_index, y_index, CSV_distance_table)


# The following 3 functions used in the 2-Opt Algorithm.
# creates a random "best tour"
def generate_ran_tour(truck):
    # append packages to best_tour list
    for item in truck.packages:
        truck.best_tour.append(item)
    # shuffle the tour
    random.shuffle(truck.best_tour)


# returns distance for a given tour
def two_opt_distance(truck, tour):
    tour = tour
    distance_matrix = truck.distance_matrix
    address_list = truck.address_list
    # set distance to 0
    total_distance = 0
    # assigns starting location to where the truck begins, which is the hub
    location1 = 0
    for package in tour:
        # look up the package object
        package = packageHashTable.search(package)
        # assign the next location to the first package delivery address
        location2 = get_index(package.address, address_list)
        # calculate distance between start and next location
        distance = get_distance(location1, location2, distance_matrix)
        total_distance += distance
        # reassign starting address to next address
        location1 = location2
    # after tour is complete, return truck to hub and calculate total_distance
    distance = get_distance(location1, 0, distance_matrix)
    total_distance += distance
    return total_distance


# Performs a 2-opt swap
def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
    return new_tour


def two_opt_implement(truck):
    generate_ran_tour(truck)
    best_distance = two_opt_distance(truck, truck.best_tour)
    found_improvement = True
    while found_improvement:
        found_improvement = False
        for i in range(len(truck.best_tour) - 1):
            for j in range(i + 1, len(truck.best_tour)):
                new_tour = two_opt_swap(truck.best_tour, i, j)
                new_distance = two_opt_distance(truck, new_tour)
                if new_distance < best_distance:
                    truck.best_tour = new_tour
                    best_distance = new_distance
                    found_improvement = True
    return best_distance


def deliver_packages(truck):
    distance_matrix = truck.distance_matrix
    address_list = truck.address_list
    # set distance to 0
    truck.total_mileage = 0.0
    # assigns starting location to where the truck begins, which is the hub
    for package in truck.best_tour:
        # assign the next location to the first package delivery address
        package = packageHashTable.search(package)
        truck_location = get_index(truck.location, address_list)
        next_location = get_index(package.address, address_list)
        # calculate distance between start and next location
        distance = get_distance(truck_location, next_location, distance_matrix)
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
    distance = get_distance(get_index(truck.location, address_list), 0, distance_matrix)
    # update truck location
    truck.location = "4001 South 700 East"
    # update truck clock
    truck.current_time += datetime.timedelta(hours=distance / truck.speed)
    # update truck mileage
    truck.total_mileage += distance


# From here to line 246, the 2-opt algorithm is used to calculate the best delivery route for 3 delivery trucks,
# each loaded with a different package list. The packages are delivered using the deliver_packages function
# to update each packages' information as they are delivered. A total_mileage is calculated at the end.

# 3 package lists are created in accordance to the package requirements. 1 for each truck.
package_list1 = [4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39, 40]
package_list2 = [1, 3, 5, 6, 18, 25, 26, 36, 31, 32, 38]
package_list3 = [2, 9, 10, 11, 12, 17, 22, 23, 24, 27, 28, 33, 35]

# Address lists are created from the package lists. Storing only unique addresses.
# These files are used find the index of an address, which are used to search a distance matrix.
address_list1 = create_address_list(package_list1)
address_list2 = create_address_list(package_list2)
address_list3 = create_address_list(package_list3)

# 3 truck objects are created with the previously created package lists and address lists
truck1 = Truck.Truck(package_list1, datetime.timedelta(hours=8), address_list1)
truck2 = Truck.Truck(package_list2, datetime.timedelta(hours=9, minutes=5), address_list2)
truck3 = Truck.Truck(package_list3, datetime.timedelta(hours=10, minutes=20), address_list3)

# An address_distance_matrix is created for each truck.
address_distance_matrix(truck1)
address_distance_matrix(truck2)
address_distance_matrix(truck3)

two_opt_implement(truck1)
deliver_packages(truck1)
two_opt_implement(truck2)
deliver_packages(truck2)

# ensures truck3 departs at or after scheduled departure time if both trucks arrive after the scheduled departure time
if truck3.departure_time < min(truck1.current_time, truck2.current_time):
    # updates truck3 departure time to the truck_time of the truck that arrives earliest
    truck3.departure_time = min(truck1.current_time, truck2.current_time)
# updates package 9 address
new_package = Package.Package(9, "410 S State St", "Salt Lake City", "UT", "84111", "EOD", 2, "At the hub",
                              "Wrong address listed")
packageHashTable.insert(9, new_package)
# recreate address list after updating package list
new_address_list = create_address_list(package_list3)
# update truck 3 address list
truck3.address_list = new_address_list
# create distance matrix
address_distance_matrix(truck3)

two_opt_implement(truck3)
deliver_packages(truck3)

total_mileage = round(truck1.total_mileage + truck2.total_mileage + truck3.total_mileage, 1)


# The following two functions are used in the main class to display package information for each truck.
# They will update each package's status information to display correctly for a given time.
def print_package(package, user_time):
    if package.package_id == 9:
        if user_time < datetime.timedelta(hours=10, minutes=20):
            package.address = "300 State St"
            package.zipcode = "84103"

    package.update_status(user_time)
    print(package)


def print_trucks(truck, num, user_time):
    print("\nTruck %d" % num)
    print(truck)
    print(''.center(170, '-'))
    print(
        f"{'Package ID': ^10} | {'Address': ^40} | "
        f"{'City': ^20} | {'State': ^8} | {'Zipcode': ^10} | {'Deadline': ^10} | "
        f"{'Weight': ^8} | {'Status': ^21} | {'Special Notes': ^20}"
    )
    for package in truck.best_tour:
        package = packageHashTable.search(package)
        print_package(package, user_time)


class Main:
    print(f"{'WGUPS ROUTING PROGRAM':^170s}")
    print(f"{'Total Mileage of Route: ':>93s}{total_mileage}{' mi'}")

    user_prompt = input("Would you like to check the status of a package?\nEnter Yes or No: ")
    if user_prompt == "y" or user_prompt == "Yes" or user_prompt == "yes":
        try:
            user_time = input("Please enter the time (HH:MM): ")
            (h, m) = user_time.split(":")
            user_time = datetime.timedelta(hours=int(h), minutes=int(m))
            user_request = input("Would you like to view a single package or all packages?\nEnter Single or All: ")
            if user_request == "Single" or user_request == "single":
                try:
                    user_package = input("Please enter the package ID: ")
                    package = packageHashTable.search(int(user_package))
                    print(
                        f"{'Package ID': ^10} | {'Address': ^40} | "
                        f"{'City': ^20} | {'State': ^8} | {'Zipcode': ^10} | {'Deadline': ^10} | "
                        f"{'Weight': ^8} | {'Status': ^21} | {'Special Notes': ^20}"
                    )
                    print_package(package, user_time)
                except AttributeError:
                    print("Package not found. Please enter a number [1-40], goodbye")
                    exit()
            elif user_request == "All" or user_request == "all":
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
