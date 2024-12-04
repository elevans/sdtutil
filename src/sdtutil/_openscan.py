import os
import io
import zipfile
import sdtfile as sf
import numpy as np

def read(path: str, debug: bool = False) -> np.ndarray:
    """Read an OpenScan SDT file.

    Read an OpenScan SDT file as a NumPy array.

    :param path:

        Path to the SDT file.

    :param debug:

        Set to enable debugging mode. Headers and other steps
        will be printed to console.

    :return:

        The SDT file as a NumPy array with dimensions (lt, row, col).
    """
    with open(path, "rb") as data:
        # get sdt file header 
        header = np.rec.fromfile(
                data,
                dtype=sf.sdtfile.FILE_HEADER,
                shape=1,
                byteorder="<"
                )[0]
        
        # info -- store as metadata on an xarray?
        data.seek(header.info_offs, os.SEEK_SET)
        info = data.read(header.info_length).decode("windows-1250")
        info = info.replace("\r\n", "\n")
        
        # get the measure block
        mblock = np.rec.fromfile(
                data,
                dtype=np.dtype(sf.sdtfile.MEASURE_INFO),
                shape=1,
                byteorder="<"
                )
        
        # assume similar config for all channels
        adc_re = int(mblock.adc_re[0])
        image_x = int(mblock.image_x)
        image_y = int(mblock.image_y)
        t = np.arange(adc_re, dtype = "float64")
        t *= mblock.tac_r / float(mblock.tac_g * adc_re)
        
    return mblock 
