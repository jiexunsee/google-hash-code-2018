

class Car:
	def __init__(self, id):
		self.id = id
		self.availability = True
		self.time_at_location = 0
		self.end_location = [0,0]
		self.history = [];


	##########################################
	''' HELPER FUNCTIONS '''
	##########################################
	def get_availability(self, time):
		if time >= self.time_at_location :
			self.availability = True
		else :
			self.availability = False
		return self.availability	

	def get_location(self):
		return self.end_location

	def receive_assignment(self, ride):
		self.history.append(ride.id);
		time_taken = abs(ride.end_loc[0]-ride.start_loc[0]) + abs(ride.end_loc[1]-ride.start_loc[1])
		time_to_start = abs(ride.start_loc[0]-self.end_location[0]) + abs(ride.start_loc[1]-self.end_location[1])
		self.time_at_location += time_taken + time_to_start
		self.end_location = ride.end_loc
		self.availability = False


	def get_history(self):
		hist = list(map(str, self.history))
		return str(len(self.history)) + ' ' + ' '.join(hist)