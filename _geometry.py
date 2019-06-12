'''
*
* _match
* GEOVAR MATCH MODULE
*
* Module designed to match corresponding nodes, elements, faces, across
* geomatric variants
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   June 12th, 2019
*
'''
import numpy as np

# ************************************************************************
# FUNCTIONS ============================================================ *
# ************************************************************************

def node_coord_match( nodeset ):
    '''
    MATCHES CORRESPONDING NODES ON THE BASIS OF COORDINATE EXACT SIMILARITIES
    '''

    nodeset_len = len(nodeset)
    print(nodeset_len)

    for i in range( 0, 1 ):

        print(' Working on {} '.format( nodeset[str(i)]['type'] ) )

        # determine by average
        nodeset_nodes   = nodeset[str(i)]['nodes']
        nodes_len       = len(nodeset_nodes)

        nodes_sum       = np.zeros((3))
        nodes_mean      = np.zeros((3))
        nodes_sd        = np.zeros((3))
        for j in range( 0, nodes_len ):
            nodes_sum = nodes_sum + nodeset_nodes[j]

        nodes_mean = nodes_sum / nodes_len

        for j in range( 0, nodes_len ):
            nodes_sd = nodes_sd + ( nodeset_nodes[j] - nodes_mean )**2

        nodes_sd = np.sqrt( nodes_sd / nodes_len )
        

    print( nodes_sum, nodes_mean, nodes_sd )
            
# --------------------------

