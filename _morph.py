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
import  _onshape


# additional python modules and libraries
import  re
import  numpy                       as      np
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def simple_morph( self ):
    '''
    simple morph
    '''

    self.prog_time          = time() - self.prog_start_time
    print( "[{:0.6f}] Morphing Onshape doc. based on var. product".format(self.prog_time) )
    
    variant_iter            = self.variant_iter
    var                     = self.var
    arr                     = self.arr
    prods                   = self.prods
    Nprods                  = len(prods)
    Nvars                   = var['nvar']
    updates                 = []
    
    for i in range(0, Nvars):
        updates.append( arr[i][prods[variant_iter][i]] )

    _onshape.update_configurations( self, updates )
    # check if morph completed successfully...

    self.variant_iter       = variant_iter + 1                              # Update iteration counter

# --------------------------
