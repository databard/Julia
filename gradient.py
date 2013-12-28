###############################################################
## gradient.py                                               ##
## --------------------------------------------------------- ##
## Gradient Generator Function                               ##
###############################################################
import numpy

## Gradient Function
## ---------------------------------------------------------
## Desc: Generates an array of RGB values, making smooth
## transitions from input points
## ---------------------------------------------------------
## Input: points: A list of points in the form
##                  [[index, (int,int,int)],]
##           points must be in order, with the first point
##           index being 0. The touple of ints dictate RGB
##           values and can be between 0 and 255
##        length: int defining how long the gradient is.
##            longer gradients may be necessary to colour
##            fractals with a high number of iterations
## ---------------------------------------------------------

def gradient(points, length=256):
	grad = numpy.zeros(length, dtype=('i4,i4,i4'))
	for i,point in enumerate(points):
		## If the first point is not zero, fill in up to first point
		if i == 0:
			for j in range(point[0]):
				grad[j] = point[1]
		else:
			## Generate gradient between points
			diff_val = abs(point[0]-points[i-1][0])
			scale_r = numpy.linspace(points[i-1][1][0], point[1][0], diff_val)
			scale_g = numpy.linspace(points[i-1][1][1], point[1][1], diff_val)
			scale_b = numpy.linspace(points[i-1][1][2], point[1][2], diff_val)
			for j, ind in enumerate(range(points[i-1][0], point[0])):
				grad[ind] = (scale_r[j], scale_g[j], scale_b[j])

		## Check if the point is the last one (Hackey..)
		try: 
			points[i+1]
		except:
			## If the last point isn't at the end of the array,
			## fill the rest of the array with the last colour
			if point[0] != length:
				for j in range(point[0], length):
					grad[j] = point[1]

	## Return the completed gradient
	return grad

## Example gradients
## ---------------------------------------------------------
## Put some examples here