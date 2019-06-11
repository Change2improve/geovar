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

# additional python modules and libraries
import  re
import  os
import  numpy                       as      np
from    platform                    import  system                          # Running platform info
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays

try:
    from    pexpect                 import  spawn                           # Call external programs (UNIX)
except:
    from    pexpect.popen_spawn     import  PopenSpawn as spawn             # Call external programs (Windows)

# onshape modules and libraries
from    onshapepy.play              import  *                               # Onshape API

# adapted onshape modules and libraries
from    _performance                import  *
import  _onshape


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def tetgen( self, verbose ):
    '''
    GENERATE TETGEN MESH FROM STL FILE
    '''

    print('[{:0.6f}] Generate TetGen mesh'.format(current_time( self )))
    
    stl_filename            = self.stl_filename
    tetgen_dir              = self.tetgen_dir
    
    if( system()=='Linux' ):
        print( " ERROR: geovar() has only been configured for Windows... ")
        #cmd = "{}tetgen -pq1.2 -g -F -C -V -N -G -I -a0.1 {}".format( self.tet, stl_filename )
        quit()

    elif( system()=='Windows' ):
        cmd = '{}tetgen.exe -pq1.2 -g -k -C -V -I -a0.1 "{}"'.format( tetgen_dir, stl_filename )
        
    child = spawn( cmd, timeout = None )                                                            # Spawn child


    if verbose == 1:
        print('[{:0.6f}] Mesh result and statistics'.format(current_time( self )))
        for line in child:                                                                          # Read STDOUT ...
            out = line.decode('utf-8').strip('\r\n')                                                # ... of spawned child ...
            print( out )                                                                            # ... process and print.
    
    if( system()=='Linux' ): child.close()                                                          # Kill child process

# --------------------------
