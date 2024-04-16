class Truck:
    def __init__(self, packages, departure_time, address_list):
        self.location = "4001 South 700 East"
        self.speed = 18
        self.capacity = 16
        self.packages = packages
        self.departure_time = departure_time
        self.total_mileage = 0.0
        self.current_time = departure_time
        self.distance_matrix = [[0 for i in range(len(address_list))] for j in range(len(address_list))]
        self.address_list = address_list
        self.best_tour = []




