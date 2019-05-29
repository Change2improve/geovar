
# import visualization modules
import numpy as np
from stl import mesh

import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.io as pio
'''
install orca using npm https://nodejs.org/en/
npm install orca
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
for i in range( 0, 100 ):
    for j in range( 0, Nnodes ):
        x.append( mesh.x[i][j] )
        y.append( mesh.y[i][j] )
        z.append( mesh.z[i][j] )
    u.append( Nnodes*i + 0 )
    v.append( Nnodes*i + 1 )
    w.append( Nnodes*i + 2 )

# creating data structure for plotly
trace0 = go.Mesh3d(
    x = x,
    y = y,
    z = z,
    alphahull=5,
    colorbar = {
        "title" : "z"
        },
    colorscale = 'Portland',
    intensity = z,
    i = u,
    j = v,
    k = w,
)

# need to make trace1 a dict() to trace over each triangle
# later, this will become a quad...
data = []
scatter_trace = {}

for i in range( 0, 100 ):
    x_trace = []
    y_trace = []
    z_trace = [] 
    for j in range( 0, (Nnodes+1) ):

        if j < Nnodes:
            #print(j)
            x_trace.append( x[Nnodes*i + j] )
            y_trace.append( y[Nnodes*i + j] )
            z_trace.append( z[Nnodes*i + j] )
            
        elif j == Nnodes:
            #print(j)
            x_trace.append( x_trace[0] )
            y_trace.append( y_trace[0] )
            z_trace.append( z_trace[0] )

    scatter_trace[str(i)] = go.Scatter3d(
        x=x_trace,
        y=y_trace,
        z=z_trace,
        marker=dict(
            size=2,
            color=z,
            symbol='circle',
            #color='rgb(127, 127, 127)',
            colorscale='Viridis',
        ),
        line=dict(
            color='#000000',
            width=1
        )
    )

    data.append( scatter_trace[str(i)] )

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

#pio.write_image(fig, 'fig1.svg')

'''
https://plot.ly/python/reference/#mesh3d
https://plot.ly/python/static-image-export/
'''

