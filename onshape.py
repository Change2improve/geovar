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
* VERSION: 1.2.5
*   - ADDED   : Ability to check whether part failed to mutate or not!
*   - FIXED   : Now fully compatible with Windows machines
*   - FIXED   : Fixed check_default() method's logic. Now we only export
*               parts that do NOT revert back to default value after mutation.
*   - ADDED   : More beautiful formatting FTW!
*
*
* KNOWN ISSUES:
*   - Non at the moment
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Dec. 10th, 2018 Year of Our Lord
* LAST CONTRIBUTION DATE    :   Dec. 18th, 2018 Year of Our Lord
*
'''

from    onshapepy.play              import  *                       # Onshape API
from    time                        import  sleep, time             # Timers/delays
from    platform                    import  system                  # Running platform info
from    datetime                    import  datetime                # Get date and time

try:
    from    pexpect                 import  spawn                   # Call external programs (UNIX)
except:
    from    pexpect.popen_spawn     import  PopenSpawn as spawn     # Call external programs (Windows)
    
from    argparse                    import  ArgumentParser          # Add input arguments to script
from    itertools                   import  product                 # Apply product rule on combinations
import  numpy                       as      np                      # Fast array creation
import  os, re                                                      # Dir/path manipulation, extract numerics from strings

# ************************************************************************
# =====================> CONSTRUCT ARGUMENT PARSER <=====================*
# ************************************************************************

ap = ArgumentParser()

# Developer mode, makes life easy for me
ap.add_argument( "--dev-mode"           ,
                 dest   = "dev_mode"    ,
                 action = 'store_true'  , default=False ,
                 help   = "Enter developer mode"        )

# Directory that points to COMPILED/EXECCUTABLE tetgen
ap.add_argument( "--tetgen-dir"         , type = str    ,
                 dest   = "tetgen_dir"  , default="foo" ,
                 help   = "Point to TetGen directory"   )

# Print out stuff to help debug
ap.add_argument( "-v", "--verbose"      ,
                 dest   = "verbose"     ,
                 action = 'store_true'  , default=False ,
                 help   = "WARNING: Prints EVERYTHING!!")

# Lower bound for variations array
ap.add_argument( "-LB", "--lower-bound" , type = int    ,
                 dest   = "lower_bound" , default = 50  ,
                 help   = "Minimum value desired"       )

# Upper bound for variations array
ap.add_argument( "-UB", "--upper-bound" , type = int    ,
                 dest   = "upper_bound" , default = 51  ,
                 help   = "Maximum value desired"       )

# Step size for variations array
ap.add_argument( "-H", "--step-size"    , type = float  ,
                 dest   = "upper_bound" , default = 0.1 ,
                 help   = "Variations step size"        )

args = ap.parse_args()

args.dev_mode    = True
if( args.dev_mode ):
    args.tetgen_dir     = '/home/moe/Desktop/geovar/tetgen1.5.1/'
##    args.verbose        = True
    args.lower_bound    = 9
    args.upper_bound    = 10
    args.step_size      = 1
# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class GeoVar( object ):

    def __init__( self ):
        if( args.tetgen_dir == "foo" ):                             # Make sure a directory for TetGen was given
            raise NameError( "No TetGen directory sepcified" )      # ...

        self.allow_export    = False                                # Flag to allow STL exports
        self.valid_mutations = 0                                    # Counter for successful mutations
        
        self.setup_directories()                                    # Setup & define directories
        self.connect_to_sketch()                                    # Instantiate Onshape client and connect

        self.get_values( initRun=True )                             # Get configurable part features and CURRENT default values

# --------------------------

    def setup_directories( self ):
        '''
        Create output folder and point to
        location of compiled TetGen program
        '''

        # ------ UNIX systems ------
        if( system()=='Linux' ):
            src      = os.getcwd()
            self.dst = "{}/output/{}/".format( src, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
            self.tet = args.tetgen_dir

            try:
                os.makedirs( self.dst )
            except OSError:
                print( "FAILED to create directory. Check permissions" )
                quit()
            else:
                print( "Created {}".format(self.dst) )

        # ----- Windows system -----
        elif( system()=='Windows' ):
            # Define useful paths
            src      = os.getcwd()
            self.dst = "{}\\output\\{}\\".format( src, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
            self.tet = args.tetgen_dir

            try:
                os.makedirs( self.dst )
            except WindowsError:
                print( "FAILED to create directory. Check permissions" )
                quit()
            else:
                print( "Created {}".format(self.dst) )

# --------------------------

    def connect_to_sketch( self ):
        '''
        Connect to Onshape and access desired sketch
        '''

        if( args.dev_mode ):
            self.did = "04b732c124cfa152cf7c07f3"                   # ...
            self.wid = "c4358308cbf0c97a44d8a71a"                   # Get features for document of interest
            self.eid = "a23208c314d70c14da7071e6"                   # ...
        else:
            self.did = raw_input('Enter document  ID: ')            # ...
            self.wid = raw_input('Enter workspace ID: ')            # ...
            self.eid = raw_input('Enter element   ID: ')            # ...

        if( len(self.did) != 24 or                                  # Ensure inputted IDs are valid
            len(self.wid) != 24 or                                  # ...
            len(self.eid) != 24 ):                                  # ...
            raise ValueError( "Document, workspace, and element IDs must each be 24 characters in length" )
        else:
            part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format( self.did, self.wid, self.eid )
            self.myPart = Part( part_URL )                          # Connect to part for modification
            self.c      = Client()                                  # Create instance of the onshape client for exporting

# --------------------------

    def get_values( self, initRun=False ):
        '''
        Extract configured variable names from part
        and get the current values.
        When initRun is True, it gets the default values
        and stores them for later usage.

        FROM: https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string

        INPUT:-
            - initRun: Set to True ONLY the first time this command is run.
                       This allows us to store the default values for the part.

        NOTE:-
            myPart.param = {
                            'feature_1': <Quantity(29.5, 'millimeter')>,
                            'feature_2': <Quantity(27.5, 'millimeter')>,
                            'fillet': True, 'fillet_type': 'circular'
                           }

        KNOWN ISSUES:
            - Still can't get boolean values such as fillets and whatnot
        '''

        numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
        rx = re.compile(numeric_const_pattern, re.VERBOSE)

        if( initRun ):                                              # If this is the initial run, get defaults
            self.keys       = list( self.myPart.params )            #   Cast dict as list to extract keys
            self.default    = [None] * len( self.keys )             #   Create a list of length for values

            print( "Found {} configurable parts with defaults:-".format(len(self.keys)) )
            for i in range( 0, len(self.keys) ):                    #   Loop over all dict entries
                param = str( self.myPart.params[ self.keys[i] ] )   #       Get dict value as string
                self.default[i] = float( rx.findall(param)[0] )     #       Extract value from string
                print( "  {:3}. {:12}: {: >10.3f}".format(i+1, self.keys[i], self.default[i]) )
            print( '' )
            return( 0 )

        else:
            current    = [None] * len( self.keys )                  #   Create a list of length for values
            
            print( "{:8}:".format("CURRENT"), end='\t' )
            for i in range( 0, len(self.keys) ):                    #   Loop over all dict entries
                param = str( self.myPart.params[ self.keys[i] ] )   #       Get dict value as string
                current[i] = float( rx.findall(param)[0] )          #       Extract value from string
                print( "{:4.3f}".format(current[i]), end='\t\t' )
            print("//"); print( "-" * self.len_cte )
            return( current )
        
# --------------------------

    def mutate_part( self, arr ):
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
        
        ranges      = [range(arr.shape[1])] * arr.shape[0]          # Range we would like to go through
        b           = np.array( list(product(*ranges)) )            # Create an array of indices of the products

        param_prvs  = np.copy( arr.T[0] )                           # Previous unchanged value of the parameters
        param_crnt  = np.zeros_like( param_prvs )

        fmt_str = str()
        for name in self.keys:                                      # Build row with key names
            fmt_str = "{}\t\t{}".format( fmt_str, name )            # for visual presentation
        fmt_str = "{}\t\tt_regen".format( fmt_str )                 # ...

        self.len_cte = len(fmt_str) * round(len(self.keys)/2)       # Format length constant
        
        # ------ Mutate  Part ------
        self.i = 0
        for i in range( 0, b.shape[0] ):                            # Loop over ALL possible combinations
            print( fmt_str )                                        #   [INFO] Print FORMATTED key names
            print( "=" * self.len_cte )                             #   [INFO] Print adaptive width dashes
            print( "{:8}:".format("SENT"), end='\t' )               #   [INFO] Print values

            temp    = str()                                         #   Temporary string to hold filename
            start   = time()                                        #   Timer for regeneration time
            
            for j in range( 0, arr.shape[0] ):                      #   Loop over ALL features
                param_crnt[j] = arr.T[b[i][j]][j]                   #       Get current value to be passed
                
                if( param_crnt[j] != param_prvs[j] ):               #       If current and previous parameters are different
                    self.myPart.params = { self.keys[j]:            #           Pass new value (aka mutate part)
                                           param_crnt[j]*u.mm }     #           ...

                    param_prvs[j] = param_crnt[j]                   #           Update previous parameter
                    self.i += 1
                    
                else: pass                                          #       Otherwise don't do anything
                
                print( "{:4.3f}".format(param_crnt[j]), end='\t\t' )#       [INFO] Print value being sent to Onshape

                temp = "{}{}{}__".format( temp, self.keys[j],       #       Build file name
                                          param_crnt[j] )           #       ...
                
            print( "{:4.3f}".format(time() - start) )               #       [INFO] Print regeneration time
            print( "-" * self.len_cte )                             #       [INFO] Print break lines

            # get the STL export
            file = "{}{}.stl".format( self.dst, temp.rstrip('_') )  #       Build file name
            
            self.check_default( param_crnt )                        #       Check if part regenerated properly

            if( self.allow_export ):                                #       Export the STL file
                self.export_stl( file )                             #       ...

        # --- Revert to defaults ---
        print( "*" * self.len_cte )                                 # [INFO] Print break lines
        print( "RESULTS:-" )                                        # ...
        print( "  {:5} mutations performed".format(b.shape[0]) )    # ...
        print( "    {:5} successful mutations".format(self.valid_mutations))
        print( "    {:5} failed     mutations".format(b.shape[0]-self.valid_mutations))
        print( "  {:5} calls to Onshape".format(self.i) )
        print( "*" * self.len_cte )                                 # [INFO] Print break lines

        self.reset_myPart()                                         # Go back to defaults

# --------------------------

    def check_default( self, passed_value ):
        '''
        Check if the value reverted to the default value after
        being changed.
        This indicates that the feature failed to mutate.

        INPUT:-
            - passed_value : Value that was sent to Onshape.
        '''

        print( "{:8}:".format("DEFAULT"), end='\t' )                # [INFO] Print DEFAULT values
        for num in self.default:                                    # ...
            print( "{:4.3f}".format(num), end='\t\t' )              # ...
        print( "//" ); print( "-" * self.len_cte )                  # ...

        current_value = self.get_values( )                          # Read CURRENT value from Onshape
        for i in range( 0, len(current_value) ):
                
            if( passed_value[i] != self.default[i] ):               # If passed value is different than the default
                if( current_value[i] == self.default[i] ):          #   Current value is equal to the default
                    self.allow_export = False                       #       File failed to regenerate, don't export!
                    print( "{:_^{width}}".format("FAILED MUTATION", width=self.len_cte), end='\n\n' )
                    return 0

        self.allow_export = True                                    #       Allow exporting of STL
        self.valid_mutations += 1                                   #       Increment counter
        print( "{:_^{width}}".format("VALID  MUTATION", width=self.len_cte), end='\n\n' )
                
# --------------------------

    def export_stl( self, file_name ):
        '''
        Export file as STL.

        INPUT:-
            - file_name: The name you'd like the STL file
                         to be given.
        '''

        stl = self.c.part_studio_stl( self.did, self.wid, self.eid )# Get the STL

        with open( file_name, 'w' ) as f:                           # Write STL to file
            f.write( stl.text )                                     # ...

        self.mesh_file( file_name )                                 # Create MESH

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
            cmd = "{}tetgen.exe -pq1.2 -g -F -C -V -N -E -I -a0.1 {}".format( self.tet, file_name )
            
        child = spawn( cmd, timeout=None )                          # Spawn child
        
        for line in child:                                          # Read STDOUT ...
            out = line.decode('utf-8').strip('\r\n')                # ... of spawned child ...
            if( args.verbose ): print( out )                        # ... process and print.
        
        if( system()=='Linux' ): child.close()                      # Kill child process
        
# --------------------------

    def reset_myPart( self ):
        '''
        Resets part to default values found at the
        beginning of the script.
        '''

        print( "Reverting part to defaults", end='' )               # [INFO] ...
        for i in range( 0, len(self.keys) ):                        # Loop over ALL features
            self.myPart.params = { self.keys[i]:                    #   Set back to default
                                   self.default[i]*u.mm }           #   ...
        print( "...DONE!" )

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

prog = GeoVar()                                                     # Startup and prepare program

''' CHANGE THESE GUYS AS YOU SEE FIT '''
LB  = args.lower_bound                                              # Lower bound
UB  = args.upper_bound                                              # Upper bound
h   = args.step_size                                                # Step size

'''
NOTE THAT ALL THE ARRAYS CREATED ARE REPLICAS OF ONE ANOTHER.
THIS WAS DONE FOR THE SAKE OF SIMPLICITY. EACH ARRAY CAN BE
CONSTRUCTED ON ITS OWN MANUALLY IF THE USER WANTS TO DO SO.
'''
arr = np.zeros( [len(prog.keys), int((UB-LB)/h)+1] )                # Dynamically create array
for i in range( 0, len(prog.keys) ):                                # depending on number of
    arr[i] = np.array( np.linspace(LB, UB, int((UB-LB)/h)+1) )      # varying features

try:
    prog.mutate_part( arr )                                         # Do da tang!
except:
    prog.reset_myPart()                                             # In case something goes wrong, reset!

