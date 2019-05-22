'''
*
* Automatic configuration and meshing of Onshape parts using Python
*
* VERSION: 1.1.2
*   - ADDED   : Script is now COMPLETELY independent of hardcoded
*               values. Script can now determine number of
*               features and dynamically adjust as needed.
*   - ADDED   : Optimized script for speed. If current feature parameter
*               is the same as the previous value (no change to it), then
*               it is not sent to Onshape to reduce time needed.
*   - MODIFIED: Adaptive width line printing.
*
*
* VERSION: 1.2.8
*   - ADDED   : Ability to check whether part failed to mutate or not!
*   - FIXED   : Now fully compatible with Windows machines
*   - FIXED   : Fixed check_default() method's logic. Now we only export
*               parts that do NOT revert back to default value after mutation.
*   - ADDED   : More beautiful formatting FTW!
*   - ADDED   : Give user ability to define array bounds!
*   - ADDED   : Enforce correct math, you can call me the math police.
*               (i.e. make sure lower bound can't be greater than upper bound)
*   - MODIFIED: Simplify code to reduce clutter.
*   - FIXED   : Doesn't break when user inputs invalid values (i.e str instead of float)
*
*
* VERSION: 1.2.9
*   - ADDED   : Automated localization of the tetgen directory/path
*
*
* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh, Fluvio L. Lobo Fenoglietto
* DATE                      :   Dec. 10th, 2018 Year of Our Lord
* LAST CONTRIBUTION DATE    :   Jan. 09th, 2019 Year of Our Lord
*
'''

from    onshapepy.play              import  *                           # Onshape API
from    time                        import  sleep, time                 # Timers/delays
from    platform                    import  system                      # Running platform info
from    datetime                    import  datetime                    # Get date and time

try:
    from    pexpect                 import  spawn                       # Call external programs (UNIX)
except:
    from    pexpect.popen_spawn     import  PopenSpawn as spawn         # Call external programs (Windows)
    
from    argparse                    import  ArgumentParser              # Add input arguments to script
from    itertools                   import  product                     # Apply product rule on combinations
import  numpy                       as      np                          # Fast array creation
import  os, re                                                          # Dir/path manipulation, extract numerics from strings


import  _setup
import  _onshape
import  _morph

# ************************************************************************
# =====================> CONSTRUCT ARGUMENT PARSER <=====================*
# ************************************************************************

ap = ArgumentParser()

# Operation Modalities ------------------------------------------------- #

# Demo. Mode
#   Demonstrates use of the geovar() program 
string = "Demo. or Example Mode --uses 'permute' document"
ap.add_argument( "-dem" , "--demo_mode" ,
                 dest   = "demo_mode"    ,
                 action = 'store_true'  , default=False ,
                 help   = "{}".format(string)           )

# Print out stuff to help debug
string = "WARNING: Prints EVERYTHING!!"
ap.add_argument( "-v"   , "--verbose"   ,
                 dest   = "verbose"     ,
                 action = 'store_true'  , default=False ,
                 help   = "{}".format(string)           )

### Quiet mode; create arrays of identical variation
##string = "Quiet mode; arrays have the same value"
##ap.add_argument( "-q"   , "--quiet"     ,
##                 dest   = "quiet"       ,
##                 action = 'store_true'  , default=False ,
##                 help   = "{}".format(string)           )

# Operation Inputs ---------------------------------------------------- #
# Input File
string = "Input file containing onshape document IDs, variable information"
ap.add_argument( "-i"   , "--input_file"     , type = str           ,
                 dest   = "input_file"       , default = "doc.xml"  ,
                 help   = "{}".format(string)                       )

### Lower bound for variations array
##string = "Minimum value desired"
##ap.add_argument( "-LB", "--lower-bound" , type = int    ,
##                 dest   = "lower_bound" , default =  0  ,
##                 help   = "{}".format(string)           )
##
### Upper bound for variations array
##string = "Maximum value desired"
##ap.add_argument( "-UB", "--upper-bound" , type = int    ,
##                 dest   = "upper_bound" , default =  0  ,
##                 help   = "{}".format(string)           )
##
### Step size for variations array
##string = "Variations step size"
##ap.add_argument( "-H", "--step-size"    , type = float  ,
##                 dest   = "step_size" , default = 0.1 ,
##                 help   = "{}".format(string)           )

args = ap.parse_args()

##if( args.dev_mode ):
##    args.tetgen_dir     = '/home/moe/Desktop/geovar/tetgen1.5.1/'
##    args.quiet          = True
##    args.verbose        = True
##    args.lower_bound    = 9
##    args.upper_bound    = 10
##    args.step_size      = 1

# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class geovar( object ):

    def __init__( self ):
##        if( args.tetgen_dir == "foo" ):                                 # Make sure a directory for TetGen was given
##            raise NameError( "No TetGen directory sepcified" )          # ...

        self.allow_export    = False                                    # Flag to allow STL exports
        self.valid_mutations = 0                                        # Counter for successful mutations
        
        self.setup()                                                    # Setup & define directories

        self.connect_to_sketch()                                        # Instantiate Onshape client and connect

        self.get_values( initRun = True )                               # Get configurable part features and CURRENT default values
        # will use the get values function to check if the user input matches...
        
# --------------------------

    def setup( self ):
        '''
        SETUP
            - Locating and defining directories
            - Gathering document information (did, wid, eid)
            - Gathering document variables
            - Generating the morphing array
        '''
        _setup.setup_directories( self )                                # retrieve directory information
        _setup.read_doc( self, args.input_file )                        # retrieve document information
        _setup.read_vars( self, args.input_file )                       # retrieve variable information
        _setup.generate_morphing_array( self )


# --------------------------

    def connect_to_sketch( self ):
        '''
        Connect to Onshape and access desired sketch
        '''
        _onshape.connect_to_sketch( self, args )                        # connect to the onshape document

# --------------------------

    def get_values( self, initRun = False ):
        '''
        Get configuration parameters from Onshape document
        '''
        _onshape.get_configurations( self )
        _onshape.get_values( self )
        

# --------------------------

    def morph_geometry( self ):
        '''
        Apply product rule on part to get as many
        geometric variations as needed

        INPUT:-
            - arr:  An array of arrays containing the values
                    we would our features to have
                    
        NOTES:-
            You MUST multiply the value with whatever unit
            you want it to be (i.e 3*u.in == 3in)
        '''

        _morph.morph_geometry( self ) 
        
# --------------------------

    def check_default( self, passed_value ):
        '''
        Check if the value reverted to the default value after
        being changed.
        This indicates that the feature failed to mutate.

        INPUT:-
            - passed_value : Value that was sent to Onshape.
        '''

        print( "{:8}:".format("DEFAULT"), end='\t' )                    # [INFO] Print DEFAULT values
        for num in self.default:                                        # ...
            print( "{:4.3f}".format(num), end='\t\t' )                  # ...
        print( "//" ); print( "-" * self.len_cte )                      # ...

        current_value = self.get_values( )                              # Read CURRENT value from Onshape
        for i in range( 0, len(current_value) ):
                
            if( passed_value[i] != self.default[i] ):                   # If passed value is different than the default
                if( current_value[i] == self.default[i] ):              #   Current value is equal to the default
                    self.allow_export = False                           #       File failed to regenerate, don't export!
                    print( "{:_^{width}}".format("FAILED MUTATION", width=self.len_cte), end='\n\n' )
                    return 0

        self.allow_export = True                                        #       Allow exporting of STL
        self.valid_mutations += 1                                       #       Increment counter
        print( "{:_^{width}}".format("VALID  MUTATION", width=self.len_cte), end='\n\n' )
                
# --------------------------

    def export_stl( self, file_name ):
        '''
        Export file as STL.

        INPUT:-
            - file_name: The name you'd like the STL file
                         to be given.
        '''

        stl = self.c.part_studio_stl( self.did, self.wid, self.eid )    # Get the STL

        with open( file_name, 'w' ) as f:                               # Write STL to file
            f.write( stl.text )                                         # ...

        self.mesh_file( file_name )                                     # Create MESH

# --------------------------

    def mesh_file( self, file_name ):
        '''
        Create a MESH out of the STL file.

        INPUT:-
            - file_name: The name you'd like the MESH file
                         to be given.
        '''

        if( system()=='Linux' ):
            cmd = "{}tetgen -pq1.2 -g -F -C -V -N -E -I -a0.1 {}".format( self.tet, file_name )
        elif( system()=='Windows' ):
            print( self.tet )
            print( file_name )
            cmd = "{}tetgen.exe -pq1.2 -g -F -C -V -N -E -I -a0.1 {}".format( self.tet, file_name )
            print( cmd )
            
        child = spawn( cmd, timeout=None )                              # Spawn child
        
        for line in child:                                              # Read STDOUT ...
            out = line.decode('utf-8').strip('\r\n')                    # ... of spawned child ...
            if( args.verbose ): print( out )                            # ... process and print.
        
        if( system()=='Linux' ): child.close()                          # Kill child process
        
# --------------------------

    def reset_myPart( self ):
        '''
        Resets part to default values found at the
        beginning of the script.
        '''

        print( "Reverting part to defaults", end='' )                   # [INFO] ...
        for i in range( 0, len(self.keys) ):                            # Loop over ALL features
            self.myPart.params = { self.keys[i]:                        #   Set back to default
                                   self.default[i]*u.mm }               #   ...
        print( "...DONE!" )

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

prog = geovar()                                                         # Startup and prepare program

'''
try:
    print( arr )
    prog.mutate_part( arr )                                             # Do da tang!
except:
    prog.reset_myPart()                                                 # In case something goes wrong, reset!
'''
