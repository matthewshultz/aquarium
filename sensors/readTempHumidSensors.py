#-----------------------------------------------------------------------------------------
# Name:          readTempHumidSensors.py
# Script will take sensor readings and write them to file
#-----------------------------------------------------------------------------------------

#import basic functions
import sys
import datetime
import os
import Adafruit_DHT
import subprocess

#Config
#ToDo: move config to ini file
#ToDo: have an accellerated logging function if requried
outDirectory = '/media/pi/UNTITLED/aquarium/data'
outFilePrefix = 'datalog'
logDirectory = '/home/pi/aquarium/sensors/config/logging.config'
def writeDataToFile(outDirectory,outline,outfileName):
    #create the desired file path
    outfilePath = os.path.join(outDirectory,outfileName)
    if os.path.isfile(outfilePath):
        #write the data to file
        with open (outfilePath,"a") as f:
            f.write(outline)
    else:
        with open(outfilePath,"w+") as f:
            header = "dateTime_Local,ambientTemp_degc,ambient_humidity,waterTemp_degc\n"
            f.write(header)
            f.write(outline)
    
def measureWaterTemperature():
    os.chdir("/sys/bus/w1/devices/28-00000606294f/")
    #test =os.system("sudo cat w1_slave")
    #test,output =commands.getstatusoutput("sudo cat w1_slave")
    result = subprocess.Popen(["sudo cat w1_slave"],stdout=subprocess.PIPE,shell=True)
    (out,err) = result.communicate()
    
    waterTemp_degc =  float(str(out).split('t=')[1])/1000
    return waterTemp_degc

def main():
    
    #ToDo: get the appropriate config values
    
    #get the appropriate time values
    time = datetime.datetime.now()
    #print str(time)
    
    #get the ambient temperature
    ambient_humidity, ambient_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,17)
    
    #get the underwater temperature
    #ToDo: move to function
    
    waterTemp_degc = measureWaterTemperature()
    #waterTemp_degc =999
    
    #waterTemp_degc =test
    timeString = time.strftime("%Y%m%d_%H%M%S")
    outfileName = outFilePrefix + timeString.split("_")[0] +'.csv'
    
    #format the data so we can write it to file
    outline =   timeString+','+str("{:.1f}".format(ambient_temperature))+','\
    +str("{:.1f}".format(ambient_humidity))+','+str("{:.1f}".format(waterTemp_degc))+'\n'
 
    writeDataToFile(outDirectory,outline,outfileName)
    
if __name__ == '__main__':
    main()
