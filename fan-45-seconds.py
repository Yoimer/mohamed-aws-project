import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)
print ("Activating PIN 19")
GPIO.output(19,GPIO.HIGH)
print("Keeping PIN 19 on for 45 seconds, please wait...")
time.sleep(45)
GPIO.output(19,GPIO.LOW)
print("Turning off PIN 19")