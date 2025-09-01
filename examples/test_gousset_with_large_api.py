import pygmich.hcimg_core.computer_vision as cv
import numpy as np
import gousset


# gousset.instrument(gousset)  # time the instrumentation setup
# gousset.instrument(np)  # time the numpy
# gousset.instrument(cv, "binary_dilation")  # time only one function
gousset.instrument(cv)


x = np.random.randn(100, 100, 100) > 0

z = x * 3

y = cv.binary_dilation(x)  # this gets time

m = cv.binary_erosion(x)  # this does not
