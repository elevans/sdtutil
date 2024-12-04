import numpy as np
from sdtutil import _openscan

def sdt_to_ndarray(path: str, file_format: str, debug: bool = False) -> np.ndarray:
    """
    """
    if file_format == "openscan":
        return _openscan.read(path, debug)
