import vtk
from vtk.util.misc import vtkGetDataRoot
from vtk.util.colors import *
VTK_DATA_ROOT = vtkGetDataRoot()

sr = vtk.vtkSTLReader()
sr.SetFileName("C:/Users/WOLF512/Documents/Gits/PD3D/geovar/output/2019-05-26__17_29_33/Part_1_var1.stl")

stlMapper = vtk.vtkPolyDataMapper()
stlMapper.SetInputConnection(sr.GetOutputPort())

stlActor = vtk.vtkLODActor()
stlActor.SetMapper(stlMapper)
stlActor.RotateX(45.0)
stlActor.RotateY(45.0)
stlActor.RotateZ(45.0)

stlActor.GetProperty().SetColor(light_grey)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the render; set the background and size
ren.AddActor(stlActor)
ren.SetBackground(0.1, 0.6, 0.4)
renWin.SetSize(500, 500)
 
# Zoom in closer
ren.ResetCamera()
cam1 = ren.GetActiveCamera()
cam1.Zoom(1.4)
 
#iren.Initialize()
renWin.Render()

# screenshot section
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()

writer = vtk.vtkPNGWriter()
writer.SetFileName("screenshot.png")
writer.SetInputDataObject(w2if.GetOutput())
writer.Write()


#iren.Start()