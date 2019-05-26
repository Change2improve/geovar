'''
import sys
bin_path = 'C:\\Program Files\\ParaView 5.6.0-Windows-msvc2015-64bit\\bin'
lib_path = 'C:\\Program Files\\ParaView 5.6.0-Windows-msvc2015-64bit\\bin\\Lib'
packages_path = 'C:\\Program Files\\ParaView 5.6.0-Windows-msvc2015-64bit\\bin\\Lib\\site-packages'
sys.path.insert(0, bin_path)
sys.path.insert(0, lib_path)
sys.path.insert(0, packages_path)

print( sys.path )
'''
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'STL Reader'
part_1_var1stl = STLReader(FileNames=['C:/Users/WOLF512/Documents/Gits/PD3D/geovar/output/2019-05-25__18_49_24/Part_1_var1.stl'])

# set active source
SetActiveSource(part_1_var1stl)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1344, 854]

# get color transfer function/color map for 'STLSolidLabeling'
sTLSolidLabelingLUT = GetColorTransferFunction('STLSolidLabeling')
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.878906683738906e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]
sTLSolidLabelingLUT.ScalarRangeInitialized = 1.0

# show data in view
part_1_var1stlDisplay = Show(part_1_var1stl, renderView1)
# trace defaults for the display properties.
part_1_var1stlDisplay.Representation = 'Surface'
part_1_var1stlDisplay.ColorArrayName = ['CELLS', 'STLSolidLabeling']
part_1_var1stlDisplay.LookupTable = sTLSolidLabelingLUT
part_1_var1stlDisplay.OSPRayScaleArray = 'STLSolidLabeling'
part_1_var1stlDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
part_1_var1stlDisplay.SelectOrientationVectors = 'None'
part_1_var1stlDisplay.ScaleFactor = 0.19685039520263672
part_1_var1stlDisplay.SelectScaleArray = 'STLSolidLabeling'
part_1_var1stlDisplay.GlyphType = 'Arrow'
part_1_var1stlDisplay.PolarAxes = 'PolarAxesRepresentation'
part_1_var1stlDisplay.GaussianRadius = 0.09842519760131836
part_1_var1stlDisplay.SetScaleArray = [None, '']
part_1_var1stlDisplay.ScaleTransferFunction = 'PiecewiseFunction'
part_1_var1stlDisplay.OpacityArray = [None, '']
part_1_var1stlDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# show color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera()

# change representation type
part_1_var1stlDisplay.SetRepresentationType('Surface With Edges')

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Opacity = 0.5

# hide color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, False)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(sTLSolidLabelingLUT, renderView1)

# set scalar coloring
ColorBy(part_1_var1stlDisplay, ('CELLS', 'STLSolidLabeling'))

# rescale color and/or opacity maps used to include current data range
part_1_var1stlDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, True)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(sTLSolidLabelingLUT, renderView1)

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Opacity = 1.0

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Opacity = 0.75

# change representation type
part_1_var1stlDisplay.SetRepresentationType('Surface')

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Specular = 0.03

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Opacity = 0.72

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Specular = 0.02

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Specular = 0.01

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.Specular = 0.0

# change representation type
part_1_var1stlDisplay.SetRepresentationType('Surface With Edges')

# set scalar coloring
ColorBy(part_1_var1stlDisplay, ('CELLS', 'STLSolidLabeling'))

# rescale color and/or opacity maps used to include current data range
part_1_var1stlDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, True)

# hide color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, False)

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.6847077360604514e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.6140907012492665e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.472856631626897e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.402238195517248e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.1550771723796365e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.907916149242025e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.6960636435100064e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.5548281725891725e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.413594102966803e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.378284184262746e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.272358632045969e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.2370501146403764e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.201741597234784e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.131123161125135e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.06050612631395e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 4.0251976089083576e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.989889091502765e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.954580574097173e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.919270655393116e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.8839621379875236e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.707418149661097e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.6368011148499123e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.60149259744432e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.354331574306709e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.177787585980282e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.036552115059448e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# Properties modified on sTLSolidLabelingLUT
sTLSolidLabelingLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.001243597653856e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]

# show color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, True)

# hide color bar/color legend
part_1_var1stlDisplay.SetScalarBarVisibility(renderView1, False)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('Blue to Red Rainbow', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('Linear Blue (8_31f)', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('Linear YGB 1211g', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('X Ray', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('Grayscale', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
sTLSolidLabelingLUT.ApplyPreset('Cool to Warm', True)

# Properties modified on part_1_var1stlDisplay
part_1_var1stlDisplay.EdgeColor = [0.3333333333333333, 1.0, 1.0]

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [2.720086198282631, -4.910269718094303, 4.430335126776654]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.984250009059906]
renderView1.CameraViewUp = [-0.26853424149904326, 0.4492518903145169, 0.8520927767510806]
renderView1.CameraParallelScale = 1.70477329428465

#### uncomment the following to render all views
RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
