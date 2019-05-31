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
    Read FEBio file
    '''

    print( '\n' )
    print( "READ FEBio INFO..." )
    #file = self.input + febio_filename
    file = febio_filename

    febio_doc       = etree.parse( file )
    febio_root      = febio_doc.getroot()

    root_len = len(febio_root)
    print( root_len )
    for i in range( 0, root_len ):
        if febio_root[i].tag == 'Geometry':
            geo_index = i


    # extracting parts from the geometry section
    geo = febio_root[geo_index]
    geo_len = len( geo )
    

    return febio_doc, febio_root, geo, geo_index, geo_len
    #self.febio_doc  = febio_doc
    #self.febio_root = febio_root
    

# --------------------------


def map_febio_components( febio_filename ):
    '''
    Read FEBio file
    '''

    print( '\n' )
    print( "READ FEBio INFO..." )
    #file = self.input + febio_filename
    file = febio_filename

    febio_doc       = etree.parse( file )
    febio_root      = febio_doc.getroot()

    return febio_doc, febio_root
    #self.febio_doc  = febio_doc
    #self.febio_root = febio_root
    

# --------------------------
