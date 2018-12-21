import  pymesh
from    stl                     import  mesh                as  meh
import  numpy                                               as  np
##from    mayavi                import  mlab                            # Data visualization
from    matplotlib              import  pyplot              as plt
from    mpl_toolkits.mplot3d    import  Axes3D
from    matplotlib.patches      import  FancyArrowPatch
from    mpl_toolkits.mplot3d    import  proj3d
# Define path
dd      = "/home/moe/Desktop/test_files/r_inner1.0__r_outer10.0__height100.1.mesh"
mesh    = pymesh.load_mesh( dd )                            # Load mesh

mesh.add_attribute("face_normal")                           # Compute normals
normals = mesh.get_attribute("face_normal")                 # Retrieve them

mesh.add_attribute("face_index")                            # Compute Indices
index = mesh.get_attribute("face_index")                    # Retrieve them

mesh.add_attribute("face_centroid")                         # Compute centroids
centroid = mesh.get_attribute("face_centroid")              # Retrieve them

mesh.add_attribute("vertex_normal")                         # Compute centroids
v_normal = mesh.get_attribute("vertex_normal")              # Retrieve them

mesh.add_attribute("vertex_index")                         # Compute centroids
v_index = mesh.get_attribute("vertex_index")              # Retrieve them

normals     = normals.reshape(len(index), 3)                # Reshape into triplets
centroid    = centroid.reshape(len(index), 3)               # Reshape into triplets
v_normal    = v_normal.reshape(len(v_index), 3)

SCALE_FACTOR    = 1
normals         = normals[::SCALE_FACTOR]
centroid        = centroid[::SCALE_FACTOR]
rigid_boundary  = np.array( np.where(normals==(0, 0, -1)) ).T
bound           = rigid_boundary[:,0]
return_val      = rigid_boundary[:,1]
index = list()
for i in range( 0, rigid_boundary.shape[0], 3 ):
    if( return_val[i] == 0 and return_val[i+1] == 1 and return_val[i+2] == 2 ):
        index.append( i )

bound = np.zeros( len(index) )
for i in range( 0, len(index) ):
    bound[i] = index[i]
        
##rigid_boundary  = rigid_boundary[:,0][::3]                  # Extract indices
##
### Make the grid plane
##x = centroid[:,0]; xx = np.copy( x )
##y = centroid[:,1]; yy = np.copy( y )
##z = centroid[:,2]; zz = np.copy( z )
##
### Make the direction data for the arrows
##u = normals[:,0]; uu = np.copy( u )
##v = normals[:,1]; vv = np.copy( v )
##w = normals[:,2]; ww = np.copy( w )
##
##x, y, z = np.zeros_like(rigid_boundary), np.zeros_like(rigid_boundary), np.zeros_like(rigid_boundary)
##u, v, w = np.zeros_like(rigid_boundary), np.zeros_like(rigid_boundary), np.zeros_like(rigid_boundary)
##i = 0
##for ndx in rigid_boundary:
##    x[i], y[i], z[i] = xx[ndx], yy[ndx], zz[ndx]
##    u[i], v[i], w[i] = uu[ndx], vv[ndx], ww[ndx]
##    i += 1
##
##fig = plt.figure()
##ax = fig.gca(projection='3d')
##
####ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
##ax.plot(x, y, z, 'o', markersize=10, color='g', alpha=0.2)
##plt.show()
