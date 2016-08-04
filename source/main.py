#!/usr/bin/python
from __future__ import print_function
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
#from scipy.interpolate import Rbf, griddata
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
# Read PDE solution from VTK
# Reference: http://stackoverflow.com/questions/23138112/vtk-to-maplotlib-using-numpy
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName("PDE/run/solution.0.10.vtk")
reader.Update()
nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
# Remove redundant points that are in the VTK format for whatever reason.
# Reference: http://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array
table = np.column_stack((nodes[:, 0], nodes[:, 1], u))
temp = np.ascontiguousarray(table).view(np.dtype((np.void, table.dtype.itemsize * table.shape[1])))
_, idx = np.unique(temp, return_index=True)
table = table[idx]
# Rename for convenience
[x, y, u] = table[:,0], table[:,1], table[:,2]
nodes = np.column_stack((x, y));
# Make interpolant using radial basis functions; this will be used for the constraints
# Reference: http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#using-radial-basis-functions-for-smoothing-interpolation
# Cubic looks okay, except for inside of the body; can't really omit inside of the body with RBF's
ni = 100
xi = np.linspace(min(x), max(x), ni)
yi = np.linspace(min(y), max(y), ni)
XI, YI = np.meshgrid(xi, yi)
UI = griddata(x, y, u, XI, YI)
# plot the result
plt.interactive(False)
plt.subplot(1, 1, 1)
plt.pcolor(XI, YI, UI, cmap=cm.jet)
plt.scatter(x, y, 10, u, cmap=cm.jet)
plt.axis('equal')
plt.title('RBF interpolation - multiquadrics')
plt.colorbar()
plt.show()
