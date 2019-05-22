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
from    time                        import  sleep, time                 # Timers/delays
import  json


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

    r                           = self.r                                                # Load dict from self structure
    r_iter                      = len(r)
    response                    = r[str(r_iter - 1)]['raw']                             # Extract the latest response [i-1]
    code                        = response.status_code                                  # Read code from the request/response structure (.status_code)
    if code == 200:
        print( ">> REQUEST SUCCESSFUL! " )
    else:
        print( ">> REQUEST FAILED " )
        quit()                                                                          # Quitting program after failed request

# ------------------------------------------------------------------------

def get_configurations( self ):
    '''
    Get configuration parameters from Onshape document
    '''

    print('\n')
    print('REQUEST CONFIGURATIONS...')

    r                           = self.r                                                # Load dict from self structure
    r_iter                      = len(r)                                                # Dummy variable that determines the response iteration based on the number of requests
    r[str(r_iter)]              = {}                                                    # Initializing the array for...
    r[str(r_iter)]['raw']       = []                                                    # ...raw response
    r[str(r_iter)]['decoded']   = []                                                    # ...decoded
    
    response                    = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid))
    r[str(r_iter)]['time']      = time() - self.prog_start_time                         # Measure time of the request with respect to the beginning of the program
    r[str(r_iter)]['raw']       = response
    r[str(r_iter)]['decoded']   = response.json()                                       # Translate request into json() structure
    
    self.r                      = r                                                     # Updating dict

    request_status( self )                                                              # The status function will print the status of the request

# ------------------------------------------------------------------------

def get_values( self, ):
    '''
    Extracts the values of the Onshape document configurations

    TO DO:
        - Add the limits of the configurations

    '''

    r                           = self.r                                                                                            # Load dict from self structure
    r_iter                      = len(r)                                                                                            # Dummy variable that determines the response iteration based on the number of requests
    Nconfigs                    = len( r[str(r_iter - 1)]['decoded']['currentConfiguration'] )                                      # Determine the number of available configurations
    configs                     = {}                                                                                                # Create a dict to store information about the configurations (temporary stucture)
    configs['Nconfigs']         = Nconfigs
    configs['parameterId']      = []
    configs['units']            = []
    configs['value']            = []
    configs['expression']       = []
    print( ">> NUMBER OF CONFIGURATIONS" + '\t' + str(Nconfigs) )
    for i in range( 0, Nconfigs ):                                                                                                  # Extract configuration information and populat dict iteraively
        configs['parameterId'].append(  r[str(r_iter - 1)]['decoded']['currentConfiguration'][i]['message']['parameterId'] )
        configs['units'].append(        r[str(r_iter - 1)]['decoded']['currentConfiguration'][i]['message']['units'] )
        configs['value'].append(        r[str(r_iter - 1)]['decoded']['currentConfiguration'][i]['message']['value'] )
        configs['expression'].append(   r[str(r_iter - 1)]['decoded']['currentConfiguration'][i]['message']['expression'] )
        print( ">> " + configs['parameterId'][i] + '\t' + str(configs['value'][i]) + '\t' + configs['units'][i])
        
    self.configs            = configs
    
# ------------------------------------------------------------------------

def check_values( self, ):
    '''
    Checks if the values provided by the user match those available to the file

    TO DO:
        - Uses the number of configurations and parameterIds to check
        - Throws a warning or ends the program

    '''

# ------------------------------------------------------------------------

def update_configurations( self, ):
    '''
    Updates the configuration values on the onshape document
    '''

    r                       = self.r                                                                                                # Load variables from the self structure                                                                                                               
    configs                 = self.configs

    Nconfigs                = configs['Nconfigs']
    for i in range( 0, Nconfigs ):
        r['currentConfiguration'][i]['message']['value'] = 73.50 #configs['parameterId'][i]
        r['currentConfiguration'][i]['message']['expression'] = '73.50 mm' #configs['parameterId'][i]

    payload = r
    print( payload )
    response                = self.c._api.request('post',                                                           
                                          '/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid),
                                          body=json.dumps(payload))                                                                             # Send configuration changes
    print( response )
    

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
