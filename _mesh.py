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
import  os
import  numpy                       as      np
from    platform                    import  system                          # Running platform info
from    itertools                   import  product                         # Apply product rule on combinations
from    time                        import  sleep, time                     # Timers/delays

try:
    from    pexpect                 import  spawn                           # Call external programs (UNIX)
except:
    from    pexpect.popen_spawn     import  PopenSpawn as spawn             # Call external programs (Windows)

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def tetgen( self ):
    '''
    Create a MESH out of the STL file.

    INPUT:-
        - file_name: The name you'd like the MESH file
                     to be given.
    '''

    stl_filename            = self.stl_filename
    
    if( system()=='Linux' ):
        cmd = "{}tetgen -pq1.2 -g -F -C -V -N -G -I -a0.1 {}".format( self.tet, stl_filename )
    elif( system()=='Windows' ):
        print( self.tet )
        print( self.stl_filename )
        cmd = "{}tetgen.exe -pq1.2 -g -k -C -V -I -a0.1 {}".format( self.tet, stl_filename )
        print( cmd )
        
    child = spawn( cmd, timeout=None )                              # Spawn child
    
    for line in child:                                              # Read STDOUT ...
        out = line.decode('utf-8').strip('\r\n')                    # ... of spawned child ...
        print( out )                            # ... process and print.
    
    if( system()=='Linux' ): child.close()                          # Kill child process

# --------------------------
