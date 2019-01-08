'''
*
* Find edge boundaries by the examining normal vectors' direction
*
* VERSION: 1.1
*   - ADDED   : Initial release
*   - FIXED   : Sorta work how it is intended
*
* KNOWN ISSUES:
*   - In the test case of the cylinder, the top and
*     bottom lids are not detected.
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Dec. 21st, 2018 Year of Our Lord
* LAST CONTRIBUTION DATE    :   Jan.  4th, 2019 Year of Our Lord
*
'''

import  pymesh
import  numpy                                               as  np
from    matplotlib              import  pyplot              as plt
from    mpl_toolkits.mplot3d    import  Axes3D
from    matplotlib.patches      import  FancyArrowPatch
from    mpl_toolkits.mplot3d    import  proj3d

# Define path
dd      = "/home/moe/Desktop/test_files/r_inner9.5__r_outer10.0__height9.1.mesh"
mesh    = pymesh.load_mesh( dd )                                    # Load mesh

mesh.add_attribute("face_normal")                                   # Compute normals
normals = mesh.get_attribute("face_normal")                         # Retrieve them

mesh.add_attribute("face_index")                                    # Compute Indices
index = mesh.get_attribute("face_index")                            # Retrieve them

mesh.add_attribute("face_centroid")                                 # Compute centroids
centroid = mesh.get_attribute("face_centroid")                      # Retrieve them

normals     = normals.reshape(len(index), 3)                        # Reshape into triplets
centroid    = centroid.reshape(len(index), 3)                       # Reshape into triplets

SCALE_FACTOR    = 1                                                 # Number of steps to slice the array into
normals         = normals[::SCALE_FACTOR]                           # Slice the array (to reduce the number of points)
centroid        = centroid[::SCALE_FACTOR]                          # ...so things go faster

'''
NOTE:-
    np.where() returns the index of any element that satisfies
    any part of the condition specified. i.e:
    
    >>> a = np.array( ([0,1,5], [3,2,1], [0,0,-1]) )
    >>> a
    array([[ 0,  1,  5],
           [ 3,  2, -1],
           [ 0,  0, -1]])
           
    >>> rigid_boundary  = np.array( np.where(a==(0, 0, -1)) ).T
    >>> rigid_boundary
    array([[0, 0],
           [1, 2],
           [2, 0],
           [2, 1],
           [2, 2]])

    This is why we still do some more processing right after that
'''
rigid_boundary  = np.array( np.where(normals==(0, 0, -1)) ).T       # Search the normals for the condition (x, y, z)=(0, 0, -1)
bound           = rigid_boundary[:,0]                               # Extract the bound indices
return_val      = rigid_boundary[:,1]                               # Extract the 

# Find arrays where ALL elements satisfy the condition specified
index = list()
for i in range( 0, rigid_boundary.shape[0], 3 ):
    if( return_val[i] == 0 and return_val[i+1] == 1 and return_val[i+2] == 2 ):
        index.append( i )

bound = np.zeros( len(index) )
for i in range( 0, len(index) ):
    bound[i] = index[i]
        
rigid_boundary  = rigid_boundary[:,0][::3]                          # Extract indices

# Make the grid plane
x = centroid[:,0]; xx = np.copy( x )
y = centroid[:,1]; yy = np.copy( y )
z = centroid[:,2]; zz = np.copy( z )

# Make the direction data for the arrows
u = normals[:,0]; uu = np.copy( u )
v = normals[:,1]; vv = np.copy( v )
w = normals[:,2]; ww = np.copy( w )

x, y, z = list(), list(), list()
u, v, w = list(), list(), list()

# Now populate the x, y, z points and the u, v, w normal vectors
for ndx in rigid_boundary:
    x.append(xx[ndx]); y.append(yy[ndx]); z.append(zz[ndx])
    u.append(uu[ndx]); v.append(vv[ndx]); w.append(ww[ndx])

# Finally plot
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True, alpha=0.25)
ax.plot(x, y, z, 'o', markersize=10, color='g', alpha=0.75)
plt.show()

