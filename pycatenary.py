# catenary calculation, re-written in python - NO Elasticity!!!

import math
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import fsolve  


def cat(a):
	# defining catenary function
	#catenary eq (math): a*sinh(L/(2*a)+atanh(d/S))+a*sinh(L/(2*a)-atanh(d/S))-S=0
	return a*math.sinh(L/(2*a))+math.atanh(d/S)+a*math.sinh(L/(2*a))-math.atanh(d/S)-S

L=float(input("Horizontal Distance between supports [m]: "))
d=float(input ("Vertical Distance between supports [m]: "))
S=float(input("Length of cable [m] - must be greater than distance between supports:  "))
w=float(input("Unit weight of cable [kg/m]: "))
za=float(input("Elevation of higher support from reference plane [m]: "))

#checking if cable length is bigger than total distance between supports
distance=(L**2+d**2)**0.5
if S <= distance:
	print ("Length of cable must be greater than TOTAL distance between supports!")
	S=float(input("Length of cable [m]: "))
else:
	pass 

# solving catenary function for 'a'

a=fsolve(cat, 1)

# hor. distance between lowest catenary point (P) to higher support point (La)
La=a*(L/(2*a)+math.atanh(d/S))
# hor. distance between lowest catenary point (P) to lower support point (Lb)
Lb=L-La
# vert. distance from higher support point to lowest point (P) in catenary (ha)
ha=a*math.cosh(La/a)-a
## calculating reaction forces and angles
# catenary lenght between support "A" (higher) and "P" - Sa
Sa=a*math.sinh(La/a)
# catenary lenght between support "B" )lower) and "P" - Sb
Sb=a*math.sinh(Lb/a)
# horizontal tension - constant through catenary: H
H=w*a
# vertical tension at "A"  (Va) and "B" (Vb)
Va=Sa*w
Vb=Sb*w
# tension at "A" (TA) and B (TB)
TA=(H**2+Va**2)**0.5
TB=(H**2+Vb**2)**0.5
# inclination angles from vertical at "A" (ThetA) and B (ThetB)
ThetA=math.atan(H/Va)
ThetB=math.atan(H/Vb)
ThetAd=ThetA*180/math.pi;
ThetBd=ThetB*180/math.pi;
# establishing A, B and P in coordinate system
# index "a" corresponding to point "A", "b" to "B"-point and "P" to lowest caten. point
zb=za-d
zp=za-ha
xa=La
xp=0
xb=-Lb

# printing results to file
print "Horizontal Distance between supports in meters: ", round(L,3)
print "Catenary length in meters: ", round(S,3)
print "Vertical Distance Between supports in meters: ", round(d,3)
print "Unit Weight of Catenary line in kg/m: ", round(w,3)
print "Elevation of higher support (A) from reference plane in meters: ", round(za,3)
print "\Catenary coef.: ", round(a,5)
print "Horizontal tension in kg (constant along line: ", round(H,3)
print "Vertical tension in A in kg: ", round(Va,3)
print "Total tension in A in kg: ", round(TA,3)
print "Total tension in B in kg: ", round(TB,3)
print "Inclination angle from vertical at A in radians: ", round(ThetA,3)
print "Inclination angle from vertical at B in radians: ", round(ThetB,3)
print "Inclination angle from vertical at A in degrees: ", round(ThetAd,3)
print "Inclination angle from vertical at B in degrees: ", round(ThetBd,3)

