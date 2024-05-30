#---Merge landmarks into a single CSV file formated for Mathematica---
# Anne Kort -- aekort@iu.edu

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
#of an csv exported from 3D Slicer"""
    f = open(fcsv, "r")
    lines = f.readlines()
    f.close()
    lines.remove(lines[0])
    f = open(fcsv, "w")
    f.writelines(lines)
    f.close()

def dropColumns(data):
    """Deletes the unneeded columns from a csv dataset"""
    dropcol=["ow","ox","oy","oz","vis","sel","lock","label","desc","associatedNodeID"]
    for col in dropcol:
        data.drop(col, inplace=True, axis=1)

def getAnimal(data):
    """Gets the animal name from the label in the dataframe"""
    label = data.loc[2,'label']
    labelList = label.split("-")
    animalLabel = labelList[0]+"_"+labelList[1]
    return animalLabel

def getCoord(data, axis=str, landmark=int):
    """Returns the coordinate of a particular axis (x,y,z) and landmark
from a specified dataframe"""
    coord = data.loc[landmark,axis]
    return float(coord)
    



#--------Prepare Data Frames------------------

# Set landmark directory
direct = "C:\\Users\\aelko\Desktop\\landmarks\\ToR"
print("Current directory: ")
print(direct)
newDiryn = input("Change directory? ")
if "y" in newDiryn.lower():
    direct = input("Enter the landmark file directory with double slashes \n")
os.chdir(direct)

# Pull list of file names from directory
fcsvFiles = os.listdir(direct)
fcsvFiles.remove('MergeLandmarks2.0.py')
if "landmarks.csv" in fcsvFiles:
    fcsvFiles.remove('landmarks.csv')
for fcsv in fcsvFiles:
    if "schema" in fcsv:
        fcsvFiles.remove(fcsv)

#Strip the first 2 lines of each file
stripyn = input("Strip the first two lines? Enter Y or N:  ")
#if "y" in stripyn.lower():
    #for fcsv in fcsvFiles:
        #fcsvStrip(fcsv)

# Import the fcsv files as a set of pandas dataframes
dataframes = []
animals = []
for fcsv in fcsvFiles:
    dataframes.append(pd.read_csv(fcsv))
    animals.append(fcsv[:-4])

# Delete unneeded columns, saving only the coordinates and label
for dataframe in dataframes:
    dropColumns(dataframe)

# Create an empty main dataframe
mainData = pd.DataFrame()


# Append new labels to the new dataframe
mainData['animal']=animals


# -------------Arrange landmarks in proper order----------------------

# Get number of landmarks
landNum = 158#len(dataframes[0])

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

