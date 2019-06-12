'''
*
* _mesh
* GEOVAR MESH MODULE
*
* Module designed to delegate "mesh-specific" functions or operations
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   Jun. 12th, 2019
*
'''

# Python Libraries and Modules
import  numpy                       as      np
import  vtk
from    vtk.util.numpy_support      import  vtk_to_numpy
from    platform                    import  system                                                  # Running platform info
try:
    from    pexpect                 import  spawn                                                   # Call external programs (UNIX)
except:
    from    pexpect.popen_spawn     import  PopenSpawn as spawn                                     # Call external programs (Windows)

# Onshape Libraries and Modules
from    onshapepy.play              import  *                                                       # Onshape API

# Geovar Libraries and Modules
from    _performance                import  *
import  _onshape


# ***************************************************************************************************
# FUNCTIONS ======================================================================================= *
# ***************************************************************************************************

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

# ------------------------------------------------------------------------------------------------- #

def read_vtk( filename ):
    '''
    IMPORT/READ VTK MESH
    '''

    # load a vtk file as input
    reader              = vtk.vtkUnstructuredGridReader()
    reader.SetFileName("dogbone_var1.vtk")
    reader.Update()

    # Get the coordinates of nodes in the mesh
    vtk_nodes           = reader.GetOutput().GetPoints().GetData()
    vtk_nodes_array     = vtk_to_numpy( vtk_nodes )

    return reader, vtk_nodes, vtk_nodes_array




