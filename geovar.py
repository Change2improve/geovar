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

# onshape modules and libraries
from    onshapepy.play              import  *                           # Onshape API


# adapted onshape modules and libraries
import  _setup
import  _onshape
import  _morph
import  _mesh

# additional python modules and libraries
from    time                        import  sleep, time                 # Timers/delays
from    platform                    import  system                      # Running platform info
from    datetime                    import  datetime                    # Get date and time


    
from    argparse                    import  ArgumentParser              # Add input arguments to script
from    itertools                   import  product                     # Apply product rule on combinations
import  numpy                       as      np                          # Fast array creation
import  os, re                                                          # Dir/path manipulation, extract numerics from strings


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


# Operation Inputs ---------------------------------------------------- #
# Input File
string = "Input file containing onshape document IDs, variable information"
ap.add_argument( "-i"   , "--input_file"     , type = str           ,
                 dest   = "input_file"       , default = "doc.xml"  ,
                 help   = "{}".format(string)                       )

args = ap.parse_args()


# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class geovar( object ):

    def __init__( self ):

        '''
        TO DO:
            - Define "r" as a dictionary to store all possible responses
            - Same for "configs" ...perhaps this should be part of the "_setup" module
        '''

        # VARIABLES
        self.prog_start_time    = time()
        self.r                  = {}                                    # Initialize the 'r' dict for record of decoded responses
        self.configs            = {}                                    # Initialized the 'configs' dict
        self.variant_iter       = 0
        
        self.allow_export       = False                                    # Flag to allow STL exports
        self.valid_mutations    = 0                                        # Counter for successful mutations
        
        self.setup()                                                    # Setup & define directories
        
# --------------------------

    def setup( self ):
        '''
        SETUP
            - Locating and defining directories
            - Gathering document information (did, wid, eid)
            - Gathering document variables
            - Generating the morphing array
            - Connect to onshape document
        '''
        
        self.prog_time          = time() - self.prog_start_time
        _setup.setup_directories( self )                                # retrieve directory information
        _setup.read_doc( self, args.input_file )                        # retrieve document information
        _setup.read_vars( self, args.input_file )                       # retrieve variable information
        _setup.generate_variant_array( self )
        _onshape.connect_to_sketch( self, args )                        # connect to the onshape document
        _onshape.get_list_of_parts( self )

# --------------------------
    

    def generate_variant( self ):
        '''
        GENERATE GEOMETRY VARIANT:
            - Connects to onshape document
            - Retrieves default configurations
            - Updates configurations based on morphing array
            - Exports geometric variant (.STL)
        '''

        self.prog_time          = time() - self.prog_start_time
        _onshape.get_configurations( self )
        _onshape.get_values( self )
        _morph.simple_morph( self )
        _onshape.export_stl( self )
        
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

    def mesh_variant( self ):
        '''
        MESH FILE
        '''

        _mesh.tetgen( self )
        
        
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

for i in range( 0, 3 ):
    prog.generate_variant()
    prog.mesh_variant()

'''
try:
    print( arr )
    prog.mutate_part( arr )                                             # Do da tang!
except:
    prog.reset_myPart()                                                 # In case something goes wrong, reset!
'''
