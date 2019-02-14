import csv
import sys
import os
import time
# Python Image Library
import Image

from naoqi import ALProxy


def saveNaoImage(IP, PORT, centerWall, rightWall, leftWall, orientation, headOrientation):
    """
    First get an image from Nao, then save it to the images folder. The name is based on the passed in orientation data
    """

    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    camProxy.unsubscribe(videoClient)


    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    # Create a PIL Image from our pixel array.
    im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

    # Save the image.
    imageName = str(centerWall) + "_" + str(rightWall) + "_" + str(leftWall) + "_" + str(orientation) + "_" + str(headOrientation) + ".png"
    imageRelativePath = os.path.join("images", imageName)
    im.save(imageRelativePath, "PNG")

ip = "192.168.1.3"
port = 9559
# Connect to ALSonar module.
sonarProxy = ALProxy("ALSonar", ip, port)

# Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
sonarProxy.subscribe("myApplication")

# Now you can retrieve sonar data from ALMemory.
memoryProxy = ALProxy("ALMemory", ip, port)

with open('data.csv', 'a') as csvfile:
    fieldnames = ['centerWall','rightWall','leftWall','orientation','headOrientation','leftSonar', 'rightSonar']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    centerWall = input('How many inches away is NAO from the center wall?')
    rightWall = input('How many inches away is NAO from the right wall?')
    leftWall = input('How many inches away is NAO from the left wall?')
    orientation = input('what is the orientation of the body?')
    headOrientation = "headOrient"


    # Get sonar left first echo (distance in meters to the first obstacle).
    leftSonar = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")

    # Same thing for right.
    rightSonar = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
	
	# Save imagine from video output
    saveNaoImage(ip, port, centerWall, rightWall, leftWall, orientation, headOrientation)

    writer.writerow({'centerWall': centerWall, 'rightWall': rightWall, 'leftWall': leftWall, 'orientation':orientation, 'headOrientation':headOrientation, 'leftSonar':leftSonar,'rightSonar':rightSonar})
