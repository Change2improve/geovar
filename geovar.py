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
import  _febio

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

string = """(1) Generate Geometric Variations of Input Geometry
            (2) Mesh Geometric Variations using TetGen
            (3) Simulate Geometric Variations using FEBio
         """
ap.add_argument( "-m"   , "--mode"     , type = int     ,
                 dest   = "mode"       , default = 1    ,
                 help   = "{}".format(string)           )

### Print out stuff to help debug
##string = "WARNING: Prints EVERYTHING!!"
##ap.add_argument( "-v"   , "--verbose"   ,
##                 dest   = "verbose"     ,
##                 action = 'store_true'  , default=False ,
##                 help   = "{}".format(string)           )


# Input File
string = "Input file name (no extensions)"
ap.add_argument( "-i"   , "--input_file"     , type = str           ,
                 dest   = "input_file"       , default = "dogbone.xml"  ,
                 help   = "{}".format(string)                       )

args = ap.parse_args()


# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class geovar( object ):

    def __init__( self ):

        # VARIABLES
        self.prog_start_time    = time()

        self.mode               = args.mode
        
        self.r                  = {}                                    # Initialize the 'r' dict for record of decoded responses
        self.configs            = {}                                    # Initialized the 'configs' dict
        self.variant_iter       = 0

        self.g                  = {}                                    # Initialize the 'g' dict for geometry data
        
        self.setup()                                                    # Setup & define directories
        
# --------------------------

    def setup( self ):
        '''
        SETUP
            - Locating and defining directories
            - Gathering document information (did, wid, eid)
            - Gathering document variables
            - Generating the morphing array
            - Gather template FEBio (or simulation file)
            - Connect to onshape document
        '''
        
        self.prog_time          = time() - self.prog_start_time

        
        _setup.setup_directories(       self )                                # retrieve directory information
        _setup.generate_filenames(      self, args.input_file, args.mode )
        _setup.read_doc(                self, args.input_file )                        # retrieve document information
        _setup.read_vars(               self, args.input_file )                       # retrieve variable information
        _setup.generate_variant_array(  self )

        #_febio.read_febio_file(         self, args.input_file )
        
        _onshape.connect_to_sketch(     self, args )                        # connect to the onshape document
        _onshape.get_list_of_parts(     self )

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

    def mesh_variant( self ):
        '''
        MESH VARIANT
            - Generates a mesh of the geometric variant
        '''

        _mesh.tetgen( self )
        

# --------------------------

    def sim_variant( self ):
        '''
        SIMULATE VARIANT
            - Triggers the simulation of the geometric variant
        '''

      

# ***************************************************************************
# =========================> MAKE IT ALL HAPPEN <============================
# ***************************************************************************

prog = geovar()                                                             # Startup and prepare program

#print( prog.mode )

print( "\n" )
print( "PROGRAM STARTING " )
#print( "> User selected MODE = {}".format( prog.mode ) ) 

Nprods = 3

if prog.mode == 1:      # MODE 1: Geometric Variations ==================== #
    for i in range( 0, Nprods ):
        prog.generate_variant()
        prog.mesh_variant()

elif prog.mode == 2:    # MODE 2: Meshing  ================================ #
    print( "> MODE {} HAS NOT BEEN INTEGRATED...".format( prog.mode ) )

elif prog.mode == 3:    # MODE 3: Simulation ============================== #
    print( "> MODE {} HAS NOT BEEN INTEGRATED...".format( prog.mode ) )

