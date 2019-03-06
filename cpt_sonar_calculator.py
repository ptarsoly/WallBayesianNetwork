import csv
import sys
import os
import numpy as np

fieldnames = ['runid', 'column', 'row', 'orientation', 'headOrientationYaw', 'actualYawU', 'actualPitchU', 'actualYawL', 'actualPitchL', 'leftSonar', 'rightSonar', 'alpha1U', 'beta1U',
              'dalU', 'db1U', 'nb1U', 'alpha2U', 'beta2U', 'da2U', 'db2U', 'nb2U', 'tU', 'NU', 'alpha1L', 'beta1L', 'dalL', 'db1L', 'nb1L', 'alpha2L', 'beta2L', 'da2L', 'db2L', 'nb2L', 'tL', 'NL']

meter_to_inch_conversion = 39.37

sensor_folder = 'sensor_data'

numRows, numCols = 8, 4

left_samples = [[[] for x in range(numCols)] for y in range(numRows)]
right_samples = [[[] for x in range(numCols)] for y in range(numRows)]


for dataFile in os.listdir('sensor_data'):
    
    with open(os.path.join(sensor_folder, dataFile)) as csvfile:
        dataReader = csv.reader(csvfile)
        sensorDataList = map(tuple, dataReader)
        left_samples_per_round = [[[] for x in range(numCols)] for y in range(numRows)]
        right_samples_per_round = [[[] for x in range(numCols)] for y in range(numRows)]
        for row in sensorDataList:
            # Every other row is all columns so ignore those
            if row[1]:
                colNum = int(row[1])
                rowNum = int(row[2])
                if row[3] == 'S':
                    # print(str(float(row[9])*meter_to_inch_conversion) +
                    #       ", "+str(float(row[10])*meter_to_inch_conversion))
                    left_samples_per_round[int(row[1]), int(row[2])].append(float(row[9])*meter_to_inch_conversion)
                    right_samples_per_round[int(row[1]), int(row[2])].append(float(row[10])*meter_to_inch_conversion)

        print(np.ndarray(left_samples_per_round).shape)
        left_samples.extend(left_samples_per_round)
        right_samples.extend(right_samples_per_round)
        
        left_samples_per_round = []
        right_samples_per_round = []
        # print("end of file")

left = np.array(left_samples)
right = np.array(right_samples)

print("Average left: "+str(np.average(left)))
print("Average right: "+str(np.average(right)))
print("Variance left: "+str(np.var(left)))
print("Variance right: "+str(np.var(right)))