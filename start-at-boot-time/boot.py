import os
from datetime import datetime
import datetime
import time

today = str(datetime.datetime.utcnow()) + "\r\n"

print("Today's date:", today)

f = open("logger.txt", "a+")
f.write(today)
f.close()