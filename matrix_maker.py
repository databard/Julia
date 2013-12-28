###############################################################
## matrix_maker.py                                           ##
## --------------------------------------------------------- ##
## Functions to make matrices                                ##
###############################################################

from pyopencl import array
import numpy

## Serialized Input Matrix
## ---------------------------------------------------------
## Desc: Creates a 1D array with desired coordinates in each 
## index
## ---------------------------------------------------------
## Input: size: (int, int) touple dictating the number of x
##            and y points to use (will translate directly
##            into pixels when making an image)
##        center: (int, int) The cartesian point to center 
##            the image around
##        scale: float defining how far from the center to
##            traverse. Must be greater than zero
## ---------------------------------------------------------
def serial_input_matrix(size, center, scale):
	## Calculate necessary ratio of height/width
	ratio = scale*(float(size[1])/size[0])
	## Generate start and end coordinated needed to do calculation
	coords = (center[0]-scale, center[1]-ratio, center[0]+scale, center[1]+ratio)
	## Calculate how much to increment each step
	increment = float(scale*2)/size[0]
	## Create matrix
	matrix = numpy.zeros(size[0]*size[1], array.vec.float2)
	for i in range(size[1]):
		for j in range(size[0]):
			matrix[i*size[0]+j] = ((j*increment)+coords[0], coords[3]-(i*increment))

	return matrix

## Serialized Output Heightmap
## ---------------------------------------------------------
## Desc: Generates a 1D array with x,y,z parts for use with
##       3D model generation
## ---------------------------------------------------------
## Input: size: (int, int) touple dictating the number of x
##            and y points to use (will translate directly
##            into pixels when making an image)
##        input_matrix: serialized matrix of ints created
##            using the fractal_cl.fractal_cl function
##        iters: defines how many iterations were used in
##            the fractal_cl generation function.
##        max_height: The maximum z value for the points.
##            All values will be scaled to this max.
## ---------------------------------------------------------
def serial_heightmap_matrix(size, input_matrix, iters = 256, max_height = 100):
	matrix = numpy.zeros(size[0]*size[1], dtype = ('f8,f8,f8'))
	for i in range(size[1]):
		for j in range(size[0]):
			#matrix[i*size[0]+j] = ((j*increment)+coords[0], (i*increment)+coords[1])
			matrix[i*size[0]+j] = (
									matrix[i*size[0]+j][0],
									matrix[i*size[0]+j][0][1],
									(input_matrix[i*size[0]+j]/float(iters))*max_height,
								  )
	return matrix

## Image Output Matrix
## ---------------------------------------------------------
## Desc: Generates a 2D array or pizels with (r,g,b) values
## Derived from a defined gradient
## ---------------------------------------------------------
## Input: size: (int, int) touple dictating the number of x
##            and y points to use (will translate directly
##            into pixels when making an image)
##        input_matrix: serialized matrix of ints created
##            using the fractal_cl.fractal_cl function
##        gradient: Gradient array of RGB values generated
##            via the gradient.gradient function
## ---------------------------------------------------------
def image_matrix(size, input_matrix, gradient):
	matrix = numpy.zeros((size[1],size[0]), dtype=('i4,i4,i4'))
	for i in range(size[1]):
		for j in range(size[0]):
			## If gradient is out of bounds, get last colour value instead
			try:
				matrix[i][j] = gradient[input_matrix[i*size[0]+j]]
			except:
				matrix[i][j] = gradient[-1]

	return matrix