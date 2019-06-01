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

import  sys, os
import  re
import  numpy                       as      np
from    onshapepy.play              import  *                               # Onshape API
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays
import  json


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def connect_to_sketch( self, args ):
    '''
    Connect to Onshape and access desired sketch
    '''

##    if( args.demo_mode ):
##        self.did = "04b732c124cfa152cf7c07f3"                               # ...
##        self.wid = "c4358308cbf0c97a44d8a71a"                               # Get features for document of interest
##        self.eid = "a23208c314d70c14da7071e6"                               # ...

    if( len(self.did) != 24 or                                              # Ensure inputted IDs are valid
        len(self.wid) != 24 or                                              # ...
        len(self.eid) != 24 ):                                              # ...
        raise ValueError( "Document, workspace, and element IDs must each be 24 characters in length" )
    else:
        part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format( self.did, self.wid, self.eid )
        self.myPart = Part( part_URL )                                      # Connect to part for modification
        self.c      = Client()                                              # Create instance of the onshape client for exporting
    
# ------------------------------------------------------------------------

def get_list_of_parts( self ):
    '''
    Get list of parts
    '''
    
    self.prog_time              = time() - self.prog_start_time
    print( "> REQUEST LIST OF PARTS... \t {}".format(self.prog_time) )
    print( " --------------------------------------------------------- " )

    response                    = self.c._api.request('get','/api/parts/d/{}/w/{}'.format(self.did, self.wid))
    request_status( self, response )                                        # The status function will print the status of the request
    res                         = json.loads(response.text)
    
    if len(res) == 1:
        partname                = res[0]['name']
        partname                = partname.replace( " ", "_" )              # This ensures that unix versions wont have issues reading the filename


    self.partname               = partname
    
# ------------------------------------------------------------------------

def request_status( self, response ):
    '''
    Decodes request status for the user
    '''

    code                        = response.status_code                      # Read code from the request/response structure (.status_code)
    if code == 200:
        pass
        #print( ">> REQUEST SUCCESSFUL! " )
        #print( " --------------------------------------------------------- " )
    else:
        print( ">> REQUEST FAILED " )
        print( " --------------------------------------------------------- " )
        quit()                                                              # Quitting program after failed request

# ------------------------------------------------------------------------

def get_configurations( self ):
    '''
    Get configuration parameters from Onshape document
    '''

    self.prog_time              = time() - self.prog_start_time
    print( ">> GET CONFIGURATIONS... \t {}".format(self.prog_time) )
    print( " --------------------------------------------------------- " )

    r                           = self.r                                                # Load dict from self structure
    r_iter                      = len(r)                                                # Dummy variable that determines the response iteration based on the number of requests
    r[str(r_iter)]              = {}                                                    # Initializing the array for...
    r[str(r_iter)]['raw']       = []                                                    # ...raw response
    r[str(r_iter)]['decoded']   = []                                                    # ...decoded
    
    response                    = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid))
    request_status( self, response )                                                    # The status function will print the status of the request
    r[str(r_iter)]['time']      = time() - self.prog_start_time                         # Measure time of the request with respect to the beginning of the program
    r[str(r_iter)]['raw']       = response
    r[str(r_iter)]['decoded']   = json.loads(response.text)                             # Translate request into json() structure
    
    self.r                      = r                                                     # Updating dict

# ------------------------------------------------------------------------

def get_values( self, ):
    '''
    Extracts the values of the Onshape document configurations

    TO DO:
        - Add the limits of the configurations

    '''

    self.prog_time              = time() - self.prog_start_time
    
    r                                       = self.r                                                                                # Load dict from self structure
    r_iter                                  = len(r)                                                                                # Dummy variable that determines the response iteration based on the number of requests
    Nconfigs                                = len( r[str(r_iter - 1)]['decoded']['currentConfiguration'] )                          # Determine the number of available configurations
    configs                                 = self.configs
    c_iter                                  = len(configs)
    configs[str(c_iter)]                    = {}
    configs[str(c_iter)]['Nconfigs']        = Nconfigs
    configs[str(c_iter)]['parameterId']     = []
    configs[str(c_iter)]['units']           = []
    configs[str(c_iter)]['value']           = []
    #configs[str(c_iter)]['expression']      = []
    print( ">> NUMBER OF CONFIGURATIONS" + '\t' + str(Nconfigs) )
    for i in range( 0, Nconfigs ):                                                                                                  # Extract configuration information and populat dict iteraively
        configs[str(c_iter)]['parameterId'].append(  r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['parameterId'] )
        configs[str(c_iter)]['units'].append(        r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['units'] )
        configs[str(c_iter)]['value'].append(        r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['defaultValue'] )
        #configs[str(c_iter)]['expression'].append(   r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['expression'] )
        print( ">> " + configs[str(c_iter)]['parameterId'][i] + '\t' + str(configs[str(c_iter)]['value'][i]) + '\t' + configs[str(c_iter)]['units'][i])
    print( " --------------------------------------------------------- " )
    self.configs            = configs
    
# ------------------------------------------------------------------------

def check_values( self, ):
    '''
    Checks if the values provided by the user match those available to the file

    TO DO:
        - Uses the number of configurations and parameterIds to check
        - Throws a warning or ends the program
        - Use the configuration file to see if there was an actual change in the part

    '''

# ------------------------------------------------------------------------

def update_configurations( self, updates ):
    '''
    Updates the configuration values on the onshape document

    TO DO:
        - Update values from input array 'new_vals'
        - Ensure that the program is smart enough to check the 'parameter_id' name rather than just the iterative order
    '''

    self.prog_time                          = time() - self.prog_start_time
    print( ">> SIMPLE MORPH... \t {}".format(self.prog_time) )
    print( " --------------------------------------------------------- " )
    
    r                                       = self.r                                                                                # Load dict from self structure
    r_iter                                  = len(r)                                                                                # Dummy variable that determines the response iteration based on the number of requests
    configs                                 = self.configs                                                                          # ...
    c_iter                                  = len(configs)
    Nconfigs                                = configs[str(c_iter - 1)]['Nconfigs']                                                  # Number of configurations
    Nupdates                                = len(updates)

    if ( Nconfigs != Nupdates ):
        print( ">> ERROR: The number of updated values is different from the number of configurations... ending program..." )
        quit()
    
    for i in range( 0, Nconfigs ):
        r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['defaultValue'] = updates[i]
        #r[str(r_iter - 1)]['decoded']['currentConfiguration'][i]['message']['expression'] = ('{} mm').format( updates[i] )
        print( ">> " + r[str(r_iter - 1)]['decoded']['configurationParameters'][i]['message']['parameterId'] + '\t' + ('{} mm').format( updates[i] ))

    payload = r[str(r_iter - 1)]['decoded']
    response                                = self.c._api.request('post','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid),body=json.dumps(payload))                                                                             # Send configuration changes
    request_status( self, response )                                                                                                # The status function will print the status of the request

# ------------------------------------------------------------------------

def export_stl( self ):
    '''
    EXPORT STL OF GENERATED PART/VARIANT
    '''

    self.prog_time                          = time() - self.prog_start_time
    print( ">> EXPORT STL... \t {}".format(self.prog_time) )
    print( " --------------------------------------------------------- " )

    variant_iter                            = self.variant_iter
    partname                                = self.partname
    dest                                    = self.dst

    stl = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/stl'.format(self.did, self.wid, self.eid))


    stl_filename = ('{}{}_var{}.stl'.format(dest, partname, variant_iter))
    
    with open( stl_filename, 'w' ) as f:                                                                                            # Write STL to file
        f.write( stl.text )

    self.stl_filename                       = stl_filename 
    

# ------------------------------------------------------------------------
