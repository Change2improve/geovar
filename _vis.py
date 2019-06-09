'''
*
* _vis
* GEOVAR VISUALIZATION MODULE
*
* Module designed to delegate "visualization-specific" functions or operations
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   Jun. 1st, 2019
*
'''

import  os
import  numpy                       as      np
import  plotly
import  plotly.graph_objs           as      go
import  plotly.io                   as      pio
from    stl                         import  mesh
from    plotly.offline              import  *


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def import_stl( self ):
    '''
    Import STL mesh file
        - This function will be moved to the geometry module latyer
    '''

    stl_file                                = self.stl_filename
    stl_mesh                                = mesh.Mesh.from_file( stl_file )

    g                                       = self.g
    variant_iter                            = self.variant_iter
    g[str(variant_iter)]                    = {}
    g[str(variant_iter)]['stl']             = {}
    g[str(variant_iter)]['stl']['mesh']     = stl_mesh
    
    self.stl_mesh                           = stl_mesh
    self.g                                  = g

# --------------------------

def read_stl( self ):
    '''
    Extract STL mesh data
        - This function will be moved to the geometry module latyer
    '''

    g               = self.g
    variant_iter    = self.variant_iter
    stl_mesh        = self.stl_mesh
    Ntris           = len( stl_mesh.points )
    Nnodes          = 3                                                     # 3 nodes per triangle

    x = []
    y = []
    z = []
    u = []
    v = []
    w = []

    # this section reads data specifically from an .stl mesh
    for i in range( 0, Ntris ):
        for j in range( 0, Nnodes ):
            x.append( stl_mesh.x[i][j] )
            y.append( stl_mesh.y[i][j] )
            z.append( stl_mesh.z[i][j] )
        u.append( Nnodes*i + 0 )
        v.append( Nnodes*i + 1 )
        w.append( Nnodes*i + 2 )

    g[str(variant_iter)]['stl']['data']         = {}
    g[str(variant_iter)]['stl']['data']['x']    = x
    g[str(variant_iter)]['stl']['data']['y']    = y
    g[str(variant_iter)]['stl']['data']['z']    = z
    g[str(variant_iter)]['stl']['data']['u']    = u
    g[str(variant_iter)]['stl']['data']['v']    = v
    g[str(variant_iter)]['stl']['data']['w']    = w
    

# --------------------------

def vis_stl( self, intensity, export ):

    g               = self.g
    variant_iter    = self.variant_iter
    stl_filename    = self.stl_filename
    units           = self.configs[variant_iter]['units']

    print( units )
    
    x               = g[str(variant_iter)]['stl']['data']['x']
    y               = g[str(variant_iter)]['stl']['data']['y']
    z               = g[str(variant_iter)]['stl']['data']['z']
    u               = g[str(variant_iter)]['stl']['data']['u']
    v               = g[str(variant_iter)]['stl']['data']['v']
    w               = g[str(variant_iter)]['stl']['data']['w']

    
    if intensity == 0:
        intensity_axis = x
        colorbar_title = "x"
    elif intensity == 1:
        intensity_axis = y
        colorbar_title = "y"
    elif intensity == 2:
        intensity_axis = z
        colorbar_title = "z"

    
    data = [
        go.Mesh3d(
            x = x,
            y = y,
            z = z,
            alphahull=5,
            colorbar = {
                "title" : colorbar_title
                },
            colorscale = 'Viridis',
            opacity = 1, 
            intensity = intensity_axis,
            i = u,
            j = v,
            k = w,
        )
    ]
    layout = go.Layout(
        xaxis=go.layout.XAxis(
            title='x'
        ),
        yaxis=go.layout.YAxis(
            title='y'
        ),
        scene = dict(
            aspectmode='data',
            camera = dict(
                eye = dict(
                    x = 3.00,
                    y = 3.00,
                    z = 3.00
                )
            )
        )
    )

    # plotting
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)

    if export == 1:
        pio.write_image(fig, '{}.svg'.format( stl_filename[:-4] ))
        pio.write_image(fig, '{}.png'.format( stl_filename[:-4] ), width=1024, height=1024)


