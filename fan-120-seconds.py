import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)
print ("Activating PIN 19")
GPIO.output(19,GPIO.HIGH)
print("Keeping PIN 19 on for 120 seconds, please wait...")
time.sleep(120)
GPIO.output(19,GPIO.LOW)
print("Turning off PIN 19")