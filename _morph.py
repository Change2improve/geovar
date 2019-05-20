'''
*
* _morph
* GEOVAR MORPH MODULE
*
* Module designed to delegate "morphing" functions that serve the GEOVAR class
*
* VERSION: 0.0.1

* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh, Fluvio L. Lobo Fenoglietto
* DATE                      :   May 20th, 2019 Year of Our Lord
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

