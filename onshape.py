'''
*
* Configure Onshpae parts using Python
*
'''

from onshapepy.play     import  *
from time               import  sleep, time

# Part Studio Part URL
part_URL = "https://cad.onshape.com/documents/04b732c124cfa152cf7c07f3/w/c4358308cbf0c97a44d8a71a/e/a23208c314d70c14da7071e6"
myPart = Part( part_URL )

# stacks to choose from
stacks = {
    'cad': 'https://cad.onshape.com'
}

# create instance of the onshape client; change key to test on another stack
c = Client()
# get features for doc
did = "04b732c124cfa152cf7c07f3"#raw_input('Enter document ID: ')
wid = "c4358308cbf0c97a44d8a71a"#raw_input('Enter workspace ID: ')
eid = "a23208c314d70c14da7071e6"#raw_input('Enter element ID: ')


# Access part parameters
# SAMPLE OUTPUT:  { 'feature_1': <Quantity(29.5, 'millimeter')>,'
#                   'feature_2': <Quantity(27.5, 'millimeter')>,
#                   'fillet': True, 'fillet_type': 'circular'}
parameters = myPart.params
print( parameters )

# Change part parameters here
# NOTE:-
#   You MUST multiply the value with whatever unit
#   you want it to be (i.e 3*u.in == 3in)

LB = 0; UB = 5                                              # Define lower and upper bounds
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
            
##            # get the STL export
##            stl = c.part_studio_stl(did, wid, eid)
##
##            file_name = "stl_part_{}.stl".format( i )
##            with open( file_name, 'w' ) as f:
##                f.write( stl.text )

