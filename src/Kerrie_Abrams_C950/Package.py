class Package:
    # package class constructor
    def __init__(self, package_id, address, city, state, zipcode, deadline_time, weight, status, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.departure_time = None
        self.arrival_time = None
        self.status = status
        self.notes = notes

    # overrides print method for this class. allowing package information to display formatted
    def __str__(self):
        return (f"{self.package_id: 10d} | {self.address:<40s} | {self.city: <20} | {self.state: ^8} | "
                f"{self.zipcode: ^10} | {self.deadline_time: <10} | "
                f"{self.weight: <8} | {self.status: <21} | {self.notes: <50}")

    # function that updates a package status for a given time.
    def update_status(self, time):
        if self.arrival_time <= time:
            arrival_time = str(self.arrival_time)
            self.status = "Delivered at %s" % arrival_time
        elif self.departure_time < time:
            self.status = "En route"
