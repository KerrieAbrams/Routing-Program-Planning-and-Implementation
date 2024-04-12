class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline_time, weight, status):
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

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.deadline_time,
            self.weight,
            self.status,
            self.arrival_time
        )

    def update_status(self):
        if