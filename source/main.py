#!/usr/bin/python
from __future__ import print_function
from numpy import array
# Read PDE solution from VTK
# Reference: http://stackoverflow.com/questions/23138112/vtk-to-maplotlib-using-numpy
import vtk
from vtk.util.numpy_support import vtk_to_numpy
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName("solution.0.0.vtk")
reader.Update()
nodes_vtk_array = reader.GetOutput().GetPoints().GetData()
u_vtk_array = reader.GetOutput().GetPointData().GetArray(0)
nodes_numpy_array = vtk_to_numpy(nodes_vtk_array)
x, y = nodes_numpy_array[:, 0], nodes_numpy_array[:, 1]
u_numpy_array = vtk_to_numpy(u_vtk_array)
u = u_numpy_array
print("x = ", x)
print("y = ", y)
print("u = ", u)
# Make interpolant using radial basis functions; this will be used for the constraints
