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

import  re
import  numpy                       as      np
from    onshapepy.play              import  *                               # Onshape API
from    itertools                   import  product                         # Apply product rule on combinations


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def connect_to_sketch( self, args ):
    '''
    Connect to Onshape and access desired sketch
    '''

    if( args.demo_mode ):
        self.did = "04b732c124cfa152cf7c07f3"                               # ...
        self.wid = "c4358308cbf0c97a44d8a71a"                               # Get features for document of interest
        self.eid = "a23208c314d70c14da7071e6"                               # ...

    if( len(self.did) != 24 or                                              # Ensure inputted IDs are valid
        len(self.wid) != 24 or                                              # ...
        len(self.eid) != 24 ):                                              # ...
        raise ValueError( "Document, workspace, and element IDs must each be 24 characters in length" )
    else:
        part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format( self.did, self.wid, self.eid )
        self.myPart = Part( part_URL )                                      # Connect to part for modification
        self.c      = Client()                                              # Create instance of the onshape client for exporting
    
# ------------------------------------------------------------------------

def request_status( self ):
    '''
    Decodes request status for the user
    '''

    response        = self.response
    code            = response.status_code
    if code == 200:
        print( " REQUEST SUCCESSFUL! " )
    else:
        print( " REQUEST FAILED " )
        quit()                                                              # Quitting program after failed request

# ------------------------------------------------------------------------

def get_configurations( self ):
    '''
    Get configuration parameters from Onshape document
    '''

    print('\n')
    print('REQUEST CONFIGURATIONS...')
    response        = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid))
    r               = response.json()                                       # Translate request into json() structure

    self.response   = response                                              # Storing variables into self container
    self.r          = r                                                     # ...


    request_status( self )                                                  # The status function will print the status of the request

# ------------------------------------------------------------------------

def get_values( self, ):
    '''
    Extracts the values of the Onshape document configurations
    '''

    res = self.res

    
    

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
    '''
# ------------------------------------------------------------------------

def morph_geometry( self ):
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
        
    ranges      = [range(arr.shape[1])] * arr.shape[0]              # Range we would like to go through
    b           = np.array( list(product(*ranges)) )                # Create an array of indices of the products

    param_prvs  = np.copy( arr.T[0] )                               # Previous unchanged value of the parameters
    param_crnt  = np.zeros_like( param_prvs )

    fmt_str = str()
    for name in self.keys:                                          # Build row with key names
        fmt_str = "{}\t\t{}".format( fmt_str, name )                # for visual presentation
    fmt_str = "{}\t\tt_regen".format( fmt_str )                     # ...

    self.len_cte = len(fmt_str) * round(len(self.keys)/2)           # Format length constant
    
    # ------ Mutate  Part ------
    self.i = 0
    for i in range( 0, b.shape[0] ):                                # Loop over ALL possible combinations
        print( fmt_str )                                            #   [INFO] Print FORMATTED key names
        print( "=" * self.len_cte )                                 #   [INFO] Print adaptive width dashes
        print( "{:8}:".format("SENT"), end='\t' )                   #   [INFO] Print values

        temp    = str()                                             #   Temporary string to hold filename
        start   = time()                                            #   Timer for regeneration time
        
        for j in range( 0, arr.shape[0] ):                          #   Loop over ALL features
            param_crnt[j] = arr.T[b[i][j]][j]                       #       Get current value to be passed
            
            if( param_crnt[j] != param_prvs[j] ):                   #       If current and previous parameters are different
                self.myPart.params = { self.keys[j]:                #           Pass new value (aka mutate part)
                                       param_crnt[j]*u.mm }         #           ...

                param_prvs[j] = param_crnt[j]                       #           Update previous parameter
                self.i += 1
                
            else: pass                                              #       Otherwise don't do anything
            
            print( "{:4.3f}".format(param_crnt[j]), end='\t\t' )    #       [INFO] Print value being sent to Onshape

            temp = "{}{}{}__".format( temp, self.keys[j],           #       Build file name
                                      param_crnt[j] )               #       ...
            
        print( "{:4.3f}".format(time() - start) )                   #       [INFO] Print regeneration time
        print( "-" * self.len_cte )                                 #       [INFO] Print break lines

        # get the STL export
        file = "{}{}.stl".format( self.dst, temp.rstrip('_') )      #       Build file name
        
        self.check_default( param_crnt )                            #       Check if part regenerated properly

        if( self.allow_export ):                                    #       Export the STL file
            self.export_stl( file )                                 #       ...

    # --- Revert to defaults ---
    print( "*" * self.len_cte )                                     # [INFO] Print break lines
    print( "RESULTS:-" )                                            # ...
    print( "  {:5} mutations performed".format(b.shape[0]) )        # ...
    print( "    {:5} successful mutations".format(self.valid_mutations))
    print( "    {:5} failed     mutations".format(b.shape[0]-self.valid_mutations))
    print( "  {:5} calls to Onshape".format(self.i) )
    print( "*" * self.len_cte )                                     # [INFO] Print break lines

    self.reset_myPart()                                             # Go back to defaults
