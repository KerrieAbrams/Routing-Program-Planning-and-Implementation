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


# parses package info from csv
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
            # creates package object
            package = Package.Package(package_id, address, city, state, zipcode, deadline_time, weight, status)
            # print(package.__str__())
            # adds package to hash table
            packageHashTable.insert(package_id, package)


# calls the load_package_data function to parse the package information
load_package_data("CSV/WGUPS_Package_File.csv")


# parses address info from csv into a list
def load_address_data(file_name):
    with open(file_name) as address_file:
        address_data = list(csv.reader(address_file))
        return address_data


# create address list
CSV_address_list = load_address_data("CSV/WGUPS_Address_File.csv")


# parses distance table from csv into a list
def load_distance_data(file_name):
    with open(file_name) as distance_file:
        distance_data = list(csv.reader(distance_file))
        return distance_data


# create distance table
CSV_distance_table = load_distance_data("CSV/WGUPS_Distance_Table_File.csv")


# finds and returns the index of a given address
def get_index(address, a_list):
    for data in a_list:
        if address in data[1]:
            return int(data[0])


# function to retrieve distance between locations given the indexes
def get_distance(x_index, y_index, table):
    distance = table[x_index][y_index]
    if distance == "":
        distance = table[y_index][x_index]
    return float(distance)


# given a package_list, create a list of unique delivery addresses
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


# create a random "best tour"
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
        # assign the next location to the first package delivery address
        package = packageHashTable.search(package)
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
        print(package)

    # after all deliveries are complete, return truck to hub
    distance = get_distance(get_index(truck.location, address_list), 0, distance_matrix)
    # update truck location
    truck.location = "4001 South 700 East"
    # update truck clock
    truck.current_time += datetime.timedelta(hours=distance / truck.speed)
    # update truck mileage
    truck.total_mileage += distance


package_list1 = [4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 25, 29, 30, 34, 39, 40]
package_list2 = [1, 3, 5, 6, 18, 26, 36, 37, 38]
package_list3 = [2, 9, 10, 11, 12, 17, 21, 22, 23, 24, 27, 28, 31, 32, 33, 35]

address_list1 = create_address_list(package_list1)
address_list2 = create_address_list(package_list2)
address_list3 = create_address_list(package_list3)

truck1 = Truck.Truck(package_list1, datetime.timedelta(hours=8), address_list1)
truck2 = Truck.Truck(package_list2, datetime.timedelta(hours=9, minutes=5), address_list2)
truck3 = Truck.Truck(package_list3, datetime.timedelta(hours=10, minutes=20), address_list3)

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
new_package = Package.Package(9, "410 S State St", "Salt Lake City", "UT", "84111", "EOD", 2, "At the hub")
packageHashTable.insert(9, new_package)
# recreate address list after updating package list
new_address_list = create_address_list(package_list3)
# update truck 3 address list
truck3.address_list = new_address_list
# create distance matrix
address_distance_matrix(truck3)

two_opt_implement(truck3)
deliver_packages(truck3)

print(truck1.total_mileage + truck2.total_mileage + truck3.total_mileage)
