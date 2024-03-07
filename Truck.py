from datetime import timedelta


class Truck:
    def __init__(self, packages, capacity, travelSpeed, milesDriven, address, departTime, currTime):
        self.packages = packages           # list of packages they can store
        self.capacity = capacity              # packages
        self.travelSpeed = travelSpeed           # miles per hour
        self.milesDriven = milesDriven           # how many miles did it drive so far (initialized to 0
        self.address = address
        self.departTime = departTime
        self.currTime = currTime

    def calculate_delivery_time(self, distance_miles):
        # Calculate time in hours based on distance and truck speed
        time_hours = float(distance_miles / self.travelSpeed)

        return timedelta(hours=time_hours)

    def update_miles_traveled(self, min_distance):
        total_distance = 0
        total_distance += min_distance
        self.milesDriven += total_distance
