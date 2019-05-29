
# import visualization modules
import numpy as np
from stl import mesh

import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.io as pio
'''
install orca using npm https://nodejs.org/en/
pip install psutil
'''
import os


# import mesh from file
mesh = mesh.Mesh.from_file('output/part1.stl')

# transform data to plotly array
Ntris = len(mesh.points)
Nnodes = 3 # 3 points per triangle

x = []
y = []
z = []
u = []
v = []
w = []
data = np.zeros((Ntris,3))

# this section reads data specifically from an .stl mesh
for i in range( 0, Ntris ):
    for j in range( 0, Nnodes ):
        x.append( mesh.x[i][j] )
        y.append( mesh.y[i][j] )
        z.append( mesh.z[i][j] )
    u.append( Nnodes*i + 0 )
    v.append( Nnodes*i + 1 )
    w.append( Nnodes*i + 2 )

# creating data structure for plotly
data = [
    go.Mesh3d(
        x = x,
        y = y,
        z = z,
        alphahull=5,
        colorbar = {
            "title" : "z"
            },
        #colorscale = 'Blues',
        colorscale = 'Viridis',
        opacity = 1,
        intensity = z,
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
    )
)

# plotting
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)

pio.write_image(fig, 'fig1.svg')

'''
https://plot.ly/python/reference/#mesh3d
https://plot.ly/python/static-image-export/
'''

