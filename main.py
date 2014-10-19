## Import the module
from tulle import *;

## Defining what unit to use
unitStr = "feet"

## Defining the room to hang material in
width  = float(raw_input("How wide is the room (in %s)? " %unitStr))
length = float(raw_input("How long is the room (in %s)? " %unitStr))
height = float(raw_input("How high is the room (in %s)? " %unitStr))
# Create room instance
room = RectRoom(length=length, width=width, height=height, units=unitStr)

## Get the defining shape of the hanging material
# Width of the strand
strand = float(raw_input("What is the width of the hanging material (in %s)? " %unitStr))
# Start material at a certain distance above ground
z = float(raw_input("How high above the ground should the material start from (in %s)? " %unitStr))
# Third point to define hanging shape
thirdPtStr = raw_input("""
How far out 'x' and above 'y' from the starting point of hanging material?
Enter as two numbers (in %s) separated by a comma 'x,y': """ %unitStr)
# Convert to two floats
d_out, d_above = map(float,thirdPtStr.split(','))

## Find amount of material needed
output = findTotal(widthOfStrand=strand, dOut=d_out,dUp= d_above,room=room)
# Totals
total_yds, strandList = output

print "Total number of yards needed: %.2f" %total_yds


