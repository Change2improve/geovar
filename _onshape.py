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

def read_doc( self, filename = 'doc_def.txt' ):
    '''
    READ DOC FILE
        Function responsible for reading and extracting information from
        the "doc" input file
    '''
    print( '' )
    print( "READ DOC FILE..." )
    filepath = self.input + filename
    _doc = open( filepath, 'r' )
    for line in _doc:
        if line[0] == '>':
            address = line
            self.address = address[1:]                                                              # Store the url/web address of the onshape part/document
            break

    address = address.split("/")
    for i in range( 0, len( address ) ):
        if address[i] == 'documents':
            self.did = address[i+1]                                                                 # Store the document id
        elif address[i] == 'w':
            self.wid = address[i+1]                                                                 # Store the workspace id
        elif address[i] == 'e':
            self.eid = address[i+1]                                                                 # Store the element id

    print( ">> DOCUMENT" + '\t' + "ID: " + self.did )
    print( ">> WORKSPACE" + '\t' + "ID: " + self.wid )
    print( ">> ELEMENT" + '\t' + "ID: " + self.eid )

    _doc.close()
    
# ------------------------------------------------------------------------

def read_vars( self, filename = 'vars_def.txt' ):
    '''
    READ VARS FILE
        Function responsible for reading and extracting information from
        the "vars" input file
    '''
    print( '' )
    print( "READ VARS FILE..." )
    filepath = self.input + filename
    _vars = open( filepath, 'r' )
    for line in _vars:
        if line[0] == '>':
            address = line
            self.address = address[1:]                                                              # Store the url/web address of the onshape part/document
            break

    address = address.split("/")
    for i in range( 0, len( address ) ):
        if address[i] == 'documents':
            self.did = address[i+1]                                                                 # Store the document id
        elif address[i] == 'w':
            self.wid = address[i+1]                                                                 # Store the workspace id
        elif address[i] == 'e':
            self.eid = address[i+1]                                                                 # Store the element id

    print( ">> DOCUMENT" + '\t' + "ID: " + self.did )
    print( ">> WORKSPACE" + '\t' + "ID: " + self.wid )
    print( ">> ELEMENT" + '\t' + "ID: " + self.eid )

    _doc.close()
