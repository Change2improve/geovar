'''
*
* _onshape
* GEOVAR ONSHAPE SUPPORT MODULE
*
* Module designed to delegate "onshape-specific" functions or operations
*
* VERSION: 0.0.1

* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh, Fluvio L. Lobo Fenoglietto
* DATE                      :   Jan. 15th, 2019 Year of Our Lord
*
'''

from    platform                    import  system                                                  # Running platform info
import  os, re                                                                                      # Dir/path manipulation, extract numerics from strings
from    datetime                    import  datetime                                                # Get date and time


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def read_doc( self ):
    '''
    READ DOC FILE
        Function responsible for reading and extracting information from
        the "doc" input file
    '''
    filename = self.input + 'doc_def.txt'
    _doc = open( filename, 'r' )
    for line in _doc:
        print( line )

    _doc.close()
    
