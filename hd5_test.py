import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

f = h5py.File('tek1.h5', 'r')

print(list(f.keys()))
print(f)

# Tektronix


dat = f['/Data']
item = f['/Spacing']
start = f['/StartTime']

print(dat.len())
print(item.value)
print(start.value)

'''
item = f["/Frame/TheFrame"]
dat = f["/Waveforms/Memory 1"]
dat1 = f["/Waveforms/Memory 1/Memory 1Data"]
head = f["/FileType/KeysightH5FileType"]

print(head.value)
print(list(dat.attrs.items()))
print(list(dat1.attrs.items()))
print(dat)
print(dat1.value)
print("****")
'''
#print(list(dat.items()))

f.clear()
f.close()

def hdfReadTektronix(tktxFile):
    ''' read tktxFile and return data as numpy array
    Oscilloscope Tektronix DPO 5204
    :param tkTNxFile: path to hdf file
    '''
    try:
        f = h5py.File(tktxFile, 'r')
        dataset = f['/Data']
        XIncr = f['/Spacing']
        XOrg = f['/StartTime']
        stop = XOrg.value + dataset.len() * XIncr.value
        time = np.linspace(XOrg.value, stop, dataset.len())
        data = dataset.value
        return time, data
    except:
        sys.stderr.write("%s open error\n" & (tktxFile))
        return None, None
    finally:
        f.clear()
        f.close()


def hdfReadKeysight(h5file):
    ''' read h5file and return data as numpy array
    Oscilloscope Infinium S-series
    :h5file: path to bin file
    '''
    memory1atrr = namedtuple("memory1atrr",
                                "waveformType Start nPoints NumSegments\
                                count xDispRange xDispOrigin xInc xOrg \
                                xUnits yDispRange yDispOrigin YInc YOrg \
                                yReference yUnits minBandwidth maxBandwidth \
                                SavedIntFct DispIntFct IntSetting WavAttr FFT_RBW")

    m1dataAttr = namedtuple("m1dataAttr",
                                "LfdSeed StartIndex DataType DecMode \
                                PktSize RawNumPst ReductionAllowed \
                                MemConIntlvMode InfoValid SegmentedTimeTag \
                                SegmentedXOrg")
    try:
        f = h5py.File(h5file, 'r')
        if f["/FileType/KeysightH5FileType"].value != b'Keysight Waveform':
            return None, None
        mem = f["/Waveforms/Memory 1"]
        dataset = f["/Waveforms/Memory 1/Memory 1Data"]
        attr1 = memory1atrr._make(list(mem.attrs.values()))
        d1attr = m1dataAttr._make(list(dataset.attrs.values()))
        stop = attr1.xOrg + attr1.nPoints * attr1.xInc
        time = np.linspace(attr1.xOrg, stop, attr1.nPoints)
        data = dataset.value
        return time, data
    except:
        sys.stderr.write("%s open error\n" & (h5file))
        return None, None
    finally:
        f.clear()
        f.close()


#t, r = hdfReadKeysight('gg.h5')
t, r = hdfReadTektronix('tek1.h5')

t1 = np.array(t)
r1 = np.array(r)

plt.plot(t1, r1)
plt.show()
