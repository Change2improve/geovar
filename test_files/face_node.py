import  numpy                                               as  np

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

    print( "{} face found.".format(len(face_offset)-2) )
    print( "Computing centroids." )

    ''' Read lines from .face and cross-reference corresponding nodes'''
##    # Now, to skip to line n (with the first line being line 0), just do
##    node_buff.seek(node_offset[n])
    NROWS, NCOLS    = 1, 3
    node_1          = np.zeros( (NROWS,NCOLS) )
    node_2          = np.zeros( (NROWS,NCOLS) )
    node_3          = np.zeros( (NROWS,NCOLS) )
    face_centroid   = np.zeros( (len(face_offset)-2,NCOLS) )

    face_buff.seek(face_offset[1]); i=0                 # Roll to first entry and start counter
                                
    for line in face_buff:
        string = line.split()
        if( string[0] == '#' ): continue
        node_buff.seek( node_offset[int(string[1])] ); node_1 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )
        node_buff.seek( node_offset[int(string[2])] ); node_2 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )
        node_buff.seek( node_offset[int(string[3])] ); node_3 = np.array( (node_buff.readline()).split()[1:], dtype=np.float64 )

        face_centroid[i] = (node_1 + node_2 + node_3) / 3.0; i += 1
        
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
    
    node_buff.close()                                   # Close files
    face_buff.close()                                   # ...

except Exception as e:
    print( e )
    node_buff.close()                                   # Close files
    face_buff.close()                                   # ...
