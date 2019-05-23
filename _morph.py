'''
*
* _morph
* GEOVAR MORPH MODULE
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

# onshape modules and libraries
from    onshapepy.play              import  *                               # Onshape API


# adapted onshape modules and libraries
import  _morph


# additional python modules and libraries
import  re
import  numpy                       as      np
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def morph_geometry( self, updates ):
    '''
    Morph or modify geometries based on a product array
    '''

    arr = self.arr

    vals_range = list( range( arr.shape[1] ) )
    prods = list( product( vals_range, repeat = arr.shape[0] ) )
    
    param_prvs  = np.copy( arr[:,0] )                               # Previous unchanged value of the parameters
    print( param_prvs )
    param_crnt  = np.zeros_like( param_prvs )
    print( param_crnt )

    fmt_str = str()
    for name in self.keys:                                          # Build row with key names
        fmt_str = "{}\t\t{}".format( fmt_str, name )                # for visual presentation
    fmt_str = "{}\t\tt_regen".format( fmt_str )                     # ...

    self.len_cte = len(fmt_str) * round(len(self.keys)/2)           # Format length constant
    
    # ------ Mutate  Part ------
    self.i = 0
    for i in range( 0, 3 ):                                         # Loop over ALL possible combinations
        #print( fmt_str )                                            #   [INFO] Print FORMATTED key names
        #print( "=" * self.len_cte )                                 #   [INFO] Print adaptive width dashes
        #print( "{:8}:".format("SENT"), end='\t' )                   #   [INFO] Print values

        temp    = str()                                             #   Temporary string to hold filename
        start   = time()                                            #   Timer for regeneration time

        for j in range( 0, arr.shape[0] ):                          #   Loop over ALL features
            param_crnt[j] = arr[j][prods[i][j]]                     #       Get current value to be passed

            print( self.myPart.params[self.keys[j]] )
            print( self.keys[j] )
            print( param_crnt[j] )
            self.myPart.params[self.keys[j]] = param_crnt[j]*u.mm             #           ...
            #assert self.myPart.params == { self.keys[j]:param_crnt[j]*u.mm }
            print( self.myPart.params[self.keys[j]] )
            param_prvs[j] = param_crnt[j]                           #           Update previous parameter
            self.i += 1
            
            '''
            if( param_crnt[j] != param_prvs[j] ):                   #       If current and previous parameters are different
                self.myPart.params = { self.keys[j]:                #           Pass new value (aka mutate part)
                                       param_crnt[j]*u.mm }         #           ...

                param_prvs[j] = param_crnt[j]                       #           Update previous parameter
                self.i += 1
                
            else: pass                                              #       Otherwise don't do anything
            '''
            
            #print( "{:4.3f}".format(param_crnt[j]), end='\t\t' )    #       [INFO] Print value being sent to Onshape

            temp = "{}{}{}__".format( temp, self.keys[j],           #       Build file name
                                      param_crnt[j] )               #       ...
        print( param_crnt )
          
        print( "{:4.3f}".format(time() - start) )                   #       [INFO] Print regeneration time
        print( "-" * self.len_cte )                                 #       [INFO] Print break lines

        # get the STL export
        file = "{}{}.stl".format( self.dst, temp.rstrip('_') )      #       Build file name
        
        #self.check_default( param_crnt )                            #       Check if part regenerated properly

        #if( self.allow_export ):                                    #       Export the STL file
        #self.export_stl( file )                                 #       ...

    # --- Revert to defaults ---
    print( "*" * self.len_cte )                                     # [INFO] Print break lines
    print( "RESULTS:-" )                                            # ...
    print( "  {:5} mutations performed".format(arr.shape[0]) )        # ...
    print( "    {:5} successful mutations".format(self.valid_mutations))
    print( "    {:5} failed     mutations".format(arr.shape[0]-self.valid_mutations))
    print( "  {:5} calls to Onshape".format(self.i) )
    print( "*" * self.len_cte )                                     # [INFO] Print break lines

    self.reset_myPart()                                             # Go back to defaults
