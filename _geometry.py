'''
*
* _geometry
* GEOVAR GEOMETRY MODULE
*
* Module designed to delegate "geometry-specific" functions or operations
* Geometries may include .STLs, .VTKs, etc.
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   May 31st, 2019
*
'''

import  numpy                       as      np
import  vtk
from    lxml                        import  etree
from    vtk.util.numpy_support      import  vtk_to_numpy



# ************************************************************************
# FUNCTIONS ============================================================ *
# ************************************************************************

def read_vtk( filename ):

    # load a vtk file as input
    reader              = vtk.vtkUnstructuredGridReader()
    reader.SetFileName("dogbone_var1.vtk")
    reader.Update()

    # Get the coordinates of nodes in the mesh
    vtk_nodes           = reader.GetOutput().GetPoints().GetData()
    vtk_nodes_array     = vtk_to_numpy( vtk_nodes )

    return reader, vtk_nodes, vtk_nodes_array

# --------------------------

