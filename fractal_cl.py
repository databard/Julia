###############################################################
## fractal_cl.py                                             ##
## --------------------------------------------------------- ##
## Gradient Generator Function                               ##
###############################################################
import numpy
import pyopencl as cl


## Opencl Fractal Calculator
## ---------------------------------------------------------
## Desc: Utilizes pyopencl to calculate all the points
## for a julia-style fractal
## ---------------------------------------------------------
## Input: size: (int, int) touple dictating the number of x
##            and y points to use (will translate directly
##            into pixels when making an image)
##        matrix: Serialized array of x,y touples (dtype =
##            cl.array.vec.float2). Can be generated using
##            matrix_maker.serial_input_matrix
##        constant: (float, float) touple for the input
##            constant for doing calculations.
##        iters: Defines number of iterations for the
##            calculations to run through. More will result
##            in a more detailed image, but take longer
##        term: Value for the equation to hit before 
##            terminating.
##        equation: Equation to use in calculation
## ---------------------------------------------------------
## Output: A serialized array of integers representing the
##    number of iterations before ternimation. Number counts
##    downwards currently for mysterious reasons
## ---------------------------------------------------------
def fractal_cl(size, matrix, constant, iters = 255, term = 2,
	           equation = "cfloat_add(cfloat_powr(z,2), c)"):
	## Collect prereqs for opencl process
	platform = cl.get_platforms()[0]
	device = platform.get_devices()[0]
	context = cl.Context([device])

	## The actual opencl program
	program = cl.Program(context, """
		#include <pyopencl-complex.h>
		__kernel void fractal_point(__global const float2 *matrix,
		__global const float2 *vector, __global float *result)
		{
			int gid = get_global_id(0);
			int n = %s;
			float2 z = matrix[gid];
			float2 c = vector[0];
			while(n != 0 && cfloat_abs(z) < %s)
			{
				z = %s;
				n = n-1;
			}
			result[gid] = n;
		}
		""" % (iters, term, equation)).build()

	## Map input constant
	vector = numpy.zeros((1,2), cl.array.vec.float2)
	vector[0,0] = constant

	## Buffers and memory and shit
	queue = cl.CommandQueue(context)
	mem_flags = cl.mem_flags
	matrix_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=matrix)
	vector_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=vector)
	fractal = numpy.zeros((size[0]*size[1]), numpy.float32)
	destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, fractal.nbytes)
	program.fractal_point(queue, fractal.shape, None, matrix_buf, vector_buf, destination_buf)
	cl.enqueue_copy(queue, fractal, destination_buf)

	return fractal