import numpy as np
import operator
from munkres import Munkres, print_matrix
import sys
from tqdm import tqdm

from car import Car as Car
from ride import Ride as Ride

class Simulation:
	def __init__(self, file_path):
		with open(file_path, 'r') as f:
			a = f.read()

		arr = [b.split() for b in a.split('\n') if len(b) > 0]
		arr = np.array(arr).astype(int)

		self.n_rows = arr[0][0]
		self.n_cols = arr[0][1]
		self.n_cars = arr[0][2]
		self.n_rides = arr[0][3]
		self.bonus = arr[0][4]
		self.n_steps = arr[0][5]

		arr = arr[1:]
		start_locs = arr[:,0:2]
		end_locs = arr[:,2:4]
		start_times = arr[:,4]
		end_times = arr[:,5]

		self.cars = [Car(i) for i in range(self.n_cars)] # create list of cars. i is the ID of the car
		self.rides = [Ride(i, start_locs[i], end_locs[i], start_times[i], end_times[i]) for i in range(self.n_rides)]
		self.rides_status = {i:False for i in range(self.n_rides)}

		self.time_step = 0

		self.ride_assignments = {} # job_number : car_number


	def step(self):
		available_cars = self.get_available_cars()
		# print('available: {}'.format([car.id for car in available_cars]))
		if len(available_cars) < 1:
			self.time_step += 1
			# print('no available cars')
			return

		assignments = self.assign_cars(available_cars)
		# print(self.rides_status)
		self.time_step += 1

	def get_available_cars(self):
		available_cars = []
		for car in self.cars:
			if car.get_availability(self.time_step):
				available_cars.append(car)

		return available_cars

	def get_unassigned_rides(self):
		unassigned_rides = []
		for ride_id, assigned in self.rides_status.items():
			if not assigned:
				unassigned_rides.append(self.rides[ride_id])
		return unassigned_rides

	def assign_cars(self, available_cars):
		n_available = len(available_cars)

		unassigned_rides = self.get_unassigned_rides()
		n_unassigned_rides = len(unassigned_rides)
		if n_unassigned_rides == 0:
			# print('no rides to assign')
			return

		# the assignments dictionary. {car_object : ride_object}
		assignments = {}

		# RUN POLICY TO POPULATE ASSIGNMENTS
		heuristic_scores = [[0 for i in range(n_unassigned_rides)] for j in range(n_available)]
		for c in range(n_available):
			for r in range(n_unassigned_rides):
				""" TO DO: score calculation """
				score = self.calculate_score(available_cars[c], unassigned_rides[r])
				heuristic_scores[c][r] = score

		if len(heuristic_scores) < 1:
			return
		indices = self.get_best_indices(heuristic_scores)
		for i, j in indices:
			assignments[available_cars[i]] = unassigned_rides[j]
			# print('setting ride {} to done'.format(j))
			self.rides_status[unassigned_rides[j].id] = True

		# send assignments to the car objects
		for car in available_cars:
			assigned_ride = assignments.get(car)
			if assigned_ride:
				# print('{} getting assigned {}.'.format(car.id, assigned_ride.id))
				car.receive_assignment(assigned_ride) # car object keeps track of history

		return assignments

	def calculate_score(self, car, ride):
		hscore = 0.0
		fulfilment = 0.0
		bonus = 0.0
		efficiency = 0.0
		#whether it can fulfil the ride
		car_location = car.get_location()
		time_pickup = abs(car_location[0]-ride.start_loc[0]) + abs(car_location[1]-ride.start_loc[1])
		time_ride = abs(ride.end_loc[0]-ride.start_loc[0]) + abs(ride.end_loc[1]-ride.start_loc[1])
		time_total = time_pickup + time_ride
		if (time_total + self.time_step) <= ride.end_time:
			fulfilment = 1.0
		#whether got bonus
		if fulfilment != 0.0:
			if (self.time_step + time_pickup) == ride.start_time:
				bonus = 1.0
		#efficiency
		if fulfilment != 0.0:
			efficiency = time_ride/time_total

		hscore = 1/(time_pickup+1)
		return hscore

	def get_best_indices(self, matrix):

		matrix = np.array(matrix)
		if matrix.shape[0] > matrix.shape[1]:
			matrix = matrix.T
			flipped = True
		else:
			flipped = False

		index_i = []
		index_j = []

		for i in range(matrix.shape[0]):
			index = np.argmax(matrix[i])
			matrix[:, index] = -1000000
			index_i.append(i)
			index_j.append(index)

		if not flipped:
			return [(index_i[a], index_j[a]) for a in range(matrix.shape[0])]
		else:
			return [(index_j[a], index_i[a]) for a in range(matrix.shape[0])]


		# cost_matrix = []
		# for row in matrix:
		# 	cost_row = []
		# 	for col in row:
		# 		cost_row += [sys.maxsize - col]
		# 	cost_matrix += [cost_row]
		# m = Munkres()
		# indices = m.compute(cost_matrix)
		# total = 0
		return indices

	def run_simulation(self):
		for t in tqdm(range(self.n_steps)):
			# print('Time step {} to {}'.format(self.time_step, self.time_step+1))
			self.step()

	def get_score(self):
		pass

	def get_submission(self):
		submission = []
		for car in self.cars:
			submission.append(car.get_history())

		submission = '\n'.join(submission)
		with open('submission.txt', 'w') as f:
			f.write(submission)


if __name__ == '__main__':
	# file_path = 'b_should_be_easy.in'
	# file_path = 'a_example.in'
	# file_path = 'c_no_hurry.in'
	# file_path = 'd_metropolis.in'
	file_path = 'e_high_bonus.in'
	simulation = Simulation(file_path)
	simulation.run_simulation()

	score = simulation.get_score()
	simulation.get_submission()

