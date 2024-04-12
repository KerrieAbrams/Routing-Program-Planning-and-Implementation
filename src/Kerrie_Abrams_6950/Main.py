# Kerrie Abrams
# Student ID: 010894830
# C950 - Data Structures and Algorithms II
# Task 2: WGPUS Routing Program Implementation

import csv
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
            package_id = package[0]
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline_time = package[5]
            weight = package[6]
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
address_list = load_address_data("CSV/WGUPS_Address_File.csv")


# parses distance table from csv into a list
def load_distance_data(file_name):
    with open(file_name) as distance_file:
        distance_data = list(csv.reader(distance_file))
        return distance_data


# create distance table
distance_table = load_distance_data("CSV/WGUPS_Distance_Table_File.csv")


# finds and returns the index of a given address
def get_index(address):
    for data in address_list:
        if address in data[2]:
            return data[0]


# function to retrieve distance between locations given the indexes
def get_distance(x_index, y_index):
    distance = distance_table[x_index][y_index]
    if distance == "":
        distance = distance_table[y_index][x_index]
    return distance





