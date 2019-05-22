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

import  os, re                                                                                      # Dir/path manipulation, extract numerics from strings
import  numpy                       as      np
from    platform                    import  system                                                  # Running platform info
from    datetime                    import  datetime                                                # Get date and time
from    lxml                        import  etree


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
    dir_list = os.listdir()                                                                         # List elements within current directory
    dir_len  = len(dir_list)
    test_string = 'tetgen'
    test_string_len = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                print( ">> FOUND" + '\t' + "DIR ...geovar\\" + dir_list[i] )
                match_index = i
                break

    current_dir = os.getcwd()
    tetgen_dir = current_dir + '\\' + dir_list[match_index] + '\\build\\Debug\\'
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
        src      = os.getcwd()
        self.dst = "{}/output/{}/".format( src,
                                           datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
        self.tet = args.tetgen_dir                                                                  # Setup tetgen directory

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
        src             = os.getcwd()
        self.input      = "{}\\input\\".format( src )                                                    # Setup input directory
        self.doc_def    = self.input + 'doc_def.txt'
        self.dst        = "{}\\output\\{}\\".format( src,
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
    file = self.input + filename

    _doc = etree.parse( file )
    _doc_address_ele = _doc.find('address')
    _doc_address_text = _doc_address_ele.text
    _doc_address_text = _doc_address_text.split("/")
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

    var                 = {}
    var['nvar']         = len(_doc_vars_ele)
    var['names']        = []
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
    self.var            = var


# ------------------------------------------------------------------------

def generate_morphing_array( self ):
    '''
    Generates Array of Combinations, based on the variables input arrays

    things to do here:
    1. generate variable arrays
    2. verify consistency between input file variable and configuration (future function called check_values())
    '''

    # interpolating morphing values based on user input
    print( '\n' )
    print( "PREPARING MORPHING ARRAY..." )
    
    var     = self.var
    arr     = []
    for i in range(0, var['nvar']):
        _name               = var['names'][i]
        _start              = var[_name]['start']
        _stop               = var[_name]['stop']
        _np                 = var[_name]['np']
        _ep                 = var[_name]['ep']
        var[_name]['vals']  = []
        var[_name]['vals']  = np.linspace( _start, _stop, _np, _ep )
        arr.append( var[_name]['vals'] )

        # reporting results
        print( ">> " + _name + '\t' + "vals: " + str( var[_name]['vals'] ) )

    self.var = var
    arr = np.array(arr)
    self.arr = arr

