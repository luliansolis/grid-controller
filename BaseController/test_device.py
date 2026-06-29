import pyvisa
import libximc.lowlevel._lowlevel as ll
from base_model import BaseModel
def get_id():
    rm = pyvisa.ResourceManager()

    # List all connected devices
    print(rm.list_resources())
    # e.g. ('USB0::0x0699::0x0346::C012345::INSTR', 'GPIB0::1::INSTR')

def load_lib_test():
    lib = ll._load_lib()
    print(lib)
def test_if_loaded():
    dev_uri = r"xi-com:///dev/ttyACM0"
    lib = ll._load_lib()
    base_model = BaseModel(dev_uri, lib)
    base_model.open_device()
    print(base_model.axis._device_id)
def opening_routine():
    dev_uri = r"xi-com:///dev/ttyACM0"
    lib = ll._load_lib()
    base_model = BaseModel(dev_uri, lib, 8100)
    base_model.open_device()
    return base_model
def test_position():
    bm = opening_routine()
    print(bm.get_position())
def test_move_left():
    bm = opening_routine()
    print(bm.move_left())
def test_calb_settings():
    bm = opening_routine()
    print(bm.get_calb_settings())
def test_move():
    bm = opening_routine()
    print(bm.move(-4*8100))
test_move()