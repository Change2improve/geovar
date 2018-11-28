'''
*
* Configure Onshpae parts using Python
*
'''

from onshapepy.play import *
from time import sleep
from time import time

# Part Studio Part URL
part_URL = "https://cad.onshape.com/documents/170d98597622d5e73691785d/w/13b21fc0217b5eb5b7a8c3fb/e/c492b1b83c1e52a0062ae590"
myPart = Part( part_URL )

# Access part parameters
# DEFAULT VALUES: { 'square_length': <Quantity(29.5, 'millimeter')>,'
#                   'circle_radius': <Quantity(27.5, 'millimeter')>,
#                   'extrusion_depth': <Quantity(2.5, 'millimeter')>,
#                   'fillet': True, 'fillet_type': 'circular'}
parameters = myPart.params
print( parameters )

# Change part parameters here
# NOTE:-
#   You MUST multiply the value with whatever unit you want it to be (i.e 3*u.in == 3in)
for i in range( 0, 100 ):
    scalar = (i+1)/100.
    print( "{}. Changing parameters...".format(i) )
    start = time()
    myPart.params = { 'circle_radius': (27.5*scalar)*u.mm, 'extrusion_depth': (2.5*scalar)*u.mm }
    print( time() - start )


### Access measurements defined within the OnShape "Measure" FeatureScript.
##measurements = myPart.measurements
##print( measurements )
