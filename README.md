# Slicermorph Addon
This is Python code for converting landmark files made in 3D Slicer to a format usable by R.
This is an alternative to the [SlicermorphR package that is made available through the official Slicermorph repository](https://github.com/SlicerMorph/SlicerMorphR).
See my [YouTube channel](https://www.youtube.com/channel/UCJaiHFrVy0wdObYoV-rwXPw) for videos on using Slicermorph.

## Exporting Landmarks from Slicer
Each specimen should have one file with all landmarks. For datasets with points and curves, convert all the curve files to point files and then merge these using the Merge Markups tool that comes with Slicermorph. 
Make sure that ALL landmarks are in the same order for every specimen and that you know which landmarks designate the start and end of each curve.
1. Export landmark files from Slicer as FCSVs. Make the file name a unique identifier for the specimen
2. Put these files in a folder with the MergeLandmarks script and nothing else.
3. Convert the FCSVs to CSVs using Windows Command Prompt (Search for "cmd" in the searchbar).\
    Use the command: `ren *.fcsv *.csv`
4. Double click on the MergeLandmarks python script in the folder and choose the directory when prompted.
5. Strip the first lines (you will be prompted) if you have not run this program on these files before.

**OUTPUT:** A file called landmarks.csv that can be imported into R for use with the geomorph package.

## Returning Landmarks to Slicer
This should be a table formatted as the landmarks.csv is (1 row / specimen) named landmarks.csv.

1. Create a blank FSCV template using your current version of Slicer named "FCSVTemplate.fcsv".
2. Place "landmarks.csv","FCSVTemplate.fcsv", and "UnMergeLandmarks.py" in a folder together.
3. Double click the UnMergeLandmarks script and give the correct directory.
4. Convert the output CSVs to FCSVS using the command: `ren *.csv *.fcsv`. **Note:** you will want to remove landmarks.csv first
