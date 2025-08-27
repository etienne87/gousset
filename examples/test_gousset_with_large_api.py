import pygmich.hcimg_core.computer_vision as cv
import numpy as np
import gousset


gousset.instrument(gousset) # time the instrumentation setup
gousset.instrument(np)      # time the numpy
gousset.instrument(cv)      # time the computer vision lib


x = np.random.randn(100,100,100) > 0

y = cv.binary_dilation(x)

