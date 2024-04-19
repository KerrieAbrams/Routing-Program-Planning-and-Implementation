class Truck:
    # truck class constructor
    def __init__(self, packages, departure_time):
        self.location = "4001 South 700 East"
        self.speed = 18
        self.capacity = 16
        self.packages = packages
        self.departure_time = departure_time
        self.total_mileage = 0.0
        self.current_time = departure_time
        self.best_tour = []

    # Overrides print method for truck class. displays formatted truck information
    def __str__(self):
        d_time = self.departure_time
        c_time = self.current_time
        mileage = round(self.total_mileage, 1)
        return "Departure Time: %s \t Estimated Return Time: %s \t Truck Mileage: %s" % (d_time, c_time, mileage)

