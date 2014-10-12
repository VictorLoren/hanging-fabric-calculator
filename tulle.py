#calculate the length of a hanging strand of weighted material

# RectRoom object to hang material in
class RectRoom(object):
    '''
        RectRoom(length,width,height,units='feet') initiates object that represents a 
        rectangular room in which material will be hung in.
        
        Automatically declares a midpoint of the room to hang fabric from as a 
        Hangpoint object: self.hangFrom
    '''
    def __init__(self,length,width,height,units='feet'):
        self.length = length
        self.width  = width
        self.height = height
        self.hangFrom  = Hangpoint(width/2.0,length/2.0,float(height))
        self.units  = units

# Hangpoint object to represent where to hang material from/to
class Hangpoint(object):
    # Construct with 3 axes in mind
    def __init__(self,x,y,z=0):
       # Assign coordinates of the point for all three axes
       (self.x, self.y, self.z) = (x,y,z)
       # Shortcut to full position coordinates
       self.position = (x,y,z)
    

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
    return coeff

def calcLength(x,y,z=0):
    #For better accuracy, will need to compute the droop (catenary)
    # Basic calculation of strand length (assume a straight line) 
    strandLength = (x**2 + y**2 + z**2)**0.5
    return strandLength

def feetToYards(inFeet):
    return inFeet/3.0

def yardsToFeet(inYards):
    return inYards * 3.0

#widthOfStrand is how wide the tulle piece (in feet)
def findTotal(widthOfStrand,z=0,room=gym,printTotal=False):
    '''
    Find total in yards.
    Input:
        widthOfStrand (number of feet, width of material)
        z=0 (how many feet it will "drape" down linearly)
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

    #find along width
    alongWidth = 0
    while(alongWidth <= room.width):
        newX = room.hangFrom.x - alongWidth
        newY = room.hangFrom.y - room.length
        # Length of strand needed (in yards)
        strandLength = calcLength(newX,newY,z)
        # Add Break point length
        strandLengths.append(strandLength)
        # Total length
        total += strandLength 
        alongWidth += widthOfStrand

    #find along length, around gym
    alongLength = 0 
    while(alongLength <= room.length):
        newX = room.hangFrom.z - room.width
        newY = room.hangFrom.y - alongLength
        # Length of strand needed (in yards)
        strandLength = calcLength(newX,newY,z)
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
