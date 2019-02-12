from naoqi import ALProxy
import time

IP = "192.168.1.4"
PORT = 9559
# Create a proxy to ALLandMarkDetection
try:
    markProxy = ALProxy("ALLandMarkDetection", IP, PORT)
except Exception, e:
  print "Error when creating landmark detection proxy:"
  print str(e)
  exit(1)

# Subscribe to the ALLandMarkDetection extractor
period = 500
markProxy.subscribe("Test_Mark", period, 0.0 )


# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)


print "Creating landmark detection proxy"

# A simple loop that reads the memValue "LandmarkDetected" and checks
# whether landmarks are detected.
for i in range(0, 20):
    time.sleep(0.5)
    val = memoryProxy.getData("LandmarkDetected", 0)
    print ""
    print "\*****"
    print ""
    # Check whether we got a valid output: a list with two fields.
    if(val and isinstance(val, list) and len(val) >= 2):
      # We detected landmarks !
      # For each mark, we can read its shape info and ID.
      # First Field = TimeStamp.
      timeStamp = val[0]
      # Second Field = array of Mark_Info's.
      markInfoArray = val[1]

      try:
        # Browse the markInfoArray to get info on each detected mark.
        for markInfo in markInfoArray:
          # First Field = Shape info.
          markShapeInfo = markInfo[0]
          # Second Field = Extra info (i.e., mark ID).
          markExtraInfo = markInfo[1]
          # Print Mark information.
          print "mark  ID: %d" % (markExtraInfo[0])
          print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
          print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])
      except Exception, e:
          print "Landmarks detected, but it seems getData is invalid. ALValue ="
          print val
          print "Error msg %s" % (str(e))
    else:
      print "Error with getData. ALValue = %s" % (str(val))

# Unsubscribe from the module.
markProxy.unsubscribe("Test_Mark")
print "Test terminated successfully."