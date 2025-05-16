import pytest
import MPDSnCxx_Interface

def test():
    vid = "0403"
    pid = "6001"
    serialNum = "AK08MWEAA"
    try:
        rf_interface = MPDSnCxx_Interface.MPDSnCxx_Interface(vid, pid, serialNum)
    except RuntimeError as X:
        assert str(X) == "Device not found"
        
        
if __name__ == "__main__":
    pytest.main()