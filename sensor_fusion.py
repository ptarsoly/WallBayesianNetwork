import csv
import sys
import os
import numpy as np

meter_to_inch_conversion = 39.37

sensor_folder = 'sensor_data'

numRows, numCols = 8, 4


def gaussian(x, mu, var):
    return np.exp(-np.power(x - mu, 2.) / (2 * var))/np.sqrt(2*np.pi*var)


# first number is average, second is variance
# these characterize the normal distribution of distance at each square
left_cpt = []
right_cpt = []

print "loading left sonar CPTs"
with open('left_sonar_straight_cpt.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        # norm is for each individual normal distribution
        norm = map(lambda x: float(x), row[0].split(', '))
        left_cpt.append(norm)
        print norm

print "loading right sonar CPTs"
with open('right_sonar_straight_cpt.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        # norm is for each individual normal distribution
        norm = map(lambda x: float(x), row[0].split(', '))
        right_cpt.append(norm)
        print norm


# for sensor fusion

print "type in left sonar distance from wall: "
left_distance = input()

print "type in right sonar distance from wall: "
right_distance = input()

max_index = 0

for row in range(numRows):
    print "Coordinate", row
    print "Left probability: ", gaussian(left_distance, np.average(left_cpt[row]), np.var(left_cpt[row]))
    print "Right probability: ", gaussian(right_distance, np.average(right_cpt[row]), np.var(right_cpt[row]))
    if gaussian(left_distance, np.average(left_cpt[row]), np.var(left_cpt[row]))*gaussian(right_distance, np.average(right_cpt[row]), np.var(right_cpt[row])) > gaussian(left_distance, np.average(left_cpt[max_index]), np.var(left_cpt[max_index]))*gaussian(right_distance, np.average(right_cpt[max_index]), np.var(right_cpt[max_index])):
        max_index = row

print "most likely distance coordinate: ", max_index
print "most likely distance coordinate left CPT: ", left_cpt[max_index]
print "most likely distance coordinate left probability: ", gaussian(left_distance, np.average(left_cpt[max_index]), np.var(left_cpt[max_index]))
print "most likely distance coordinate right CPT: ", right_cpt[max_index]
print "most likely distance coordinate right probability: ",gaussian(right_distance, np.average(right_cpt[max_index]), np.var(right_cpt[max_index]))