import csv
from naoqi import ALProxy


ip = "192.168.1.4"
# Connect to ALSonar module.
sonarProxy = ALProxy("ALSonar", ip, 9559)

# Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
sonarProxy.subscribe("myApplication")

# Now you can retrieve sonar data from ALMemory.
memoryProxy = ALProxy("ALMemory", ip, 9559)

with open('data.csv', 'a') as csvfile:
    fieldnames = ['centerWall','rightWall','leftWall','orientation','headOrientation','leftSonar', 'rightSonar']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    centerWall = input('How many inches away is NAO from the center wall?')
    rightWall = input('How many inches away is NAO from the right wall?')
    leftWall = input('How many inches away is NAO from the left wall?')
    orientation = input('what is the orientation of the body?')


    # Get sonar left first echo (distance in meters to the first obstacle).
    leftSonar = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")

    # Same thing for right.
    rightSonar = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    writer.writerow({'centerWall': centerWall, 'rightWall': rightWall, 'leftWall': leftWall, 'orientation':orientation, 'headOrientation':headOrientation, 'leftSonar':leftSonar,'rightSonar':rightSonar})
