import numpy, Image
from gradient import gradient
from fractal_cl import fractal_cl
from matrix_maker import serial_input_matrix, image_matrix

## Set up inputs
## Example Gradient (grey and red with black tips)
grad = gradient([[0,(0,0,0)], [730,(200,0,0)], [1000,(25,25,25)]], length = 1000)
## Image Size in pixels
size = (400,400)
## Point to center image around
center = (0,0)
## How far to traverse (-scale to scale around center)
scale = 1
## Input constant
constant = (-0.70176,-0.3842)

equation = "cfloat_add(cfloat_powr(z,2), c)"
eqname = "Julia"

## Create input matrix
in_matrix = serial_input_matrix(size, center, scale)

## Do the stuff
fractal = fractal_cl(size, in_matrix, constant, iters = 999, equation = equation)
image = image_matrix(size, fractal, grad)


## Make an image
img = Image.fromarray(image.astype('uint8,uint8,uint8'), 'RGB')
img.save('%s_%s_%s.png' % (eqname, constant[0], constant[1]))