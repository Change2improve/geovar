
from    lxml                        import  etree

file = "C:\\Users\\WOLF512\\Documents\\Gits\\PD3D\\geovar\\input\\dogbone.feb"

_doc = etree.parse( file )
root = _doc.getroot()

# find the geometry 'child' although this should not change... but perhaps in the future
root_len = len(root)
print( root_len )
for i in range( 0, root_len ):
    if root[i].tag == 'Geometry':
        geo_index = i

print(geo_index) # validation


# extracting parts from the geometry section
geo_ele = root[geo_index]
geo_len = len( geo_ele )
print( geo_len )

nodes = []
elements = []

for i in range( 0, geo_len ):

    if geo_ele[i].tag == 'Nodes':

        nodes_ele = geo_ele[i]
        nodes_len = len( nodes_ele )

        for j in range( 0, nodes_len ):
            
            instring = "{},{}".format( int(nodes_ele[j].attrib['id']),
                                       nodes_ele[j].text )
            nodes.append( instring.split(',') )

backup = nodes_ele[0].text
nodes_ele[0].text = " -1, -1, -1"
_doc.write('dogbone_mod.xml')
