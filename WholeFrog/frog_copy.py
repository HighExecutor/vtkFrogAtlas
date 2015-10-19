import vtk
import Tkinter as tk
import numpy
from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor
import tkColorChooser


path = './WholeFrog/frog.'

# Plane
texReader = vtk.vtkJPEGReader()
texReader.SetFileName("./grass.jpg")
atext = vtk.vtkTexture()
atext.SetInputConnection(texReader.GetOutputPort())
atext.InterpolateOn()

plane = vtk.vtkPlaneSource()
plane.SetResolution(0.01, 0.01)
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(1000, 0, 0)
plane.SetPoint2(0, 1000, 0)
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(plane.GetOutputPort())
planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.SetPosition(-750, -250, -200)
planeActor.SetTexture(atext)

# Frog
# Source
# frogReader = vtk.vtkImageReader()
# frogReader.SetDataByteOrderToLittleEndian()
# frogReader.SetDataExtent(0, 499, 0, 469, 1, 136)
# frogReader.SetDataSpacing(1, 1, 1.5)
# frogReader.SetDataScalarTypeToUnsignedChar()
# frogReader.SetFileDimensionality(2)
# frogReader.SetFilePrefix(path)
# frogReader.SetFilePattern("%s%03d.raw")
# frogReader.Update()
#
# frogDens = vtk.vtkPiecewiseFunction()
# frogDens.AddPoint(0.0, 0.0)
# frogDens.AddPoint(60.0, 0.0)
# frogDens.AddPoint(110.0, 0.02)
# frogDens.AddPoint(150.0, 0.05)
# frogDens.AddPoint(200.0, 0.1)
# frogDens.AddPoint(230.0, 0.15)
#
# frogClr = vtk.vtkColorTransferFunction()
# frogClr.AddRGBPoint(0.0, 0.0, 0.26, 0.1)
# frogClr.AddRGBPoint(25.0, 0.0, 0.4, 0.15)
# frogClr.AddRGBPoint(50.0, 0.1, 0.5, 0.25)
# frogClr.AddRGBPoint(75.0, 0.2, 0.6, 0.36)
# frogClr.AddRGBPoint(100.0, 0.25, 0.7, 0.45)
# frogClr.AddRGBPoint(125.0, 0.4, 0.76, 0.64)
# frogClr.AddRGBPoint(150.0, 0.6, 0.83, 0.71)
# frogClr.AddRGBPoint(175.0, 0.7, 0.88, 0.79)
# frogClr.AddRGBPoint(200.0, 0.85, 0.94, 0.94)
# frogClr.AddRGBPoint(225.0, 0.9, 0.97, 0.97)
# frogClr.AddRGBPoint(250.0, 0.96, 0.98, 0.98)

# frogFunc = vtk.vtkVolumeRayCastCompositeFunction()

# frogMapper = vtk.vtkVolumeRayCastMapper()
# frogMapper = vtk.vtkSmartVolumeMapper()
# frogMapper = vtk.vtkGPUVolumeRayCastMapper()
# frogMapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
# frogMapper.SetInputConnection(frogReader.GetOutputPort())
# frogMapper.SetVolumeRayCastFunction(frogFunc)

# frogVolProp = vtk.vtkVolumeProperty()
# frogVolProp.SetColor(frogClr)
# frogVolProp.SetScalarOpacity(frogDens)
# frogVolProp.SetInterpolationTypeToLinear()
# frogVolProp.ShadeOn()

# frog = vtk.vtkVolume()
# frog.SetMapper(frogMapper)
# frog.SetProperty(frogVolProp)
# frog.RotateY(180)

# Frog's tissues
tissueReader = vtk.vtkImageReader()
tissueReader.SetDataByteOrderToLittleEndian()
tissueReader.SetDataExtent(0, 499, 0, 469, 1, 136)
tissueReader.SetDataSpacing(1, 1, 1.5)
tissueReader.SetDataScalarTypeToUnsignedChar()
tissueReader.SetFileDimensionality(2)
tissueReader.SetFilePrefix('./WholeFrog/frogTissue.')
tissueReader.SetFilePattern("%s%03d.raw")
tissueReader.Update()

frogDens = vtk.vtkPiecewiseFunction()
frogDens.AddPoint(0.0, 0.0)
frogDens.AddPoint(60.0, 0.0)
frogDens.AddPoint(110.0, 0.02)
frogDens.AddPoint(150.0, 0.05)
frogDens.AddPoint(200.0, 0.1)
frogDens.AddPoint(230.0, 0.15)

frogClr = vtk.vtkColorTransferFunction()
frogClr.AddRGBPoint(0.0, 0.0, 0.26, 0.1)
frogClr.AddRGBPoint(25.0, 0.0, 0.4, 0.15)
frogClr.AddRGBPoint(50.0, 0.1, 0.5, 0.25)
frogClr.AddRGBPoint(75.0, 0.2, 0.6, 0.36)
frogClr.AddRGBPoint(100.0, 0.25, 0.7, 0.45)
frogClr.AddRGBPoint(125.0, 0.4, 0.76, 0.64)
frogClr.AddRGBPoint(150.0, 0.6, 0.83, 0.71)
frogClr.AddRGBPoint(175.0, 0.7, 0.88, 0.79)
frogClr.AddRGBPoint(200.0, 0.85, 0.94, 0.94)
frogClr.AddRGBPoint(225.0, 0.9, 0.97, 0.97)
frogClr.AddRGBPoint(250.0, 0.96, 0.98, 0.98)

def createActor( thr, reader, color, opacity ):

    # adding discrete marching cubes algorithm
    # mc = vtk.vtkMarchingCubes()
    mc = vtk.vtkContourFilter()
    # mc.ComputeScalarsOff()
    mc.SetInputConnection(reader.GetOutputPort())
    mc.GenerateValues(1, thr, thr)
    mc.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(mc.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    prop = vtk.vtkProperty()
    prop.SetColor(color)
    prop.SetOpacity(opacity)

    # prop.BackfaceCullingOn()
    actor.SetProperty(prop)
    actor.RotateY(180)
    return actor

indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# indexes = [1, 2, 4, 5, 6, 8, 12, 13, 15]
tissues_labels = {1:'blood', 2:'brain', 3:'duodenum', 4:'eye retina', 5:'eye_white', 6:'heart', 7:'ileum', 8:'kidney',
                  9:'large intestine', 10:'liver', 11:'lung', 12:'nerve', 13:'skeleton', 14:'spleen', 15:'stomach'}

tissues_colors = {1:(1, 0, 0), 2:(1, 0.3, 0.5), 3:(0, 0, 0), 4:(0, 1, 0), 5:(1, 1, 1),
                  6:(0.9, 0.1, 0.1), 7:(0, 0, 0), 8:(0.4, 0.1, 0.9), 9:(0, 0, 0), 10:(0.6, 0.5, 0), 11:(0, 0, 0),
                  12:(0.9, 0.5, 0.2), 13:(0.8, 0.8, 0.8), 14:(0, 0, 0), 15:(0.4, 0.2, 0.7)}

tissues_opacities = {1:0.3, 2:1, 3:0.3, 4:0.9, 5:0.9,
                  6:0.9, 7:0.3, 8:0.9, 9:0.2, 10:0.2, 11:0.2,
                  12:0.6, 13:0.4, 14:0.2, 15:0.1}
rend_tissues = True
tissues = []
if rend_tissues:
    # for t in indexes:
    for t in [4]:
        tissues.append(createActor(t, tissueReader, tissues_colors[t], tissues_opacities[t]))
        print(tissues_labels[t] + " has been built")

# Light
# light = vtk.vtkLight()
# light.SetFocalPoint(0, 0, 0)
# light.SetPosition(1000, 1000, 500)
# light.SetDiffuseColor(0.1, 1, 0.1)
# light.SetIntensity(10)

# Renderer
renderer = vtk.vtkRenderer()
# renderer.AddActor(planeActor)
# renderer.AddVolume(frog)
# renderer.AddLight(light)
# for tissue in tissues:
#     renderer.AddActor(tissue)
# renderer.AddActor(tissues[0])


# renderer.SetBackground(1.0, 1.0, 1.0)

# Camera
# camera = renderer.MakeCamera()
# camera.SetPosition(800.0, 800.0, 500.0)
# camera.SetFocalPoint(0.0, 0.0, 0.0)
# camera.SetViewAngle(30.0)
# camera.SetRoll(45.0)
# renderer.SetActiveCamera(camera)


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

# def set_color(b):
#         new_color = tkColorChooser.askcolor()
#         icons[b].configure(background=new_color[1])
#         tissues[b-1].GetProperty().SetColor(float(new_color[0][0]) / 255, float(new_color[0][1]) / 255, float(new_color[0][2] / 255))
#
# def set_opacity():
#     for b in indexes:
#         new_opacity = float(opacities[b].get())
#         tissues[b-1].GetProperty().SetOpacity(new_opacity)
#
# for label_idx in indexes:
#     buttons[label_idx] = tk.Button(menu, text=tissues_labels[label_idx], width=10)
#     buttons[label_idx].grid(row=(label_idx - 1), column=0)
#     t_color = tissues_colors[label_idx]
#     t_color = '#%02x%02x%02x' % (int(t_color[0] * 255), int(t_color[1] * 255), int(t_color[2] * 255))
#     cur_idx = label_idx
#     icons[label_idx] = tk.Button(menu, width=5, background=t_color)
#     icons[label_idx].grid(row=(label_idx - 1), column=1)
#     opacities[label_idx] = tk.Entry(menu, width=3)
#     opacities[label_idx].insert(tk.END, tissues_opacities[label_idx])
#     opacities[label_idx].grid(row=(label_idx - 1), column=2)



# icons[1].configure(command=lambda: set_color(1))
# icons[2].configure(command=lambda: set_color(2))
# icons[3].configure(command=lambda: set_color(3))
# icons[4].configure(command=lambda: set_color(4))
# icons[5].configure(command=lambda: set_color(5))
# icons[6].configure(command=lambda: set_color(6))
# icons[7].configure(command=lambda: set_color(7))
# icons[8].configure(command=lambda: set_color(8))
# icons[9].configure(command=lambda: set_color(9))
# icons[10].configure(command=lambda: set_color(10))
# icons[11].configure(command=lambda: set_color(11))
# icons[12].configure(command=lambda: set_color(12))
# icons[13].configure(command=lambda: set_color(13))
# icons[14].configure(command=lambda: set_color(14))
# icons[15].configure(command=lambda: set_color(15))

# set_op = tk.Button(menu, text="Set opacities", command=set_opacity)
# set_op.grid(row=16, column=0)
#
# menu.pack()

# opacities[1].configure(validate='focusout', validatecommand=lambda: set_opacity(1))
# opacities[2].configure(validate='focusout', validatecommand=lambda: set_opacity(2))
# opacities[3].configure(validate='focusout', validatecommand=lambda: set_opacity(3))
# opacities[4].configure(validate='focusout', validatecommand=lambda: set_opacity(4))
# opacities[5].configure(validate='focusout', validatecommand=lambda: set_opacity(5))
# opacities[6].configure(validate='focusout', validatecommand=lambda: set_opacity(6))
# opacities[7].configure(validate='focusout', validatecommand=lambda: set_opacity(7))
# opacities[8].configure(validate='focusout', validatecommand=lambda: set_opacity(8))
# opacities[9].configure(validate='focusout', validatecommand=lambda: set_opacity(9))
# opacities[10].configure(validate='focusout', validatecommand=lambda: set_opacity(10))
# opacities[11].configure(validate='focusout', validatecommand=lambda: set_opacity(11))
# opacities[12].configure(validate='focusout', validatecommand=lambda: set_opacity(12))
# opacities[13].configure(validate='focusout', validatecommand=lambda: set_opacity(13))
# opacities[14].configure(validate='focusout', validatecommand=lambda: set_opacity(14))
# opacities[15].configure(validate='focusout', validatecommand=lambda: set_opacity(15))

# def SetDens(r):
    # mcs[0].GenerateValues(1, float(r), float(r))
    # mcs[0].Update()
#     window.Render()

# slider = Tkinter.Scale(root, label="Density", orient="horizontal", command=SetDens, from_=0, to=10000)
# slider.set(900)
# slider.pack(side="top", expand="true", fill="both")
# Start handling interaction events
window.Render()

window.Render()
root.mainloop()
# for i in range(100):
#     print("move")
#     pos = frog.GetPosition()
#     frog.SetPosition(pos[0], pos[1], pos[2] + 5)
#     window.Render()







