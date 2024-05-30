#---Merge landmarks into a single CSV file formated for Mathematica---
# Anne Kort -- annekort@umich.edu
# Prepartion for this program
# A csv with one "label" column and then the landmarks columns as x1, y1, z1, etc.
# Label the landmarks file "landmarks.csv"
# Create an .fcsv template using an export from Slicer labeled "FCSVTemplate.csv"
# After finishing...
# Open a command prompt and set the directory to the folder with the landmarks
# run the command>ren *.csv *.fcsv

#---------Libraries---------------

import pandas as pd
import os

#---------Functions---------------

# Strip the first two lines of the .fcsv format
def fcsvAddHeader(fcsv):
    """Adds the first two lines, 
of an fcsv exported from 3D Slicer"""
    f = open(fcsv, "r")
    lines = f.readlines()
    f.close()
    lines.insert(0,"# CoordinateSystem = LPS\n")
    lines.insert(0,"# Markups fiducial file version = 5.4\n")
    lines[2]=lines[2][0:-25]+'\n' # Removes the unknown crap generated by pandas
    f = open(fcsv, "w")
    f.writelines(lines)
    f.close()

def makeFCSV(temp,animal):
    """Makes a blank FCSV based on the template"""
    newTemp=temp.copy()
    newTemp.to_csv(label+".csv",header=True,index=False)
    
def getCoord(landmarkList, axis=str, landmark=int):
    """Gets the coordinate of a particular axis (x,y,z) and landmark
from a specified list of landmarks and adds to the template"""
    coord = landmarkList.loc[axis+str(landmark)]
    return coord


#--------Prepare Data Frames------------------

# Set landmark directory
direct = 'C:\\Users\\aelko\\Desktop\\ExampleSemiLandmarks\\Unmerge'
print("Current directory: ")
print(direct)
newDiryn = input("Change directory? ")
if "y" in newDiryn.lower():
    direct = input("Enter the landmark file directory with double slashes \n")
os.chdir(direct)

# Get number of landmarks
landNum = int(input("Number of landmarks? "))

# Import the landmarks and template files
landmarks = pd.read_csv('landmarks.csv')
template = pd.read_csv('FCSVTemplate.csv')

# Get a list of the labels in the landmarks file and set as the index for the dataframe
labels = landmarks['label']
landmarks.set_index(labels,inplace=True)

# -------------Arrange landmarks in proper order----------------------


# Loop through each animal and create a new file based on the template
for label in labels:
    makeFCSV(template,label)

# Loop through each animal and edit the new file with the coordinates
for label in labels:
    fcsvOpen = pd.read_csv(label+'.csv')
    landList=landmarks.loc[label]  #Get a list of the landmarks for that animal
    for i in range(1,landNum+1):
        xCoord=getCoord(landList, 'x', i)
        print(xCoord)
        fcsvOpen.at[i-1,'x']=xCoord
        print(fcsvOpen.at[i-1,'x'])
        yCoord=getCoord(landList, 'y', i)
        fcsvOpen.at[i-1,'y']=yCoord
        zCoord=getCoord(landList, 'z', i)
        fcsvOpen.at[i-1,'z']=zCoord
    fcsvOpen.to_csv(label+".csv",header=True,index=False)
    fcsvAddHeader(label+'.csv')
    
