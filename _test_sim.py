
import  numpy                       as      np
from    lxml                        import  etree
from    _febio                      import  *

file = 'dogbone.feb'

febio_doc, root, geo, geo_index, geo_len = read_febio_file( file )

fdata = get_febio_data( geo )



#backup = nodes[0].text
#nodes[0].text = " -1, -1, -1"
#febio_doc.write('dogbone_mod.xml')
