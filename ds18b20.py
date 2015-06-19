"""
Python class for the DS18B20 temperature sensor, based on code by Adafruit Industries by ThreeSixes (https://github.com/ThreeSixes/py-ds18b20)

Original Adafruit Code:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
"""

import glob
import time
import subprocess

"""
Class for the DS18B20 temperature sensor module, based on caode from Adafruit Industries:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
"""
class ds18b20:
    
    """
    Class constructor.
    """
    def __init__(self):
        # Max polling rate is 0.750 seconds.
        self.minPoll = 0.750
        
        # Configuration for the /sys nodes
        baseDir = '/sys/bus/w1/devices/'
        deviceFolder = glob.glob(baseDir + '28*')[0]
        self.deviceFile = deviceFolder + '/w1_slave'

   
    """
    Read raw temperature values from the /sys node for the sensor.
    """
    def __readTempRaw(self):
        
        # Read data from the nodes
        try:
            catData = subprocess.Popen(['cat', self.deviceFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = catData.communicate()
        except Exception as e:
            raise e
        
        # Encode as UTF-8 and split into an array.
        outDecode = out.decode('utf-8')
        lines = outDecode.split('\n')
        
        return lines
 
    """
    Read temperature value from the sensor. Returns a float representing teperature in degrees Celcius.
    """
    def readTemp(self):
        lines = self.__readTempRaw()
        tempC = -9999.9
        
        # Raise an exception if we have bad CRC data.
        if lines[0].find('YES') < 0:
            raise ValueError("Bad CRC value from DS18B20 at " + self.deviceFile)
        
        # Find the chunk of the second line that represents the temperature.
        equalsPos = lines[1].find('t=')
        
        # If the temperature isn't missing read the data.
        if equalsPos != -1:
            tempString = lines[1][equalsPos+2:]
            tempC = float(tempString) / 1000.0
        else:
            raise IOError("Missing temperature data from DS18B20 at " + self.deviceFile)
        
        return tempC
