# Kerrie Abrams
# Student ID: 010894830
# C950 - Data Structures and Algorithms II
# Task 2: WGPUS Routing Program Implementation

import csv
import Package
import CreateHashTable
import Truck

packageHashTable = CreateHashTable.HashTable()


def load_package_data(file_name):
    with open(file_name) as package_file:
        package_data = csv.reader(package_file, delimiter=',')
        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline_time = package[5]
            weight = package[6]
            status = "At the hub"

            package = Package.Package(package_id, address, city, state, zipcode, deadline_time, weight, status)

            packageHashTable.insert(package_id, package)


