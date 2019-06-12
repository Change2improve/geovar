'''
*
* _febio
* GEOVAR FEBio MODULE
*
* Module designed to delegate "febio-specific" functions or operations
* Most of these functions deal with reading/writing/operating/executing FEBio config files
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   May 31st, 2019
*
'''

import  numpy                       as      np
from    lxml                        import  etree

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def read_febio_file( febio_filename ):
    '''
    READ FEBio FILE
    '''

    #print( '\n' )
    #print( "READ FEBio INFO..." )
    #file = self.input + febio_filename
    file = febio_filename
    #print(file)

    febio_doc       = etree.parse( file )
    febio_root      = febio_doc.getroot()

    root_len = len(febio_root)
    #print( root_len )
    for i in range( 0, root_len ):
        if febio_root[i].tag == 'Geometry':
            geo_index = i


    # extracting parts from the geometry section
    geo = febio_root[geo_index]
    geo_len = len( geo )
    

    #return febio_doc, febio_root, geo, geo_index, geo_len
    #self.febio_doc  = febio_doc
    #self.febio_root = febio_root

    return geo, febio_doc, febio_root

# ------------------------------------------------------------------------------------------------------------ #

def write_febio_file( febio_filename ):
    '''
    WRITE FEBio FILE
    '''

    

# ------------------------------------------------------------------------------------------------------------ #

def get_febio_data( geo ):
    '''
    EXTRACT FEBio FILE DATA
    '''

    #print( '\n' )
    #print( "EXTRACT FEBio INFO..." )

    # the inputs of this program should be the XML components of interest (e.g.: Geometry)
    geo_len = len(geo)
    nodeset = {}
##    fdata                                           = {}
##    fdata['baseline']                               = {}
##    fdata['baseline']['geo']                        = {}
##    fdata['baseline']['geo']['nodes']               = {}
##    fdata['baseline']['geo']['nodes']['id']         = []
##    fdata['baseline']['geo']['nodes']['text']       = []
##    fdata['baseline']['geo']['elements']            = {}
##    fdata['baseline']['geo']['elements']['id']      = []
##    fdata['baseline']['geo']['elements']['text']    = []
##    fdata['baseline']['geo']['nodeset']             = {}

    for i in range( 0, geo_len ):

        #print( i )
        #print( geo[i].tag )

        if geo[i].tag == 'Nodes': # -------------------------------------------------------------------------- #
            #print( "> Gathering Nodes..." )
            nodes_id, nodes      = get_nodes(        geo, i )

        if geo[i].tag == 'Elements': # ----------------------------------------------------------------------- #
            #print( "> Gathering Elements..." )
            elements_id, elements   = get_elements(     geo, i)
            
        if geo[i].tag == 'NodeSet': # ------------------------------------------------------------------------ #
            #print( "> Gathering NodeSet(s)..." )
            nodeset = get_nodeset(      geo, i, nodes, nodeset )
                    

    # update structure
    #fdata['baseline']['geo']['nodes']['array']          = nodes_array
    #fdata['baseline']['geo']['elements']['array']       = elements_array
    
    return nodes_id, nodes, nodeset 

# ------------------------------------------------------------------------------------------------------------ #

def get_nodes( geo, index ):
    '''
    GET NODE DATA
    '''
    nodes_obj           = geo[index]
    nodes_len           = len( nodes_obj )

    # initializing numpy arrays
    nodes_id            = []
    nodes               = np.zeros(( nodes_len, 3 ), dtype=float)
    
    for j in range( 0, nodes_len ):           

        # extracting raw data
        ## extracting nodes
        #fdata['baseline']['geo']['nodes']['id'].append(         nodes[j].attrib['id'] )
        #fdata['baseline']['geo']['nodes']['text'].append(       nodes[j].text )
        
        # tranform into numeric values for proper manipulation
        nodes_id.append(int(nodes_obj[j].attrib['id']))
        nodes[j]  = nodes_obj[j].text.split(',')

    return nodes_id, nodes

# ------------------------------------------------------------------------------------------------------------ #

def get_elements( geo, index):
    '''
    GET ELEMENT DATA
    '''
    elements_obj            = geo[index]
    elements_len        = len( elements_obj )

    # using attributes to ensure proper extraction
    # this will be implemented now and should be standard in the future
    if elements_obj.attrib['type'] == 'tet4':
        #print( ">> The mesh uses tets of 4 nodes" )
        nodes_per_tet = 4

    # initializing numpy arrays
    elements_id         = []
    elements      = np.zeros(( elements_len, nodes_per_tet ), dtype=int)
    
    for j in range( 0, elements_len ):           

        # extracting raw data
        ## extracting elements
        #fdata['baseline']['geo']['elements']['id'].append(      elements[j].attrib['id'] )
        #fdata['baseline']['geo']['elements']['text'].append(    elements[j].text )
        
        # tranform into numeric values for proper manipulation
        elements_id.append(int(elements_obj[j].attrib['id']))
        elements[j] = elements_obj[j].text.split(',')

    return elements_id, elements

# ------------------------------------------------------------------------------------------------------------ #

def get_nodeset( geo, index, nodes, nodeset ):
    '''
    GET NODESET DATA
    '''
    nodeset_obj = geo[index]
    nodeset_len = len(nodeset_obj)

    # using the attributes
    nodeset_type = nodeset_obj.attrib['name']
    nodeset_len = len(nodeset_obj)

    # nodeset index
    nodeset_index = len(nodeset)
    nodeset[str(nodeset_index)] = {}
    if nodeset_type[:-2] == 'FixedDisplacement': # ----------------------------------------------------------- #
        nodeset[str(nodeset_index)]['type']     = 'fixdisp{}'.format(nodeset_type[len(nodeset_type)-2:])

    if nodeset_type[:-2] == 'PrescribedDisplacement': # ------------------------------------------------------ #
        nodeset[str(nodeset_index)]['type']     = 'presdisp{}'.format(nodeset_type[len(nodeset_type)-2:])
        
    elif nodeset_type[:-2] != 'FixedDisplacement' and nodeset_type[:-2] != 'PrescribedDisplacement':
        print('The current version of GEOVAR does not support FEBios NoseSet:Type {}'.format( nodeset_type ))

    nodeset[str(nodeset_index)]['id']    = []
    nodeset[str(nodeset_index)]['nodes'] = []
    for j in range( 0, nodeset_len ):
        nodeset[str(nodeset_index)]['id'].append( nodeset_obj[j].attrib['id'] )
        nodeset[str(nodeset_index)]['nodes'].append( nodes[ int(nodeset_obj[j].attrib['id'])-1] )

    return nodeset

# ------------------------------------------------------------------------------------------------------------ #

def nodeset_match( nodeset ):
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
