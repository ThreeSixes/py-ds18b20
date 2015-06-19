"""
Python DS18B20 test code by ThreeSixes (https://github.com/ThreeSixes/py-ds18b20)
"""

from ds18b20 import ds18b20
from pprint import pprint
import time

"""
Test class
"""
class ds18B20Test:
    def __init__(self):
        # Create our temperature sensor instance.
        self.tempSens = ds18b20()

    """
    Continuous temperature test and wait for the min poll time to read the sensor again.
    """
    def continuousReading(self):
        # Continuously read the temperature from the sensor.
        while True:
            self.singleReading()
            
            # Wait a for the minimum time we can before polling again.
            time.sleep(self.tempSens.minPoll)

    """
    Single reading test
    """
    def singleReading(self):
        try:
            print(str(self.tempSens.readTemp()) + "C")
        except ValueError as e:
            print "CRC error:"
            pprint(e)
        except IOError as e:
            print "Temp data missing:"
            pprint(e)

# Create our sensor instance.
myTest = ds18B20Test()

# Take a single reading
print ("Single reading test and wait 1 second before dropping into continuous mode.")
myTest.singleReading()
time.sleep(1)

# Now read continuously.
print("Reading continuously...")
myTest.continuousReading()