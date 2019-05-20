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

from    onshapepy.play              import  *                           # Onshape API
import  re

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def connect_to_sketch( self, args ):
    '''
    Connect to Onshape and access desired sketch
    '''

    if( args.demo_mode ):
        self.did = "04b732c124cfa152cf7c07f3"                       # ...
        self.wid = "c4358308cbf0c97a44d8a71a"                       # Get features for document of interest
        self.eid = "a23208c314d70c14da7071e6"                       # ...

    if( len(self.did) != 24 or                                      # Ensure inputted IDs are valid
        len(self.wid) != 24 or                                      # ...
        len(self.eid) != 24 ):                                      # ...
        raise ValueError( "Document, workspace, and element IDs must each be 24 characters in length" )
    else:
        part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format( self.did, self.wid, self.eid )
        self.myPart = Part( part_URL )                              # Connect to part for modification
        self.c      = Client()                                      # Create instance of the onshape client for exporting
    
# ------------------------------------------------------------------------

def get_values( self, initRun = False ):
    '''
    Extract configured variable names from part and get the current values.
    When initRun is True, it gets the default values and stores them for later usage.

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

    if( initRun ):                                                  # If this is the initial run, get defaults
        self.keys       = list( self.myPart.params )                #   Cast dict as list to extract keys
        print( self.keys )
        self.default    = [None] * len( self.keys )                 #   Create a list of length for values

        print( "Found {} configurable parts with defaults:-".format(len(self.keys)) )
        for i in range( 0, len(self.keys) ):                        #   Loop over all dict entries
            param = str( self.myPart.params[ self.keys[i] ] )       #       Get dict value as string
            self.default[i] = float( rx.findall(param)[0] )         #       Extract value from string
            print( "  {:3}. {:12}: {: >10.3f}".format(i+1, self.keys[i], self.default[i]) )
        print( '' )
        return( 0 )

    else:
        current    = [None] * len( self.keys )                      #   Create a list of length for values
        
        print( "{:8}:".format("CURRENT"), end='\t' )
        for i in range( 0, len(self.keys) ):                        #   Loop over all dict entries
            param = str( self.myPart.params[ self.keys[i] ] )       #       Get dict value as string
            current[i] = float( rx.findall(param)[0] )              #       Extract value from string
            print( "{:4.3f}".format(current[i]), end='\t\t' )
        print("//"); print( "-" * self.len_cte )
        return( current )
        
