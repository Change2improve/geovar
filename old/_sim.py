'''
*
* _sim
* GEOVAR SIMULATION MODULE
*
* Module designed to delegate "simulation-specific" functions or operations
*
* VERSION: 0.0.1
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   May 26th, 2019 Year of Our Lord
*
'''


from    lxml                        import  etree

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def read_FEBio_file( self, febio_filename ):
    '''
    Generate FEBio file of the meshed geometric variant for simulation
        - The program uses a default PreView (FEBio's pre-processor) as reference
    '''

    print( '\n' )
    print( "READ DOC INFO..." )
    file = self.input + febio_filename

    _doc = etree.parse( file )
    _doc_geometry = _doc.find('geometry')
    
    
    

# --------------------------
