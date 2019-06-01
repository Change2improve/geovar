'''
*
* _setup
* GEOVAR SETUP SUPPORT MODULE
*
* Module designed to delegate "setup" functions that serve the GEOVAR class
*
* VERSION: 0.0.1

* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh, Fluvio L. Lobo Fenoglietto
* DATE                      :   Jan. 10th, 2019 Year of Our Lord
*
'''


# additional python modules and libraries
import  os, re                                                                                      # Dir/path manipulation, extract numerics from strings
import  sys
import  numpy                       as      np
from    platform                    import  system                                                  # Running platform info
from    datetime                    import  datetime                                                # Get date and time
from    lxml                        import  etree
from    itertools                   import  product                                                 # Apply product rule on combinations

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def setup_input_directory( self ):
    '''
    Locates the path to the input files;
        - The repository structure
        - On a Windows OS
    '''
    print( '\n' )
    print( "SETUP INPUT DIR..." )
    dir_list = os.listdir()                                                                         # List elements within current directory
    dir_len  = len(dir_list)
    test_string = 'input'
    test_string_len = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                print( ">> FOUND" + '\t' + "DIR ...geovar\\" + dir_list[i] )
                match_index = i
                break

    current_dir = os.getcwd()
    input_dir = current_dir + '\\' + dir_list[match_index] + '\\'
    print( ">> CURRENT" + '\t' + "DIR: " + current_dir )
    print( ">> INPUT" + '\t' + "DIR: " + input_dir )

    self.input = input_dir                                                                           # Passing tetgen path to the .self structure
           
# ------------------------------------------------------------------------

def setup_tetgen_directory( self ):
    '''
    Locates the path to the tetgen application within;
        - The repository structure
        - On a Windows OS
    '''
    print( '\n' )
    print( "SETUP TETGEN DIR..." )
    dir_list                    = os.listdir()                                                                         # List elements within current directory
    dir_len                     = len(dir_list)
    test_string                 = 'tetgen'
    test_string_len             = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                print( ">> FOUND" + '\t' + "DIR ...geovar\\" + dir_list[i] )
                match_index = i
                break

    current_dir                 = os.getcwd()
    tetgen_dir                  = '{}\\{}\\build\\Debug\\'.format(current_dir,dir_list[match_index])
    print( ">> CURRENT" + '\t' + "DIR: " + current_dir )
    print( ">> TETGEN" + '\t' + "DIR: " + tetgen_dir )

    self.tet = tetgen_dir                                                                           # Passing tetgen path to the .self structure
           
# ------------------------------------------------------------------------

def setup_directories( self ):
    '''
    Create output folder and point to
    location of compiled TetGen program
    '''

    # ------ UNIX systems ------
    if( system()=='Linux' ):
        src                     = os.getcwd()
        self.dst                = "{}/output/{}/".format( src,
                                                          datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
        self.tet                = args.tetgen_dir                                                                  # Setup tetgen directory

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
        src                     = os.getcwd()
        self.input              = "{}\\input\\".format( src )                                                    # Setup input directory
        self.doc_def            = self.input + 'doc_def.txt'
        self.dst                = "{}\\output\\{}\\".format( src,
                                                             datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )

        setup_input_directory( self )
        setup_tetgen_directory( self )                                                                  

        try:
            os.makedirs( self.dst )
        except WindowsError:
            print( "FAILED to create directory. Check permissions" )
            quit()
##        else:
##            print( "Created {}".format(self.dst) )

# ------------------------------------------------------------------------

def read_doc( self, filename ):
    '''
    READ DOC INFO
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    print( '\n' )
    print( "READ DOC INFO..." )
    file                        = self.input + filename

    _doc = etree.parse( file )
    _doc_address_ele            = _doc.find('address')
    _doc_address_text           = _doc_address_ele.text
    _doc_address_text           = _doc_address_text.split("/")
    for i in range( 0, len( _doc_address_text ) ):
        if _doc_address_text[i] == 'documents':
            self.did = _doc_address_text[i+1]                                                           # Store the document id
        elif _doc_address_text[i] == 'w':
            self.wid = _doc_address_text[i+1]                                                           # Store the workspace id
        elif _doc_address_text[i] == 'e':
            self.eid = _doc_address_text[i+1]                                                           # Store the element id
            
    print( ">> DOCUMENT" + '\t' + "ID: " + self.did )
    print( ">> WORKSPACE" + '\t' + "ID: " + self.wid )
    print( ">> ELEMENT" + '\t' + "ID: " + self.eid )
    
# ------------------------------------------------------------------------

def read_vars( self, filename ):
    '''
    READ VAR INFO
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    print( '\n' )
    print( "READ VAR INFO..." )
    file = self.input + filename

    _doc = etree.parse( file )
    _doc_vars_ele = _doc.find('variables')

    var                         = {}
    var['nvar']                 = len(_doc_vars_ele)
    var['names']                = []
    print( ">> NUMBER OF VARIABLES" + '\t' + str(var['nvar']) )

    for i in range(0, len(_doc_vars_ele) ):
        var_name                = _doc_vars_ele[i].get("name")
        var['names'].append( _doc_vars_ele[i].get("name") )
        var[var_name]           = {}
        var[var_name]['start']  = float( _doc_vars_ele[i].get("start") )
        var[var_name]['stop']   = float( _doc_vars_ele[i].get("stop") )
        var[var_name]['np']     = int( _doc_vars_ele[i].get("np") )
        var[var_name]['ep']     = int( _doc_vars_ele[i].get("ep") )
        print( ">> " + str(var_name) + '\t' + str(var[var_name]['start']) + '\t' + str(var[var_name]['stop']) + '\t' + str(var[var_name]['np']) + '\t' + str(var[var_name]['ep']) )

    #print( var )

    # storing updated variables into self structure  
    self.var                    = var


# ------------------------------------------------------------------------

def generate_variant_array( self ):
    '''
    GENERATE GEOMETRIC VARIANT ARRAY
        - Generates the array of values for every input variable
        - Generates all possible combinations for all possible values of each variable
    '''

    # interpolating morphing values based on user input
    print( '\n' )
    print( "PREPARING VARIANT ARRAY..." )
    
    var                         = self.var                                                              # Load var from self structure 
    arr                         = []                                                                    # Define array 'arr' which will contain all the user input values for each user input variable
    for i in range(0, var['nvar']):                                                                     # Populate 'arr'
        _name                   = var['names'][i]
        _start                  = var[_name]['start']
        _stop                   = var[_name]['stop']
        _np                     = var[_name]['np']
        _ep                     = var[_name]['ep']
        var[_name]['vals']      = []
        var[_name]['vals']      = np.linspace( _start, _stop, _np, _ep )                                # Generate values using linspace
        arr.append( var[_name]['vals'] )
        print( (">> {} \t vals: {}").format(_name,str(var[_name]['vals'])))                             # Reporting

    arr = np.array(arr)                                                                                 # Convert 'arr' into a numpy array
    
    vals_range                  = list( range( arr.shape[1] ) )
    prods                       = list( product( vals_range, repeat = arr.shape[0] ) )                  # Calculate all possible variable combinations, considering all the values for each variable
    print("\n")
    print( (">> WARNING: THIS PROGRAM WILL GENERATE {} GEOMETRIC VARIANTS (.STL)...").format(len(prods)))
    query_variants( ">> Do you wish to continue?", default="yes")
        
    self.var                    = var                                                                   # Load changes to 'self' structure
    self.arr                    = arr
    self.prods                  = prods

# ------------------------------------------------------------------------

def query_variants(question, default="yes"):
    """
    STOP:
        - Halts process until user reviews information
    """
    valid           = {"yes": True, "y": True, "ye": True,
                       "no": False, "n": False}
    if default is None:
        prompt      = " [y/n] "
    elif default    == "yes":
        prompt      = " [Y/n] "
    elif default    == "no":
        prompt      = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            if valid[choice] == False:
                print(">> Terminating program...")
                quit()
            else:
                print(">> Proceed at your own risk..!")
                return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
