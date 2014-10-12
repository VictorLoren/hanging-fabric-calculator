#calculate the length of a hanging strand

# RectRoom class
class RectRoom(object):
    def __init__(self,length,width):
        self.length = length
        self.width = width

def calcLength(x,y,z=0):
    #For better accuracy, will need to compute the droop (catenary)
    # Basic calculation of strand length (assume a straight line) 
    strandLength = (x**2 + y**2 + z**2)**0.5
    return strandLength

#lengths are in feet
L = 92; W=68; H=22; MidXY=(W/2,L/2)

def feetToYards(inFeet):
    return inFeet/3.0

def yardsToFeet(inYards):
    return inYards * 3.0

#widthOfStrand is how wide the tulle piece (in feet)
def findTotal(widthOfStrand,z=0,printTotal=False):
    '''
    Find total in yards.
    Input:
        widthOfStrand (number of feet, width of tulle)
        z=0 (how many feet it will "drape" down linearly)
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
    while(alongWidth <= W):
        newX,newY = (MidXY[0] - alongWidth,MidXY[1]-L)
        # Length of strand needed (in yards)
        strandLength = calcLength(newX,newY,z)
        # Add Break point length
        strandLengths.append(strandLength)
        # Total length
        total += strandLength 
        alongWidth += widthOfStrand

    #find along length, around gym
    alongLength = 0 
    while(alongLength <= L):
        newX,newY = (MidXY[0] - W,MidXY[1]- alongLength)
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
    #all the strand lengths
    strandLengths *=2 
    if printTotal:
        print '\nTotal Length For Room: %.2f yards' %(2*total)
    # Return total length in yards and a list of strand lengths needed
    return (2*total , strandLengths.sort())

def totalCost(costPerYard,widthOfStrandInFeet,drapingInFeet,printTotal=False):
    total = findTotal(widthOfStrandInFeet,drapingInFeet,printTotal)
    cost = total * costPerYard
    print "Total length %.2f yards for $%.2f (@ $%.2f per yard)" %(total,cost,costPerYard)
    return cost

print "Imported 'tulle'"
