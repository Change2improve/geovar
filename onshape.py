'''
*
* Configure Onshpae parts using Python
*
'''

from    onshapepy.play      import  *                   # Onshape API
from    time                import  sleep, time         # Timers/delays
from    platform            import  system              # Running platform info
from    datetime            import  datetime            # Get date and time
from    pexpect             import  spawn               # Call external programs
import  os, pexpect                                     # Directory and path manipulation

DEV_MODE = True
## ###
## Program Setup
## ###

if( system()=='Linux' ):
    # Define useful paths
    src = os.getcwd()
    dst = "{}/output/{}/".format( src, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
    tet = "{}/tetgen1.5.1/tetgen".format( src )

    try:
        os.makedirs( dst )
    except OSError:
        print( "FAILED to create directory. Check permissions" )
        quit()
    else:
        print( "Created {}".format(dst) )
        
if( system()=='Windows' ):
    # Define useful paths
    src = os.getcwd()
    dst = "{}\\output\\{}\\".format( src, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
##    tet = "{}\\tetgen1.5.1\\"                         # Don't know how to call cmd line software from windows

    try:
        os.makedirs( dst )
    except WindowsError:
        print( "FAILED to create directory. Check permissions" )
        quit()
    else:
        print( "Created {}".format(dst) )

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

LB = 0; UB = 2                                         # Define lower and upper bounds
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

            file_name = "{}ri{}_ro{}_h{}.stl".format( dst, i, j, k )
            with open( file_name, 'w' ) as f:
                f.write( stl.text )

            cmd = "{} -pq1.2 -g -F -C -V -N -E -a0.1 {}".format( tet, file_name )
            child = spawn(cmd, timeout=None)                            # Spawn child
            for line in child:                                          # Read STDOUT ...
                out = line.decode('unicode-escape').strip('\r\n')       # ... of spawned child ...
                print( out )                                            # ... process and print.
            child.close()                                               # Kill child process


