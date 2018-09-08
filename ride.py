class Ride:

    def __init__(self, id, start_loc, end_loc, start_time, end_time):
        self.id = id
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.start_time = start_time
        self.end_time = end_time
        self.status = 'incomplete'

    def updateStatus(status):
        self.status = status
