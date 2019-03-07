import csv
import sys
import os
import numpy as np

meter_to_inch_conversion = 39.37

sensor_folder = 'sensor_data'

numRows, numCols = 8, 4

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

# first number is average, second is variance
# these characterize the normal distribution of distance at each square
left_ = [[[0,0] for x in range(numCols)] for y in range(numRows)]
right_samples = [[[0,0] for x in range(numCols)] for y in range(numRows)]

with open('left_sonar_straight_cpt.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        # norm is for each individual normal distribution
        norm = row[0].split(', ')

# for sensor fusion

# print "type in left sonar distance from wall: "
# distance = input()

# maxIndex = [0,0]

# for row in range(numRows):
#     for col in range(numCols):
#         if gaussian(distance, np.average(left_samples[row][col]), np.sqrt(np.var(left_samples[row][col]))) > gaussian(distance, np.average(left_samples[maxIndex[0]][maxIndex[1]]), np.sqrt(np.var(left_samples[maxIndex[0]][maxIndex[1]]))):
#             maxIndex[0] = row
#             maxIndex[1] = col

# print "most likely left distance: ", maxIndex[0]