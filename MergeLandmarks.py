#---Merge landmarks into a single CSV file formated for Mathematica or R---
# Anne Kort

# Prepartion for this program
# Export Slicer landmarks into a folder with nothing else
# Change the file extensions for the landmarks exported from Slicer to CSV
# Open a command prompt and set the directory to the folder with the landmarks
# run the command>ren *.fcsv *.csv

#---------Libraries---------------

import pandas as pd
import os
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

#---------Functions---------------

# Strip the first two lines of the .fcsv format
def fcsvStrip(fcsv):
    """Strips the first line, the column IDs
of an csv exported from 3D Slicer"""
    f = open(fcsv, "r")
    lines = f.readlines()
    f.close()
    lines.remove(lines[0])
    lines.remove(lines[0])
    lines.remove(lines[0])
    lines.insert(0,"colID,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,,,desc,associatedNodeID\n")
    f = open(fcsv, "w")
    f.writelines(lines)
    f.close()

def getCoord(data, axis=str, landmark=int):
    """Returns the coordinate of a particular axis (x,y,z) and landmark
from a specified dataframe"""
    coord = data.loc[landmark,axis]
    return float(coord)
    


#--------Prepare Data Frames------------------

# Set landmark directory
direct = "C:\\Users\\aelko\Desktop\\ExampleSemiLandmarks\\ToR"
print("Current directory: ")
print(direct)
newDiryn = input("Change directory? ")
if "y" in newDiryn.lower():
    direct = input("Enter the landmark file directory with double slashes \n")
os.chdir(direct)

# Pull list of file names from directory
fcsvFiles = os.listdir(direct)
fcsvFiles.remove('MergeLandmarks.py')
if "landmarks.csv" in fcsvFiles:
    fcsvFiles.remove('landmarks.csv')

#Strip the first 2 lines of each file
stripyn = input("Strip the first two lines? Enter Y or N:  ")
if "y" in stripyn.lower():
    for fcsv in fcsvFiles:
        fcsvStrip(fcsv)

# Import the fcsv files as a set of pandas dataframes
dataframes = []
specimens = []
for fcsv in fcsvFiles:
    dataframes.append(pd.read_csv(fcsv,usecols=[0,1,2,3]))
    specimens.append(fcsv[:-4])

# Create an empty main dataframe
mainData = pd.DataFrame()

# Append new labels to the new dataframe
mainData['specimen']=specimens


# -------------Arrange landmarks in proper order----------------------

# Get number of landmarks
landNum = int(input("Number of Landmarks:  "))

# Create new columns for coordinate rearrangement
colums = []
for i in range(0,landNum):
    colums.append('x'+str(i+1))
    colums.append('y'+str(i+1))
    colums.append('z'+str(i+1))

mainData[colums]=1

# Fill in coordinates
count = 0
for dataframe in dataframes:
    for i in range(0,landNum):
        xCoord = getCoord(dataframe, 'x', i)
        yCoord = getCoord(dataframe, 'y', i)
        zCoord = getCoord(dataframe, 'z', i)
        mainData.loc[count,'x'+str(i+1)] = float(xCoord)
        mainData.loc[count,'y'+str(i+1)] = float(yCoord)
        mainData.loc[count,'z'+str(i+1)] = float(zCoord)
    count = count + 1

#--------------Export--------------

mainData.to_csv('landmarks.csv',header=False,index=False)



