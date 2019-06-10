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
    IMPORT STL MESH
    '''

    stl_file                                = self.stl_filename
    stl_mesh                                = mesh.Mesh.from_file( stl_file )

    r                                       = self.r
    variant_iter                            = self.variant_iter
    r[str(variant_iter)]['stl']             = {}
    r[str(variant_iter)]['stl']['mesh']     = stl_mesh
    
    self.stl_mesh                           = stl_mesh
    self.r                                  = r

# --------------------------

def read_stl( self ):
    '''
    EXTRACT DATA FROM STL MESH
    '''

    r                                       = self.r
    r_iter                                  = self.variant_iter
    stl_mesh                                = self.stl_mesh
    Ntris                                   = len( stl_mesh.points )
    Nnodes                                  = 3                                                     # 3 nodes per triangle

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

    r[str(r_iter)]['stl']['data']           = {}
    r[str(r_iter)]['stl']['data']['x']      = x
    r[str(r_iter)]['stl']['data']['y']      = y
    r[str(r_iter)]['stl']['data']['z']      = z
    r[str(r_iter)]['stl']['data']['u']      = u
    r[str(r_iter)]['stl']['data']['v']      = v
    r[str(r_iter)]['stl']['data']['w']      = w
    

# --------------------------

def vis_stl( self, intensity, plot, export ):
    '''
    VISUALIZE STL MESH
    '''

    r               = self.r
    configs         = self.configs
    r_iter          = self.variant_iter
    stl_filename    = self.stl_filename
    Nconfigs        = configs[str(r_iter)]['Nconfigs']
    #units           = self.configs[str(variant_iter)]['units']
    # here we can make a section that deals with the units... in the dogbone example, variables are unitless...

    
    x               = r[str(r_iter)]['stl']['data']['x']
    y               = r[str(r_iter)]['stl']['data']['y']
    z               = r[str(r_iter)]['stl']['data']['z']
    u               = r[str(r_iter)]['stl']['data']['u']
    v               = r[str(r_iter)]['stl']['data']['v']
    w               = r[str(r_iter)]['stl']['data']['w']

    
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
            showscale=True,
            colorbar = {
                "title" : colorbar_title,
                "xpad" : 10,
                "ypad" : 10,
                },
            colorscale = 'Viridis',
            opacity = 1, 
            intensity = intensity_axis,
            i = u,
            j = v,
            k = w,
        )
    ]

    title = []
    for i in range(0, Nconfigs):
        title.append( ' {} = {} {}'.format( r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['parameterId'],
                                            r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['defaultValue'],
                                            r[str(r_iter)]['decoded']['configurationParameters'][i]['message']['rangeAndDefault']['message']['units'] ))

    title = ','.join(title)
        
    layout = go.Layout(
        title=title,
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
    if plot == 1:
        plotly.offline.plot(fig)

    if export == 1:
        pio.write_image(fig, '{}.svg'.format( stl_filename[:-4] ))
        pio.write_image(fig, '{}.png'.format( stl_filename[:-4] ), width=2048, height=1024)


