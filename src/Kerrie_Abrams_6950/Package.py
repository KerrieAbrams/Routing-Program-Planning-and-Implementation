class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline_time, weight, departure_time, arrival_time, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self. zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = status

    def __str__(self):
        return self.package_id