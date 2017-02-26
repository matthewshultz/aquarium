#-----------------------------------------------------------------------------------------
# Name:          readTempHumidSensors.py
# Script will take sensor readings and write them to file
#-----------------------------------------------------------------------------------------

#import basic functions
import sys
import os
import csv
import matplotlib.pyplot as plt
import os
from datetime import datetime

print "may have goofed the matplotlib install, its acting funny"

def grabDataDict(filename):
    """Extract the data from the text files
    
    """
    #read in the files as a dictionary
    f = open(filename,'rb')
    dataList=[]
    inputfile = csv.DictReader(f)
    for row in inputfile:
        dataList .append(row)
    return dataList
    
def plotData(dataList,configuredTemp):
    """Plot the given data list
    
    """
    plt.figure()
    dateTime=[]
    waterTemp=[]
    ambientTemp=[]
    for data in dataList:
        #plot the water temperature
        dateTime.append(datetime.strptime(data['dateTime_Local'],"%Y%m%d_%H%M%S"))
        waterTemp.append(float(data['waterTemp_degc']))
        ambientTemp.append(float(data['ambientTemp_degc']))

    plt.plot(dateTime,waterTemp,'b', label = 'Water Temperature')
    plt.plot(dateTime,ambientTemp,'g', label = 'Ambient Temperature')
    #plot the configured temperature
    plt.legend()
    plt.plot([dateTime[0],dateTime[-1]],[configuredTemp,configuredTemp],'k')
        
        
    plt.show()

def main():
    """Main function to call process
    
    """
    daysOfDataToPlot = 3
    dataDirectory = '/media/pi/UNTITLED/aquarium/data'
    configuredTemp = 26
    print daysOfDataToPlot
    dataFileList = os.listdir(dataDirectory)
    
    #Read in data
    dataList = []
    for dataFile in dataFileList:
        dataFilePath = os.path.join(dataDirectory,dataFile)
        dataList_day = grabDataDict(dataFilePath)
        dataList = dataList + dataList_day
    
    plotData(dataList,configuredTemp)
    
if __name__ == '__main__':
    main()
