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

# Python Libraries and Modules
import  sys, os
import  re
import  numpy                       as      np
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays
import  json

# Onshape Libraries and Modules
from    onshapepy.play              import  *                               # Onshape API

# Geovar Libraries and Modules
from    _performance                import  *

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def connect_to_sketch( self, args ):
    '''
    CONNECT TO ONSHAPE DOCUMENT
    '''
    
    print('[{:0.6f}] Connecting to Onshape document'.format(current_time( self )))
    
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
    RETRIEVE LIST OF PARTS IN ONSHAPE DOCUMENT
    '''
    
    print('[{:0.6f}] Getting list of parts from Onshape document'.format(current_time( self )))
    
    self.prog_time              = time() - self.prog_start_time
    print( "[{:0.6f}] Request list of parts from Onshape".format(self.prog_time) )

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
    REQUEST STATUS
    '''
    
    code                        = response.status_code                      # Read code from the request/response structure (.status_code)
    if code == 200:
        print( "[{:0.6f}] Request successful".format(self.prog_time) )
    else:
        print( "[{:0.6f}] Request failed... quiting program...".format(self.prog_time) )
        quit()                                                              # Quitting program after failed request

# ------------------------------------------------------------------------

def get_configurations( self ):
    '''
    GET CONFIGURATIONS PARAMETERS
    '''

    print('[{:0.6f}] Getting configuration parameters from the Onshape document'.format(current_time( self )))

    r                           = self.r                                                # Load dict from self structure
    r_iter                      = self.variant_iter                                     # Using the variant iter variable to define the iteration
    r[str(r_iter)]              = {}                                                    # Initializing the array for...
    r[str(r_iter)]['raw']       = []                                                    # ...raw response
    r[str(r_iter)]['decoded']   = []                                                    # ...decoded
    
    response                    = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid))
    request_status( self, response )                                                    # The status function will print the status of the request
    r[str(r_iter)]['time']      = current_time( self )                                  # Measure time of the request with respect to the beginning of the program
    r[str(r_iter)]['raw']       = response
    r[str(r_iter)]['decoded']   = json.loads(response.text)                             # Translate request into json() structure
    
    self.r                      = r                                                     # Updating dict

# ------------------------------------------------------------------------

def get_values( self, ):
    '''
    GET VALUES FROM CONFIGURATION REQUEST
    '''

    print('[{:0.6f}] Extracting values from configuration request'.format(current_time( self )))
    
    r                                       = self.r                                                                                # Load dict from self structure
    r_iter                                  = self.variant_iter                                                                     # Using the variant iter variable to define the iteration
    Nconfigs                                = len(r[str(r_iter)]['decoded']['currentConfiguration'])                                # Determine the number of available configurations
    configs                                 = self.configs
    c_iter                                  = r_iter
    configs[str(c_iter)]                    = {}
    configs[str(c_iter)]['Nconfigs']        = Nconfigs
    configs[str(c_iter)]['parameterId']     = []
    configs[str(c_iter)]['units']           = []
    configs[str(c_iter)]['value']           = []
    for i in range( 0, Nconfigs ):                                                                                                  # Extract configuration information and populat dict iteraively
        configs[str(c_iter)]['parameterId'].append(  r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['parameterId'] )
        configs[str(c_iter)]['units'].append(        r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['units'] )
        configs[str(c_iter)]['value'].append(        r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['defaultValue'] )
        print( "[{:0.6f}] \t {} \t {} \t {} ".format(self.prog_time, configs[str(c_iter)]['parameterId'][i], str(configs[str(c_iter)]['value'][i]), configs[str(c_iter)]['units'][i]))

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
    UPDATE CONFIGURATIONS
    '''

    print('[{:0.6f}] Update configurations'.format(current_time( self )))
    
    r                                       = self.r                                                                                # Load dict from self structure
    configs                                 = self.configs                                                                          # ...
    p                                       = self.p

    r_iter                                  = self.variant_iter                                                                     # Using the variant iter variable to define the iteration
    c_iter                                  = r_iter                                                                                # iteration number for configurations structure
    p_iter                                  = r_iter                                                                                # ...for payload structure

    p[str(p_iter)]                          = r[str(r_iter)]                                                                        # initialize payload structure by copying the contents of r
    
    Nconfigs                                = configs[str(c_iter)]['Nconfigs']                                                      # Number of configurations
    Nupdates                                = len(updates)

    if ( Nconfigs != Nupdates ):
        print('[{:0.6f}] FATAL ERROR :: The number of updated values is different from the number of configurations'.format(current_time( self )) )
        quit()
    
    for i in range( 0, Nconfigs ):
        p[str(p_iter)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['defaultValue'] = updates[i]
        print( "[{:0.6f}] \t {} \t {} mm".format(self.prog_time, p[str(p_iter)]['decoded']['configurationParameters'][i]['message']['parameterId'], updates[i] ))

    payload = p[str(p_iter)]['decoded']
    response                                = self.c._api.request('post','/api/partstudios/d/{}/w/{}/e/{}/configuration'.format(self.did, self.wid, self.eid),body=json.dumps(payload))                                                                             # Send configuration changes
    request_status( self, response )                                                                                                # The status function will print the status of the request

# ------------------------------------------------------------------------

def export_stl( self ):
    '''
    EXPORT STL OF GENERATED PART/VARIANT
    '''

    print('[{:0.6f}] Export new configurations from Onshape'.format(current_time( self )))

    variant_iter                            = self.variant_iter
    partname                                = self.partname
    dest                                    = self.dst

    stl = self.c._api.request('get','/api/partstudios/d/{}/w/{}/e/{}/stl'.format(self.did, self.wid, self.eid))


    stl_filename = ('{}{}_var{}.stl'.format(dest, partname, variant_iter))
    
    with open( stl_filename, 'w' ) as f:                                                                                            # Write STL to file
        f.write( stl.text )

    self.stl_filename                       = stl_filename 
    

# ------------------------------------------------------------------------
