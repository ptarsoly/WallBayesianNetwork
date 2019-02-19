import csv
import sys
import os
import time
import math
import operator
# Python Image Library
import Image

from naoqi import ALProxy


def captureLandmarkData(yaw):
    # Captures data from the landmark/vision sensor and returns the data in a tuple
    motionid = motionProxy.post.angleInterpolation(
        ["HeadYaw", "HeadPitch"],
        [[0.00001+yaw, 0.0+yaw, 0.000001+yaw],[0.0, 0.000001]], [[1.0, 1.5, 2.0],[1.0, 3.0]],
        True  # angle, time, absolute (vs relative to current)
        )
    time.sleep(0.5)
    landmarkProxy.pause(False) # not tested
    time.sleep(0.250)
    landmarkProxy.pause(True) # not tested
    hps = getHeadPitch()
    if (abs(math.degrees(hps[0]) > 15.0)):
        print("unacceptable pitch:",math.degrees(hps[0]))
        print("PROGRAM NOW EXITING, DATA FOR THIS ROW WILL BE BAD AND SHOULD BE DELETED")
        sys.exit(-1)
    headYaw = getHeadYaw();

    (alpha1, beta1, da1, db1, nb1, alpha2, beta2, da2, db2, nb2, t, N) = getLandmarkAngles(2);
    print("acceptable head yaw/pitch:",math.degrees(headYaw[0]),math.degrees(hps[0]))
    print("status, N="+str(N),"alpha="+str(math.degrees(alpha1))+"/"+str(math.degrees(alpha2)),"db="+str(math.degrees(db1))+"/"+str(math.degrees(db2)))
    
    return (math.degrees(headYaw[0]), math.degrees(hps[0]), alpha1, beta1, da1, db1, nb1, alpha2, beta2, da2, db2, nb2, t, N)


def getHeadPitch():
    ## return value based on sensors
    hc = motionProxy.getAngles("HeadPitch", False) # requested value
    hs = motionProxy.getAngles("HeadPitch", True)
    #print ("hc=",hc[0], "hs=",hs[0])
    return hs;

def getHeadYaw():
    ## return value based on sensors
    hc = motionProxy.getAngles("HeadYaw", False) # requested value
    hs = motionProxy.getAngles("HeadYaw", True)
    #print ("hc=",hc[0], "hs=",hs[0])
    return hs;

def getLandmarkAngles(i):
    ###
    # Read landmark data if available (at most 2 landmarks at once)
    # By default it reads the closest two, parsed as
    # (alpha1, beta1, da1, db1, mid, alpha2, beta2, da2, db2, mid2, time, N)
    #  mid="mark ID, da="width/delta alpha", db="height/delta beta"
    # When no landmark, returns N=0
    # if i<N returns mark i instead of mark 2
    ###
    data = getLandmarkPosition()
    print("Landmark Data: " + str(data))
    # if there is information in data (at least one mark)
    if (data):
        time = data[0]
        markInfoArray = data[1]
        N = len(markInfoArray)
        markInfo0 = markInfoArray[0]
        # get the angle from the data
        markShapeInfo = markInfo0[0]
        markExtraInfo = markInfo0[1]
        alpha1 = markShapeInfo[1]
        beta1 = markShapeInfo[2]
        da1 = markShapeInfo[3]
        db1 = markShapeInfo[4]
        mid = markExtraInfo[0]
        alpha2 = None
        beta2 = None
        da2 = None
        db2 = None
        mid2 = None
        if (N == 1):
            print("N="+str(N) + " id="+str(mid))
            return (alpha1, beta1, da1, db1, mid, 0, 0, 0, 0, 0, time, N)
        if (N > 1):
            # if index i exists, return it. Otherwise returns index 1
            if (N > i and i > 0): 
                markInfo1 = markInfoArray[i]
            else: 
                markInfo1 = markInfoArray[1]
                markShapeInfo = markInfo1[0]
                markExtraInfo = markInfo1[1]
                alpha2 = markShapeInfo[1]
                beta2 = markShapeInfo[2]
                da2 = markShapeInfo[3]
                db2 = markShapeInfo[4]
                mid2 = markExtraInfo[0]
                print("N="+str(N) + " id="+str(mid)+" "+str(mid2))
            return (alpha1, beta1, da1, db1, mid, alpha2, beta2, da2, db2, mid2, time, N)
    else:
        return (0,0,0,0,0,0,0,0,0,0,0,0)

def getLandmarkPosition():
    ###
    # Looking in memory for the "LandmarkDetected" event
    ###
    return memoryProxy.getData("LandmarkDetected")

def saveNaoImage(camProxy, runid, row, column, orientation, headOrientationYaw, cameraNameUsed):
    """
    First get an image from Nao, then save it to the images folder. The name is based on the passed in orientation data
    """

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0


    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    # Create a PIL Image from our pixel array.
    im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

    # Save the image.
    imageName = str(runid) + "_" + str(column) + "_" + str(row) + "_" + str(orientation) + "_" + str(headOrientationYaw) + "_" + cameraNameUsed + ".png"
    imageRelativePath = os.path.join("images", imageName)
    im.save(imageRelativePath, "PNG")

def subscribeToLandmarks():
    ###
    # subscribe to landmark detection with period 200ms and precision 0.0
    # the precision of 1 is maximim, and 0 is minimum.
    # The period of 30 is default (but we select 200, which is more than enough)
    ###
    landmarkProxy.subscribe("Wall_Mark", 100, 0.0)

ip = "192.168.1.2"
port = 9559
# Connect to ALSonar module.
sonarProxy = ALProxy("ALSonar", ip, port)

# Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
sonarProxy.subscribe("myApplication")

# Now you can retrieve sonar data from ALMemory.
memoryProxy = ALProxy("ALMemory", ip, port)

# Vision/landmark detection  proxy
landmarkProxy = ALProxy("ALLandMarkDetection", ip, port)

# Proxies for walking around/movement/posture
motionProxy = ALProxy("ALMotion", ip, port)
postureProxy = ALProxy("ALRobotPosture", ip, port)

# Proxy for video device
camProxy = ALProxy("ALVideoDevice", ip, port)
resolution = 2    # VGA
colorSpace = 11   # RGB

with open('data.csv', 'a') as csvfile:
    fieldnames = ['runid', 'column','row', 'orientation','headOrientationYaw', 'actualYawU', 'actualPitchU', 'actualYawL', 'actualPitchL', 'leftSonar', 'rightSonar', 'alpha1U', 'beta1U', 'dalU', 'db1U', 'nb1U', 'alpha2U', 'beta2U', 'da2U', 'db2U', 'nb2U', 'tU', 'NU', 'alpha1L', 'beta1L', 'dalL', 'db1L', 'nb1L', 'alpha2L', 'beta2L', 'da2L', 'db2L', 'nb2L', 'tL', 'NL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    runid = raw_input('What is the unique run ID?: ')
    orientation = raw_input('what is the orientation of the body? (L, S, R): ')
    headOrientationYaw = "Init"
    
    postureProxy.goToPosture("StandInit",0.5)
    motionProxy.moveInit()
    motionProxy.setStiffnesses("Head", 1.0)
    if (motionProxy.moveIsActive()):
        print("active move")
        motionProxy.killMove()
        
    print("subscribe landmarks")
    subscribeToLandmarks();
    
    squareSizeInches = 0.0508
    numSquares = 32
    squaresInColumn = (8 if (orientation.upper() == 'S') else 4)
    moveUp = True
    row = 0
    column = 0

    # Loop for the robot to move square positions automatically
    for squareNumber in range (0, numSquares):
        print("squareNumber: " + str(squareNumber))
        # Every 8 or 4 columns we need to move right
        if (squareNumber % squaresInColumn) == 0 and squareNumber != 0:
            print("MOVING RIGHT")
            # Move right
            moveUp = operator.not_(moveUp) # Change to move opposite direction up/down now
            motionProxy.moveTo(0.0, (squareSizeInches * -1.0), 0.0)
            column = column + 1
        elif squareNumber != 0:
            print("MOVING UP OR DOWN")
            # move up/down
            yDistance = squareSizeInches
            if not moveUp:
                yDistance = yDistance * -1.0
                row = row - 1
            else:
                row = row + 1
            motionProxy.moveTo(yDistance, 0.0, 0.0)
            
        # Wait for movement
        time.sleep(1)
        
        print("Nao should be at column, row: (" + str(column) + "," + str(row) + ")")
        
        # Loops and gathers data at different head angles
        for loopCount in range(-9,10):
        #for loopCount in range(0,1):
            yaw = math.radians(loopCount * 5)  # yaw desired for head (when body turning not desired)
            headOrientationYaw = str(yaw)
            print("init head yaw: " + headOrientationYaw)
            motionProxy.angleInterpolationWithSpeed("Head", [yaw, 0.0], 1.0)
            landmarkProxy.pause(True) # not tested
            
            videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

            # Capture landmark data and image using upper camera
            camProxy.setActiveCamera(0)
            activeCameraIndex = camProxy.getActiveCamera()
            cameraNameUsed = camProxy.getCameraName(activeCameraIndex)
            
            print("Looking using camera: " + cameraNameUsed)
            (actualYawU, actualPitchU, alpha1U, beta1U, da1U, db1U, nb1U, alpha2U, beta2U, da2U, db2U, nb2U, tU, NU) = captureLandmarkData(yaw)
        
            # Save image from video output every third time the Nao rotates his head
            if loopCount % 3 == 0:
                saveNaoImage(camProxy, runid, row, column, orientation, headOrientationYaw, cameraNameUsed)
            
            # Do a second round using the lower camera
            camProxy.setActiveCamera(1)
            activeCameraIndex = camProxy.getActiveCamera()
            cameraNameUsed = camProxy.getCameraName(activeCameraIndex)
            
            print("Looking using camera: " + cameraNameUsed)
            (actualYawL, actualPitchL, alpha1L, beta1L, da1L, db1L, nb1L, alpha2L, beta2L, da2L, db2L, nb2L, tL, NL) = captureLandmarkData(yaw)
            
            # Save image from video output every third time the Nao rotates his head
            if loopCount % 3 == 0:
                saveNaoImage(camProxy, runid, row, column, orientation, headOrientationYaw, cameraNameUsed)
            
            camProxy.setActiveCamera(0) # Set back to the first one which is default
            
            camProxy.unsubscribe(videoClient)
            
            # Get sonar left first echo (distance in meters to the first obstacle).
            leftSonar = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            print("left sonar: " + str(leftSonar))

            # Same thing for right.
            rightSonar = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            print("right sonar: " + str(rightSonar))

            writer.writerow({'runid': runid, 'column': column, 'row': row, 'orientation':orientation, 'headOrientationYaw':headOrientationYaw, 'actualYawU':actualYawU, 'actualPitchU':actualPitchU,'actualYawL':actualYawL, 'actualPitchL':actualPitchL, 'leftSonar':leftSonar, 'rightSonar':rightSonar, 'alpha1U':alpha1U, 'beta1U':beta1U, 'dalU':da1U, 'db1U':db1U, 'nb1U':nb1U, 'alpha2U':alpha2U, 'beta2U':beta2U, 'da2U':da2U, 'db2U':db2U, 'nb2U':nb2U, 'tU':tU, 'NU':NU, 'alpha1L':alpha1L, 'beta1L':beta1L, 'dalL':da1L, 'db1L':db1L, 'nb1L':nb1L, 'alpha2L':alpha2L, 'beta2L':beta2L, 'da2L':da2L, 'db2L':db2L, 'nb2L':nb2L, 'tL':tL, 'NL':NL})
