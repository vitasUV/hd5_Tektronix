import sys
import h5py
import numpy as np

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