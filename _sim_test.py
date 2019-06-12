from _febio     import *
from _mesh      import *
from _geometry  import * 


# this only needs to be done once, so we should push it to the setup... perhaps?
geo, febio_doc, febio_root = read_febio_file( 'dogbone.feb' )
nodes_id, nodes, nodeset = get_febio_data( geo )



#reader, vtk_nodes, vtk_nodes_array = read_vtk( 'dogbone_var1.vtk' )

#nodeset_nodes = node_coord_match( geo, nodes_array )

