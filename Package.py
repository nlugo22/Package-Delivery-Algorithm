class Package:
    def __init__(self, packageId, deliverAddress, deliverCity, deliverState, deliverZip, deliverDeadline, packageWeight):
        self.id = packageId
        self.address = deliverAddress
        self.city = deliverCity
        self.state = deliverState
        self.zip = deliverZip
        self.deadline = deliverDeadline
        self.weight = packageWeight
        self.status = deliverStatus = "At Hub"
        self.deliveredAt = datetime = 0

    def print_package(self):
        print(f'| {self.id} | {self.address} | {self.city} | {self.state} | {self.zip} | {self.deadline} | {self.weight} | {self.status} |')