import hd5Tektx
import pylab

file = 'tek1.h5'

t, r = hd5Tektx.hdfReadTektronix(file)

pylab.plot(t, r)
pylab.show()

print("Test finished")