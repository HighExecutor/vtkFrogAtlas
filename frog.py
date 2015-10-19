__author__ = 'Mishanya'

import vtk
import Tkinter as tk
from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor
import tkColorChooser

# Grass plane
# Texture
need_plane = False
if need_plane:
    texReader = vtk.vtkJPEGReader()
    texReader.SetFileName("./grass.jpg")
    atext = vtk.vtkTexture()
    atext.SetInputConnection(texReader.GetOutputPort())
    atext.InterpolateOn()
    #Plane
    plane = vtk.vtkPlaneSource()
    plane.SetResolution(0.01, 0.01)
    plane.SetOrigin(0, 0, 0)
    plane.SetPoint1(2000, 0, 0)
    plane.SetPoint2(0, 2000, 0)
    planeMapper = vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort())
    planeActor = vtk.vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetPosition(-1250, -750, -200)
    planeActor.SetTexture(atext)

# Frog
# Source
frogReader = vtk.vtkImageReader()
frogReader.SetDataByteOrderToLittleEndian()
frogReader.SetDataExtent(0, 499, 0, 469, 1, 136)
frogReader.SetDataSpacing(1, 1, 1.5)
frogReader.SetDataScalarTypeToUnsignedChar()
frogReader.SetFileDimensionality(2)
frogReader.SetFilePrefix("./WholeFrog/frog.")
frogReader.SetFilePattern("%s%03d.raw")
frogReader.Update()

# Frog density
frogDens = vtk.vtkPiecewiseFunction()
frogDens.AddPoint(0.0, 0.0)
frogDens.AddPoint(230.0, 0.002)

#Frog color
frogClr = vtk.vtkColorTransferFunction()
frogClr.AddRGBPoint(0.0, 0.1, 0.9, 0.1)
frogClr.AddRGBPoint(250.0, 0.96, 0.98, 0.98)

# Frog mapper
frogFunc = vtk.vtkVolumeRayCastCompositeFunction()
frogMapper = vtk.vtkVolumeRayCastMapper()
frogMapper.SetInputConnection(frogReader.GetOutputPort())
frogMapper.SetVolumeRayCastFunction(frogFunc)

# Frog property
frogVolProp = vtk.vtkVolumeProperty()
frogVolProp.SetColor(frogClr)
frogVolProp.SetScalarOpacity(frogDens)
frogVolProp.SetInterpolationTypeToLinear()
frogVolProp.ShadeOn()

#Frog actor
frog = vtk.vtkVolume()
frog.SetMapper(frogMapper)
frog.SetProperty(frogVolProp)
frog.RotateY(180)


# Tissues
tissueReader = vtk.vtkImageReader()
tissueReader.SetDataByteOrderToLittleEndian()
tissueReader.SetDataExtent(0, 499, 0, 469, 1, 136)
tissueReader.SetDataSpacing(1, 1, 1.5)
tissueReader.SetDataScalarTypeToUnsignedChar()
tissueReader.SetFileDimensionality(2)
tissueReader.SetFilePrefix('./WholeFrog/frogTissue.')
tissueReader.SetFilePattern("%s%03d.raw")
tissueReader.Update()

# Labels
indexes = [i for i in range(1, 16)]
tissues_labels = {1:'blood', 2:'brain', 3:'duodenum', 4:'eye retina', 5:'eye white', 6:'heart', 7:'ileum', 8:'kidney',
                  9:'large intestine', 10:'liver', 11:'lung', 12:'nerve', 13:'skeleton', 14:'spleen', 15:'stomach'}

# Initial colors
tissues_colors = {1:(1, 0, 0),
                  2:(1, 0.3, 0.5),
                  3:(0, 0.5, 1),
                  4:(0, 1, 0),
                  5:(1, 1, 1),
                  6:(0.9, 0.1, 0.1),
                  7:(0.3, 0.6, 0.8),
                  8:(0.4, 0.1, 0.9),
                  9:(0.1, 0.9, 0.4),
                  10:(0.6, 0.5, 0),
                  11:(0, 0.6, 0.9),
                  12:(0.9, 0.5, 0.2),
                  13:(0.8, 0.8, 0.8),
                  14:(1, 0.1, 1),
                  15:(0.4, 0.2, 0.7)}

# Init densities
tissueDens = vtk.vtkPiecewiseFunction()
tissueDens.AddPoint(0, 0.0)
for i in indexes:
    tissueDens.AddPoint(i, 0)

# Colors
tissueClr = vtk.vtkColorTransferFunction()
tissueClr.AddRGBPoint(0, 0.0, 0.0, 0.0)
for i in indexes:
    tissueClr.AddRGBPoint(i, tissues_colors[i][0], tissues_colors[i][1], tissues_colors[i][2])

# Opacity Gradient
tissueOpacityGrad = vtk.vtkPiecewiseFunction()
tissueOpacityGrad.AddPoint(1,   0.1)
tissueOpacityGrad.AddPoint(15,   1.0)

# Tissue property
tissueVolProp = vtk.vtkVolumeProperty()
tissueVolProp.SetColor(tissueClr)
tissueVolProp.SetScalarOpacity(tissueDens)
tissueVolProp.SetGradientOpacity(tissueOpacityGrad)
tissueVolProp.SetInterpolationTypeToLinear()
# tissueVolProp.ShadeOn()
tissueVolProp.ShadeOff()

# Tissue mapper

# Ray cast functions:
tissueFunc = vtk.vtkVolumeRayCastCompositeFunction()
# tissueFunc = vtk.vtkVolumeRayCastMIPFunction()

# Different types of mappers:
# tissueMapper = vtk.vtkVolumeRayCastMapper()
tissueMapper = vtk.vtkVolumeTextureMapper2D()
# tissueMapper = vtk.vtkSmartVolumeMapper()
# tissueMapper = vtk.vtkGPUVolumeRayCastMapper()
# tissueMapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()

# tissueMapper.SetVolumeRayCastFunction(tissueFunc)
tissueMapper.SetInputConnection(tissueReader.GetOutputPort())

# Tissue Volume
tissue = vtk.vtkVolume()
tissue.SetMapper(tissueMapper)
tissue.SetProperty(tissueVolProp)
tissue.RotateY(180)


# Light
light = vtk.vtkLight()
light.SetFocalPoint(0, 0, 0)
light.SetPosition(1000, 1000, 500)
light.SetIntensity(10)

# Renderer
renderer = vtk.vtkRenderer()
if need_plane:
    renderer.AddActor(planeActor)
renderer.AddVolume(frog)
renderer.AddVolume(tissue)
renderer.AddLight(light)


# Window
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)


# Set up Tk GUI
root = tk.Tk("Frog")
# Define a quit method that exits cleanly
def quit(obj=root):
    obj.quit()

root.protocol("WM_DELETE_WINDOW", quit)
vtkw = vtkTkRenderWindowInteractor(root, rw=window, width=300, height=300)
vtkw.pack(side="left", expand="true", fill="both")

menu = tk.Frame(root, height=300, width=150)
menu.pack(side='left', fill="y")


buttons = dict()
icons = dict()
functions = dict()
opacities = dict()

def set_color(b):
    # Set color of icon and tissue
    try:
        new_color = tkColorChooser.askcolor()
        icons[b].configure(background=new_color[1])
        tClr = (float(new_color[0][0]) / 255, float(new_color[0][1]) / 255, float(new_color[0][2]) / 255)
        tissueClr.AddRGBPoint(b, tClr[0], tClr[1], tClr[2])
        window.Render()
    except Exception:
        print("Set color - failed")

def set_opacity(b):
    # Set vision of tissue
    try:
        if buttons[b].cget('relief') == tk.RAISED:
            buttons[b].config(relief=tk.SUNKEN)
            tissueDens.AddPoint(b, 1)
            tissueDens.Update()
        else:
            buttons[b].config(relief=tk.RAISED)
            tissueDens.AddPoint(b, 0)
        window.Render()
    except Exception:
        print("Set opacity - failed")

for label_idx in indexes:
    # Vision set buttons
    buttons[label_idx] = tk.Button(menu, text=tissues_labels[label_idx], width=15, font=18)
    buttons[label_idx].grid(row=(label_idx - 1), column=0)
    t_color = tissues_colors[label_idx]
    t_color = '#%02x%02x%02x' % (int(t_color[0] * 255), int(t_color[1] * 255), int(t_color[2] * 255))
    cur_idx = label_idx
    # Color set buttons
    icons[label_idx] = tk.Button(menu, width=5, background=t_color, font=18)
    icons[label_idx].grid(row=(label_idx - 1), column=1)

# Set commands
icons[1].configure(command=lambda: set_color(1))
icons[2].configure(command=lambda: set_color(2))
icons[3].configure(command=lambda: set_color(3))
icons[4].configure(command=lambda: set_color(4))
icons[5].configure(command=lambda: set_color(5))
icons[6].configure(command=lambda: set_color(6))
icons[7].configure(command=lambda: set_color(7))
icons[8].configure(command=lambda: set_color(8))
icons[9].configure(command=lambda: set_color(9))
icons[10].configure(command=lambda: set_color(10))
icons[11].configure(command=lambda: set_color(11))
icons[12].configure(command=lambda: set_color(12))
icons[13].configure(command=lambda: set_color(13))
icons[14].configure(command=lambda: set_color(14))
icons[15].configure(command=lambda: set_color(15))
# Set commands
buttons[1].configure(command=lambda: set_opacity(1))
buttons[2].configure(command=lambda: set_opacity(2))
buttons[3].configure(command=lambda: set_opacity(3))
buttons[4].configure(command=lambda: set_opacity(4))
buttons[5].configure(command=lambda: set_opacity(5))
buttons[6].configure(command=lambda: set_opacity(6))
buttons[7].configure(command=lambda: set_opacity(7))
buttons[8].configure(command=lambda: set_opacity(8))
buttons[9].configure(command=lambda: set_opacity(9))
buttons[10].configure(command=lambda: set_opacity(10))
buttons[11].configure(command=lambda: set_opacity(11))
buttons[12].configure(command=lambda: set_opacity(12))
buttons[13].configure(command=lambda: set_opacity(13))
buttons[14].configure(command=lambda: set_opacity(14))
buttons[15].configure(command=lambda: set_opacity(15))

window.Render()
root.mainloop()