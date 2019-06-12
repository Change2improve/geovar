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

def node_coord_match( geo, nodes_array ):
    '''
    MATCHES CORRESPONDING NODES ON THE BASIS OF COORDINATE EXACT SIMILARITIES
    '''

    geo_len = len(geo)


    # unpack nodes ----------------------------------------------------- #
    # nodes come from "node_array"
    
    
    
    for i in range( 0, 3 ):

        if geo[i].tag == 'NodeSet':

            nodeset = geo[i]
            nodeset_type    = nodeset.attrib['name']
            print( nodeset_type )

            nodeset_len = len(nodeset)
            print(nodeset_len)

            # pull ids from nodeset ------------------------------------- #
            nodeset_id          = []
            nodeset_nodes       = []

            nodes_coord_sum     = np.zeros((3))
            nodes_coord_avg     = []
            
            for j in range( 0, nodeset_len ):
                nodeset_id.append(      int(nodeset[j].attrib['id'])    )
                nodeset_nodes.append(   nodes_array[nodeset_id[j] - 1]  )

                nodes_coord_sum = nodes_coord_sum + nodes_array[nodeset_id[j] - 1]

            print( nodeset_id )
            print( nodeset_nodes )
            print( nodes_coord_sum )

                

    '''
    for i in range( 0, nodeset_len ):
        
    # using the attributes
    nodeset_type    = nodeset.attrib['name']
    nodeset_len     = len(nodeset)

    if nodeset_type[:-2] == 'FixedDisplacement': # ----------------------------------------------------------- #
        label_str = 'fixdisp{}'.format(nodeset_type[len(nodeset_type)-2:])
        fdata['baseline']['geo']['nodeset'][label_str]          = {}
        fdata['baseline']['geo']['nodeset'][label_str]['id']    = []
        for j in range( 0, nodeset_len ):
            fdata['baseline']['geo']['nodeset'][label_str]['id'].append( nodeset[j].attrib['id'] )

    if nodeset_type[:-2] == 'PrescribedDisplacement': # ------------------------------------------------------ #
        label_str = 'presdisp{}'.format(nodeset_type[len(nodeset_type)-2:])
        fdata['baseline']['geo']['nodeset'][label_str]          = {}
        fdata['baseline']['geo']['nodeset'][label_str]['id']    = []
        for j in range( 0, nodeset_len ):
            fdata['baseline']['geo']['nodeset'][label_str]['id'].append( nodeset[j].attrib['id'] )

    elif nodeset_type[:-2] != 'FixedDisplacement' and nodeset_type[:-2] != 'PrescribedDisplacement':
        message = "The current version of GEOVAR does not support FEBio's NoseSet:Type {}".format( nodeset_type )
        print( message )

    return fdata
    '''
    return nodeset_nodes

# --------------------------

