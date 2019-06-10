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


# Python Libraries and Modules
import  os, re                                                                                      # Dir/path manipulation, extract numerics from strings
import  sys
import  numpy                       as      np
from    time                        import  sleep, time                 # Timers/delays
from    platform                    import  system                                                  # Running platform info
from    datetime                    import  datetime                                                # Get date and time
from    lxml                        import  etree
from    itertools                   import  product                                                 # Apply product rule on combinations

# Geovar Libraries and Modules
from    _performance                import  *

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def setup_input_directory( self ):
    '''
    SETUP INPUT DIRECTORY
    '''

    print('[{:0.6f}] Setup input directory'.format(current_time( self )))
    current_dir                 = os.getcwd()
    input_dir                   = '{}\\input\\'.format( current_dir )

    if os.path.exists( input_dir ) == False:
        print('[{:0.6f}] FATAL ERROR :: No input directory detected'.format(current_time( self )))
        #os.makedirs( input_dir )
    else:
        print('[{:0.6f}] Input directory found'.format(current_time( self )))
        
    self.current_dir            = current_dir
    self.input_dir              = input_dir                                                         # Passing tetgen path to the .self structure

# ------------------------------------------------------------------------

def setup_output_directory( self ):
    '''
    SETUP OUTPUT DIRECTORY
    '''

    self.prog_time              = time() - self.prog_start_time
    print('[{:0.6f}] Setup output directory'.format(current_time( self )))
    current_dir                 = os.getcwd()
    output_dir                  = '{}\\output\\'.format( current_dir )
    dst                         = '{}{}\\'.format( output_dir, datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )

    # ----------------------------------------------------------------------------------------------------------------- # create output (main) directory, if not yet created
    if os.path.exists( output_dir ) == False:
        print('[{:0.6f}] WARNING :: No output directory found... generating...'.format(current_time( self )))
        os.makedirs( output_dir )
    else:
        print('[{:0.6f}] Output directory found'.format(current_time( self )))
    
    # ----------------------------------------------------------------------------------------------------------------- # create output (execution-specific) directory, if not yet created
    if os.path.exists( dst ) == False:
        print('[{:0.6f}] WARNING :: No destination directory found... generating...'.format(current_time( self )))
        os.makedirs( dst )
    else:
        print('[{:0.6f}] Destination directory found'.format(current_time( self )))
    
    
    self.output_dir             = output_dir
    self.dst                    = dst
    
# ------------------------------------------------------------------------

def setup_tetgen_directory( self ):
    '''
    SETUP TETGEN DIRECTORY
    '''
           
    print('[{:0.6f}] Setup TetGen directory'.format(current_time( self )))
    
    dir_list                    = os.listdir()                                                                          # List elements within current directory
    dir_len                     = len(dir_list)
    test_string                 = 'tetgen'
    test_string_len             = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                match_index = i
                break

    current_dir                 = os.getcwd()
    tetgen_dir                  = '{}\\{}\\build\\Debug\\'.format(current_dir,dir_list[match_index])
    self.tetgen_dir             = tetgen_dir                                                                           # Passing tetgen path to the .self structure
           
# ------------------------------------------------------------------------

def setup_directories( self ):
    '''
    SETUO DIRECTORIES
    '''

    # ------ UNIX systems ------
    if( system()=='Linux' ):
        print( " ERROR: geovar() has only been configured for Windows... ")
        quit()

    # ----- Windows system -----
    elif( system()=='Windows' ):
        # Define useful paths
        setup_input_directory(  self )
        setup_tetgen_directory( self )
        setup_output_directory( self )

# ------------------------------------------------------------------------

def generate_filenames( self, filename, mode ):
    '''
    GENERATE FILENAMES
        - This program works on the premise that all input filenames, in
          accordance with the program's structure, have the same "name",
          while lacking the same extension
    '''

    print('[{:0.6f}] Setup filenames'.format(current_time( self )))

    if filename.rfind('.'):
        filename_woe            = filename[:filename.rfind('.')]
    
    self.input_stl_filename = "{}.stl".format(filename_woe)
    self.input_xml_filename = "{}.xml".format(filename_woe)
    self.input_vtk_filename = "{}.vtk".format(filename_woe)
    self.input_feb_filename = "{}.feb".format(filename_woe)
           
# ------------------------------------------------------------------------

def read_doc( self, filename ):
    '''
    READ DOC INFO
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    
    print('[{:0.6f}] Reading Onshape doc. info. from input XML'.format(current_time( self )))
    
    file                        = self.input_dir + self.input_xml_filename

    if os.path.exists( file ) == False:
        print('[{:0.6f}] FATAL ERROR :: No input XML file found'.format(current_time( self )))
        quit()

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
    
# ------------------------------------------------------------------------

def read_vars( self, filename ):
    '''
    READ VAR INFO
        Function responsible for reading and extracting information from
        the "doc" input file
            doc_def contains the identification of the target document within the onshape platform
    '''
    
    print('[{:0.6f}] Reading variants info. from input XML'.format(current_time( self )))
    
    file                        = self.input_dir + self.input_xml_filename

    if os.path.exists( file ) == False:
        print('[{:0.6f}] FATAL ERROR :: No input XML file found'.format(current_time( self )))
        quit()
    
    _doc = etree.parse( file )
    _doc_vars_ele = _doc.find('variables')

    var                         = {}
    var['nvar']                 = len(_doc_vars_ele)
    var['names']                = []

    for i in range(0, len(_doc_vars_ele) ):
        var_name                = _doc_vars_ele[i].get("name")
        var['names'].append( _doc_vars_ele[i].get("name") )
        var[var_name]           = {}
        var[var_name]['start']  = float( _doc_vars_ele[i].get("start") )
        var[var_name]['stop']   = float( _doc_vars_ele[i].get("stop") )
        var[var_name]['np']     = int( _doc_vars_ele[i].get("np") )
        var[var_name]['ep']     = int( _doc_vars_ele[i].get("ep") )
        
    self.var                    = var

# ------------------------------------------------------------------------

def generate_variant_array( self ):
    '''
    GENERATE GEOMETRIC VARIANT ARRAY
        - Generates the array of values for every input variable
        - Generates all possible combinations for all possible values of each variable
    '''

    print('[{:0.6f}] Generate geomatric variants array'.format(current_time( self )))
    
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
        print(('[{:0.6f}]\t{}\tvals: {}').format(current_time(self),_name,str(var[_name]['vals'])))     # Reporting

    arr = np.array(arr)                                                                                 # Convert 'arr' into a numpy array
    
    vals_range                  = list( range( arr.shape[1] ) )
    prods                       = list( product( vals_range, repeat = arr.shape[0] ) )                  # Calculate all possible variable combinations, considering all the values for each variable
        
    self.var                    = var                                                                   # Load changes to 'self' structure
    self.arr                    = arr
    self.prods                  = prods
    self.Nprods                 = len( prods )

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
