'''
*
* Configure Onshpae parts using Python
*
* VERSION: 1.0
*   - ADDED   : Initial release
*
* KNOWN ISSUES:
*   - Nada so far.
* 
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Dec. 10th, 2018 Year of Our Lord
* LAST CONTRIBUTION DATE    :               -----
*
'''

from    onshapepy.play              import  *                       # Onshape API
from    time                        import  sleep, time             # Timers/delays
from    platform                    import  system                  # Running platform info
from    datetime                    import  datetime                # Get date and time
from    pexpect                     import  spawn                   # Call external programs
from    argparse                    import  ArgumentParser          # Add input arguments to script
import  os, re                                                      # Dir/path manipulation, extract numerics from strings

# ************************************************************************
# =====================> CONSTRUCT ARGUMENT PARSER <=====================*
# ************************************************************************
ap = ArgumentParser()

ap.add_argument( "--dev-mode", action = 'store_true',
                 dest = "dev_mode", default= False  ,
                 help = "Enter developer mode"      )

ap.add_argument( "--tetgen-dir"     , type = str    ,
                 dest = "tetgen_dir", default="foo" ,
                 help = "Point to TetGen directory" )

args = ap.parse_args()

args.dev_mode    = True
args.tetgen_dir  = '/home/moe/Desktop/geovar/tetgen1.5.1/'
# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class GeoVar( object ):

    def __init__( self ):
        if( args.tetgen_dir == "foo"):                              # Make sure a directory for 
                raise NameError( "No TetGen directory sepcified" )  # TetGen was given
        
        self.setup_directories()                                    # Setup & define directories
        self.connect_to_sketch()                                    # Instantiate Onshape client and connect

        self.get_default()                                          # Get configurable part features and CURRENT default values
        self.mutate_part()                                          # Do the thing

# --------------------------

    def setup_directories( self ):
        '''
        Create output folder and point to
        location of compiled TetGen program
        '''

        # ------ UNIX systems ------
        if( system()=='Linux' ):
            src = os.getcwd()
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
        if( system()=='Windows' ):
            # Define useful paths
            src = os.getcwd()
            dst = "{}\\output\\{}\\".format( src, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
##            tet = "{}\\tetgen1.5.1\\"                               # Don't know how to call cmd line software from windows

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

    def get_default( self ):
        '''
        Extract configured variable names from part
        and get the current default values

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

        self.keys       = list( self.myPart.params )
        self.default    = [None] * len( self.keys )

        print( "Found {} configurable parts with defaults:-".format(len(self.keys)) )
        for i in range( 0, len(self.keys) ):
            param = str( self.myPart.params[ self.keys[i] ] )
            self.default[i] = float( rx.findall(param)[0] )
            print( "  {:3}. {:12}: {: >10.3f}".format(i+1, self.keys[i], self.default[i]) )
        print( '' )
        
# --------------------------

    def mutate_part( self ):
        '''
        Apply product rule on part to get as many
        geometric variations as needed

        NOTE:-
            You MUST multiply the value with whatever unit
            you want it to be (i.e 3*u.in == 3in)
        '''
        LB = 0; UB = 2                                              # Define lower and upper bounds
        for i in range( LB, UB ):
            for ii in range( 0, len(self.keys) ):
                print( "{}".format( self.keys[ii] ), end='\t\t' )
            print( "t_regen" )
            print( "========================================================\n" )
            scalar_1 = (i+1)/float(UB)
            
            for j in range( LB, UB ):
                scalar_2 = (j+1)/float(UB)
                
                for k in range( LB, UB ):
                    scalar_3 = (k+1)/float(UB)

                    start   = time()
                    self.myPart.params = { 'r_inner' : ( 50*scalar_1)*u.mm,
                                           'r_outer' : (100*scalar_2)*u.mm,
                                           'height'  : (100*scalar_3)*u.mm }
                    end     =  time() - start
                    
                    print( "{:4.3f} \t\t {:4.3f} \t {:4.3f} \t {:4.3f}".format(50*scalar_1,
                                                                               100*scalar_2,
                                                                               100*scalar_3, end) )
                    print( "--------------------------------------------------------" )
                    
                    # get the STL export
                    self.export_stl( i, j, k )
                    

# --------------------------

    def export_stl( self, i, j, k ):
        '''
        Apply product rule on part to get as many
        geometric variations as needed

        NOTE:-
            You MUST multiply the value with whatever unit
            you want it to be (i.e 3*u.in == 3in)
        '''

        stl = self.c.part_studio_stl( self.did, self.wid, self.eid )

        file_name = "{}ri{}_ro{}_h{}.stl".format( self.dst, i, j, k )
        with open( file_name, 'w' ) as f:
            f.write( stl.text )

        cmd = "{}tetgen -pq1.2 -g -F -C -V -N -E -a0.1 {}".format( self.tet, file_name )
        child = spawn(cmd, timeout=None)                            # Spawn child
        for line in child:                                          # Read STDOUT ...
            out = line.decode('unicode-escape').strip('\r\n')       # ... of spawned child ...
            print( out )                                            # ... process and print.
        child.close()                                               # Kill child process

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

GeoVar()
