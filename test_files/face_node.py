'''
*
* Determine and extract exterior faces/nodes
*
* VERSION: 1.1
*   - ADDED   : Initial release
*   - ADDED   : Ability to extract all or exterior faces
*
* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Dec. 21st, 2018 Year of Our Lord
* LAST CONTRIBUTION DATE    :   Jan.  3rd, 2019 Year of Our Lord
*
'''

import  numpy                       as      np
from    argparse                    import  ArgumentParser              # Add input arguments to script
from    datetime                    import  datetime                    # Get date and time
from    matplotlib                  import  pyplot              as plt  # Plot stuff
from    mpl_toolkits.mplot3d        import  proj3d

# ************************************************************************
# =====================> CONSTRUCT ARGUMENT PARSER <=====================*
# ************************************************************************

ap = ArgumentParser()

# Extract all faces from .faces/.node files
string = "Extract ALL faces"
ap.add_argument( "--all-faces"          ,
                 dest   = "all_faces"   ,
                 action = 'store_true'  , default=False ,
                 help   = "{}".format(string)           )

args = ap.parse_args()

args.all_faces = True
# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

# Define path
node_file   = "/home/moe/Desktop/test_files/r_inner1.0__r_outer10.0__height100.1.node"
face_file   = "/home/moe/Desktop/test_files/r_inner1.0__r_outer10.0__height100.1.face"

try:
    print( "Loading files into buffer...", end='' )
    node_buff   = open( node_file, 'r', 1 )             # Store files in buffer
    face_buff   = open( face_file, 'r', 1 )             # ...

    node_offset = []                                    # Lists for offsets
    face_offset = []                                    # ...

    offset = 0                                          # Build list of line offsets here
    for line in node_buff:                              # ...
        node_offset.append( offset )                    # ...
        offset += len( line )                           # ...
    node_buff.seek( 0 )                                 # ...

    offset = 0                                          # Same here
    for line in face_buff:                              # ...
        face_offset.append( offset )                    # ...
        offset += len( line )                           # ...
    face_buff.seek( 0 )                                 # ...
    print( "...Done!" )

    print( "{} face(s) found.".format(len(face_offset)-2) )
    print( "Computing centroids." )

    ''' Read lines from .face and cross-reference corresponding nodes'''
    # Now, to skip to line n (with the first line being line 0)
    # use: node_buff.seek(node_offset[n])
    NROWS, NCOLS    = 1, 3                              # Rows and columns in each entry
    node_1          = np.zeros( (NROWS,NCOLS) )         # Construct empty arrays for nodes
    node_2          = np.zeros( (NROWS,NCOLS) )         # ...
    node_3          = np.zeros( (NROWS,NCOLS) )         # ...
    face_centroid   = list()                            # Dynamically populating lists in Python is faster

    face_buff.seek(face_offset[1]); i=0                 # Roll to first entry and start counter

    date = datetime.now().strftime("%Y-%m-%d__%H_%M_%S")# Get date
    with open( 'array.csv', 'w' ) as f:                 # Truncate file
        f.write( "# {}\n".format(date) )                #   Write header
        f.write( "# 'Ello mate\n" )                     #   ...

    for line in face_buff:                              # Loop over all lines in .face file
        string = line.split()                           #   Split lines on white-space

        ''' DETERMINE CONDITION TO SATISFY '''
        if( args.all_faces ):
            if( string[0] == '#' ):
                write_to_array  = False
            else: write_to_array = True
        else:
            if( string[0] == '#' or string[4] == '0' ):
                write_to_array  = False
            else: write_to_array = True

        ''' COMPUTE CENTROID AND WRITE TO ARRAY '''   
        if( write_to_array ):
            node_buff.seek( node_offset[int(string[1])] ); node_1 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )
            node_buff.seek( node_offset[int(string[2])] ); node_2 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )
            node_buff.seek( node_offset[int(string[3])] ); node_3 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )

            face_centroid.append( (node_1 + node_2 + node_3) / 3.0 ); i += 1
            with open( 'array.csv', 'a' ) as f:
                f.write( "{},{},{}\n".format(face_centroid[-1][0], face_centroid[-1][1], face_centroid[-1][2]) )

            ''' COUNTER FOR SHITS & GIGS '''
            if( args.all_faces ):
                if  ( i == round( (len(face_offset)-2)*0.10 ) ): print( "10% done" )
                elif( i == round( (len(face_offset)-2)*0.20 ) ): print( "20% done" )
                elif( i == round( (len(face_offset)-2)*0.30 ) ): print( "30% done" )
                elif( i == round( (len(face_offset)-2)*0.40 ) ): print( "40% done" )
                elif( i == round( (len(face_offset)-2)*0.50 ) ): print( "50% done" )
                elif( i == round( (len(face_offset)-2)*0.60 ) ): print( "60% done" )
                elif( i == round( (len(face_offset)-2)*0.70 ) ): print( "70% done" )
                elif( i == round( (len(face_offset)-2)*0.80 ) ): print( "80% done" )
                elif( i == round( (len(face_offset)-2)*0.90 ) ): print( "90% done" )
                elif( i == round( (len(face_offset)-2)*1.00 ) ): print( "100% done" )

    ''' CLOSE FILES '''
    node_buff.close()                                   # Close files
    face_buff.close()                                   # ...

    ''' PLOT '''
    face_centroid = np.array( face_centroid )
    x = face_centroid[:,0]
    y = face_centroid[:,1]
    z = face_centroid[:,2]
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ##ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
    ax.plot(x, y, z, 'o', markersize=10, color='g', alpha=0.2)
    plt.show()

except Exception as e:
    print( "Caught Error: {}".format(e) )
    node_buff.close()                                   # Close files
    face_buff.close()                                   # ...

