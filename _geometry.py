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
    #print(nodeset_len)

    match_axis = []
    match_mean = []
    match_sd   = []
    
    for i in range( 0, nodeset_len ):

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

        # determine smallest deviation
        nodes_sd_min = np.min( nodes_sd )
        #print( nodes_sd_min )

        # determine if smallest deviation meets tolerance
        tol = 1e-10 # --------------------------------------------------------------------> this value needs to be extracted, used as an input
        if np.abs(nodes_sd_min) < tol:
            # capturing index of smallest deviation
            # capturing the average value of the smallest deviation
            for i in range( 0, len(nodes_sd) ):
                if nodes_sd[i] == nodes_sd_min:
                    min_index = i
                    break
            nodes_mean_min = nodes_mean[min_index]

        # results
        match_axis.append(  min_index )
        match_mean.append(  nodes_mean_min )
        match_sd.append(    nodes_sd_min )

    print( match_axis, match_mean, match_sd )
            
# --------------------------

