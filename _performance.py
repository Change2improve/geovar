'''
*
* _performance
* GEOVAR PERFORMANCE SUPPORT MODULE
*
* Module designed to delegate "performance" functions that serve the GEOVAR class
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   June 9th, 2019
*
'''

# Python Libraries and Modules
from    time                        import  sleep, time                 # Timers/delays

# Geovar Libraries and Modules
# ...

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def current_time( self ):
    '''
    Measures time from start of the program
    '''
    current_time        = time() - self.prog_start_time

    self.current_time   = current_time

    return current_time
