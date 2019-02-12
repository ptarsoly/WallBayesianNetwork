# Creates a proxy on the text-to-speech module
from naoqi import ALProxy

IP = "192.168.1.4"
tts = ALProxy("ALTextToSpeech", IP, 9559)

# Example: Sends a string to the text-to-speech module
tts.say("Why can't I find landmarks!")