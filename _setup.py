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

def read_doc( self, filename = 'doc_def.xml' ):
    '''
    READ DOC FILE
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    print( '\n' )
    print( "READ DOC FILE..." )
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

def read_vars( self, filename = 'doc_def.xml' ):
    '''
    READ DOC FILE
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    print( '\n' )
    print( "READ DOC FILE..." )
    file = self.input + filename

    _doc = etree.parse( file )
    _doc_vars_ele = _doc.find('variables')

    var_name    = []                                                                                    # list of variable names
    var_start   = []                                                                                    # ... ... start points
    var_stop    = []                                                                                    # ... ... stop points
    var_np      = []                                                                                    # ... ... number of points
    var_ep      = []                                                                                    # ... ... end point constraint
    for i in range(0, len(_doc_vars_ele) ):
        var_name.append(    _doc_vars_ele[i].get("name")    )
        var_start.append(   _doc_vars_ele[i].get("start")   )
        var_stop.append(    _doc_vars_ele[i].get("stop")    )
        var_np.append(      _doc_vars_ele[i].get("np")      )
        var_ep.append(      _doc_vars_ele[i].get("ep")      )

    print( var_name, var_start, var_stop, var_np, var_ep )
        
    self.var_name   = var_name
    self.var_start  = var_start
    self.var_stop   = var_stop
    self.var_np     = var_np
    self.var_ep     = var_ep
    
    
# ------------------------------------------------------------------------
