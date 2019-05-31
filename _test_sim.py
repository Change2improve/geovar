
import  numpy                       as      np
from    lxml                        import  etree
from    _febio                      import  *

file = 'dogbone.feb'

febio_doc, root, geo, geo_index, geo_len = read_febio_file( file )



fdata                                           = {}
fdata['baseline']                               = {}
fdata['baseline']['geo']                        = {}
fdata['baseline']['geo']['nodes']               = {}
fdata['baseline']['geo']['nodes']['id']         = []
fdata['baseline']['geo']['nodes']['text']       = []
fdata['baseline']['geo']['elements']            = {}
fdata['baseline']['geo']['elements']['id']      = []
fdata['baseline']['geo']['elements']['text']    = []

for i in range( 0, geo_len ):

    if geo[i].tag == 'Nodes': # -------------------------------------------------------------------------- #

        nodes               = geo[i]
        nodes_len           = len( nodes )

        # initializing numpy arrays
        nodes_array         = np.zeros(( nodes_len, 3 ), dtype=float)
        
        for j in range( 0, nodes_len ):           

            # extracting raw data
            ## extracting nodes
            fdata['baseline']['geo']['nodes']['id'].append(         nodes[j].attrib['id'] )
            fdata['baseline']['geo']['nodes']['text'].append(       nodes[j].text )
            
            # tranform into numeric values for proper manipulation
            nodes_array[j]  = nodes[j].text.split(',')

    if geo[i].tag == 'Elements': # ----------------------------------------------------------------------- #

        elements            = geo[i]
        elements_len        = len( elements )
        print( elements_len )

        # initializing numpy arrays
        elements_array      = np.zeros(( elements_len, 4 ), dtype=int)
        
        for j in range( 0, elements_len ):           

            # extracting raw data
            ## extracting elements
            fdata['baseline']['geo']['elements']['id'].append(      elements[j].attrib['id'] )
            fdata['baseline']['geo']['elements']['text'].append(    elements[j].text )
            
            # tranform into numeric values for proper manipulation
            elements_array[j] = elements[j].text.split(',')


# update structure
fdata['baseline']['geo']['nodes']['array']          = nodes_array
fdata['baseline']['geo']['elements']['array']       = elements_array


backup = nodes[0].text
nodes[0].text = " -1, -1, -1"
febio_doc.write('dogbone_mod.xml')
