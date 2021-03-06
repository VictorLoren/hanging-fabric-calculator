#calculate the length of a hanging strand of weighted material

# RectRoom object to hang material in
class RectRoom(object):
    '''
        RectRoom(length,width,height,units='feet') initiates object that 
        represents a rectangular room in which material will be hung in.
        
        Automatically declares a midpoint of the room to hang fabric from as a 
        Point object: self.hangFrom
    '''
    def __init__(self,length,width,height,units='feet'):
        self.length = length
        self.width  = width
        self.height = height
        self.hangFrom = Point(width/2.0,length/2.0,float(height))
        self.units  = units

# Point to represent some vertex in 3D space
class Point(object):
    # Construct with 3 axes in mind
    def __init__(self,x,y,z=0):
       # Assign coordinates of the point for all three axes
       (self.x, self.y, self.z) = (x,y,z)
       # Shortcut to full position coordinates
       self.pt = (x,y,z)
    # Addition and subtraction
    def __add__(self,pt):
       return Point(self.x+pt.x,self.y+pt.y,self.z+pt.z)
    def __iadd__(self,pt):
       self.x += pt.x
       self.y += pt.y
       self.z += pt.z
       return self
    def __sub__(self,pt):
        return Point(self.x-pt.x,self.y-pt.y,self.z-pt.z)
    def __iadd__(self,pt):
        self.x -= pt.x
        self.y -= pt.y
        self.z -= pt.z
        return self
    # Printing object
    def __repr__(self):
        return "(%f,%f,%f)" %(self.x,self.y,self.z)
    def __str__(self):
        return "(%f,%f,%f)" %(self.x,self.y,self.z)

# Define a RectRoom (in feet)
gym = RectRoom(length=92,width=68,height=22)

# Find a matching parabola with 3 points in x-y-plane (only 3 ince deg(y)=1)
def findParabola(p0,p1,p2):
    # Always of the form y = a * x^2 + b * x + c
    fcoeffs = lambda x,y : (x*x , x , 1, y)
    # Map points to arrays of coeffecients (variable array, solution array) 
    arr0 = fcoeffs(p0.x,p0.y)
    arr1 = fcoeffs(p1.x,p1.y)
    arr2 = fcoeffs(p2.x,p2.y)
    # Solve system of equations
    from numpy import array as npArray
    from numpy.linalg import solve
    # Varaible arrary
    arrV = npArray([
                    arr0[0:-1], 
                    arr1[0:-1],
                    arr2[0:-1]
                    ])
    # Solution array ... = arrS
    arrS = npArray([arr0[3],arr1[3],arr2[3]])
    coeff = solve(arrV,arrS)
    # Give the parameters needed to construct parabola (a,b,c) for y=ax^2+bx+c
    return coeff

# Find arc length of a parabola defined by three points given
def findArcLength(fromPoint,toPoint,definePt):
    # Rename the parameters given for brevity
    p0,p1,p2 = fromPoint, toPoint, definePt
    # Get the parameters that describe the parabola (ax^2+bx+c)
    (a,b,c) = findParabola(p0,p1,p2)
    # Import basic integrating tool
    from scipy.integrate import quad as integrate
    # Function for the arc length integrand: Sqrt(1+[y']^2)
    from numpy import sqrt
    func = lambda x : sqrt( 1 + (2*a*x + b) * (2*a*x + b) )
    # Integrate to find arc length
    arcLength = integrate(func,p0.x,p1.x)[0]
    return arcLength

# Convert two 3D points to a 2D plane (keep z as y)
def convertCoordinates(p0,p1):
	from numpy import sqrt
	# New Coordinates are x,y away from first
	dx = p1.x - p0.x
	dy = p1.y - p0.y
	dz = p1.z - p0.z
	x = sqrt(dx*dx + dy*dy)
	y = dz
	return (Point(0,0,0) , Point(x,y,0))

def calcLength(startPt,endPt,detailPt):#(x,y,z=0):
    #For better accuracy, will need to compute the droop (catenary)
    # Basic calculation of strand length (assume a straight line) 
    #strandLength = (x**2 + y**2 + z**2)**0.5
    strandLength = findArcLength(startPt,endPt,detailPt) 
    return strandLength

def feetToYards(inFeet):
    return inFeet/3.0

def yardsToFeet(inYards):
    return inYards * 3.0

#widthOfStrand is how wide the tulle piece (in feet)
def findTotal(widthOfStrand,z=0,dOut=1,dUp=1,room=gym,printTotal=False):
    '''
    Find total in yards.
    Input:
        widthOfStrand (number of feet, width of material)
        z=0 (how many feet it will start from above the floor)
        dOut=1, dUp=1 (how many feet material drapes away from and above wall)
        room=gym (RectRoom object to hang material in)
        printTotal=False (Friendly print)

    Output:
        tuple -> 
               The length needed (in yards),
               list of strand lengths (in yards)
    '''
    #Length of each break points
    strandLengths = []
    #Total length
    total = 0

    # Point definitions
    startPt  = Point(0,0,0) + Point(0,0,z) # raise the point up by z
    endPt = room.hangFrom #where the material will end at (ex hung in center)

    #find along width
    alongWidth = 0
    while(alongWidth <= room.width):
        fromPt = Point(alongWidth,0) + startPt #move start to the right
        # Find length (in 2D xz-plane)
        # Convert the points to its own xy-plane
        p0,p1 = convertCoordinates(fromPt,endPt) # Convert to its own xy-plane
        p2 = p0 + Point(dOut,dUp) #get a point away from the start
        strandLength = calcLength(p0,p1,p2)

        # Add Break point length
        strandLengths.append(strandLength)
        # Total length
        total += strandLength 
        alongWidth += widthOfStrand

    #find along length, around gym
    fromPt = startPt #initiate in corner
    alongLength = 0 
    while(alongLength <= room.length):
        # Length of strand needed (in yards)
        fromPt = Point(0,alongLength) + startPt #move start along wall (down the length)
        # Find length (in 2D xz-plane)
        # Convert the points to its own xy-plane 
        p0,p1 = convertCoordinates(fromPt,endPt) # Convert to its own xy-plane
        p2 = p0 + Point(dOut,dUp) #get a point away from the start
        strandLength = calcLength(p0,p1,p2)

        # Add Break point length
        strandLengths.append(strandLength)
        # Total length
        total += strandLength
        alongLength += widthOfStrand

    #convert to yards
    total = feetToYards(total)
    strandLengths = map(feetToYards,strandLengths)
    # All the strand lengths and sorted
    strandLengths *= 2; strandLengths.sort()
    if printTotal:
        print '\nTotal Length For Room: %.2f yards' %(2*total)
    # Return total length in yards and a list of strand lengths needed
    return (2*total , strandLengths)

def totalCost(costPerYard,widthOfStrandInFeet,drapingInFeet,printTotal=False):
    total = findTotal(widthOfStrandInFeet,drapingInFeet,printTotal)
    cost = total * costPerYard
    print "Total length %.2f yards for $%.2f (@ $%.2f per yard)" %(total,cost,costPerYard)
    return cost

print "Imported 'tulle'"
