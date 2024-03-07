

def findById(self):
    done = False
    while not done:
        key = input('Enter a package id, exit to stop: ')

        key = key.lower()
        if key == 'exit':
            done = True
            break
        elif key.isalnum():
            index = int(key)
            package = self.myHash.search(index)
            print("| Id |     Address     |     City     | State |  Zip  | ETA | Weight |")
            print(package.print_package())

        else:
            print("Invalid search")

def printValues(self):
    self.myHash.printAll()


def printByTime(self):
    startTime = input('Enter a start time (e.x. 12:00 AM, case matters): ')
    self.myHash.findTime(startTime)

