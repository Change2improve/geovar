'''
*
* Configure Onshpae parts using Python
*
'''

from    onshapepy.play      import  *
from    time                import  sleep, time
from    platform            import  system
from    datetime            import  datetime
import  os

DEV_MODE = True
## ###
## Program Setup
## ###

if( system()=='Linux' ):
    # Define useful paths
    src = os.getcwd()
    dst = src + "/output/{}/".format( datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )

    try:
        os.makedirs( dst )
    except OSError:
        print( "FAILED to create directory. Check permissions" )
        quit()
    else:
        print( "Created {}".format(dst) )
        os.chdir( dst )
        
if( system()=='Windows' ):
    # Define useful paths
    src = os.getcwd()
    dst = src + "\\output\\{}\\".format( datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )

    try:
        os.makedirs( dst )
    except WindowsError:
        print( "FAILED to create directory. Check permissions" )
        quit()
    else:
        print( "Created {}".format(dst) )
        os.chdir( dst )

## ###
## Connect to sketch
## ###

if( DEV_MODE ):
    did = "04b732c124cfa152cf7c07f3"                    # ...
    wid = "c4358308cbf0c97a44d8a71a"                    # Get features for document of interest
    eid = "a23208c314d70c14da7071e6"                    # ...
else:
    did = raw_input('Enter document  ID: ')             # ...
    wid = raw_input('Enter workspace ID: ')             # ...
    eid = raw_input('Enter element   ID: ')             # ...

if( len(did) != 24 or len(wid) != 24 or len(eid) != 24 ):
    raise ValueError( "Document, workspace, and element IDs must be 24 characters in length" )

# Connect to Onshape and part
part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format( did, wid, eid )
myPart      = Part( part_URL )                          # Connect to part for modification
c           = Client()                                  # Create instance of the onshape client for exporting

# Access part parameters
# SAMPLE OUTPUT:  { 'feature_1': <Quantity(29.5, 'millimeter')>,'
#                   'feature_2': <Quantity(27.5, 'millimeter')>,
#                   'fillet': True, 'fillet_type': 'circular'}
parameters = myPart.params
print( parameters )


## ###
## Perform Permutations
## ###

# Change part parameters here
# NOTE:-
#   You MUST multiply the value with whatever unit
#   you want it to be (i.e 3*u.in == 3in)

LB = 0; UB = 10                                         # Define lower and upper bounds
for i in range( LB, UB ):
    print( "\nr_inner \t r_outer \t height \t t_regen" )
    print( "========================================================\n" )
    scalar_1 = (i+1)/float(UB)
    
    for j in range( LB, UB ):
        scalar_2 = (j+1)/float(UB)
        
        for k in range( LB, UB ):
            scalar_3 = (k+1)/float(UB)

            start   = time()
            myPart.params = { 'r_inner' : ( 50*scalar_1)*u.mm,
                              'r_outer' : (100*scalar_2)*u.mm,
                              'height'  : (100*scalar_3)*u.mm }
            end     =  time() - start
            
            print( "{:4.3f} \t\t {:4.3f} \t {:4.3f} \t {:4.3f}".format(50*scalar_1,
                                                                       100*scalar_2,
                                                                       100*scalar_3, end) )
            print( "--------------------------------------------------------" )
            
            # get the STL export
            stl = c.part_studio_stl(did, wid, eid)

            file_name = "ri{}_ro{}_h{}.stl".format( i, j, k )
            with open( file_name, 'w' ) as f:
                f.write( stl.text )

