import plotly
import plotly.graph_objs as go
from plotly.offline import *
import numpy as np

pts=np.loadtxt('mesh_dataset.txt')
x,y,z=zip(*pts)

trace = go.Mesh3d(x=x,y=y,z=z,color='#FFB6C1',opacity=0.50)
plotly.offline.plot([trace])
