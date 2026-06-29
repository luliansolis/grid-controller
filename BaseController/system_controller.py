from base_model import BaseModel
from top_model import TopModel
import libximc.lowlevel._lowlevel as ll
import json
import threading
import queue
from matlab_interface import OscClient
class SystemController:
    """
    Sends commands to the base and top model, from the Manual Movement interface
    """
    def __init__(self, config_file):
        """
        Inits the base and top model. Since the base model uses a device, a priority queue is used
        to send commands instead of threading
        """
        with open(config_file, "r") as f:
            self.params = json.load(f)
        self._initiate_base_model()
        self._initiate_top_model()
        if self.params["with_osc_client"]:
            self._initiate_os_client()
        else:
            self.os_client = None
        self._queue_top_controller_starter()
        t = threading.Thread(target = self._queue_top_controller_consumer, daemon = True)
        t.start()
    def _initiate_top_model(self):
        """
        Starts the top model. 
        """
        baudrate = self.params["baudrate"]
        ten_steps = self.params["top_ten_steps"]
        port = self.params["port"]
        self.top_mod = TopModel(port, baudrate, ten_steps)
    
    def _initiate_base_model(self):
        """
        Starts the base model 
        """
        lib = ll._load_lib()
        dev_id = self.params["dev_id"]
        ten_steps = self.params["bot_ten_steps"]
        self.base_mod = BaseModel(dev_id, lib, ten_steps)
    def _initiate_os_client(self):
        """
        Starts the oscilloscope client
        """
        path_name = self.params["path"]
        filename = self.params["filename"]
        self.os_client = OscClient(filename, path_name)
    def _queue_top_controller_starter(self):
        """
        Creates the queue for the controller
        """
        self.queue = queue.Queue()
    def _queue_top_controller_consumer(self):
        """
        A threaded consumer that fires commands whenever a command is put into the queue
        """
        self.base_mod.open_device()
        while True:
            cmd = self.queue.get()
            cmd()
    def queue_top_controller_feeder(fn):
        """
        Feeds the commands using a wrapper
        """
        def wrapper(self, *args, **kwargs):
            print("Displacement Task")
            self.queue.put(lambda: fn(self, *args))
        return wrapper
    """
    The following methods move the base model. Every command is put into the queue
    """
    @queue_top_controller_feeder
    def zero_base_model(self):
        self.base_mod.move_home()
    @queue_top_controller_feeder
    def move_bot_mm(self, mm):
        self.base_mod.move_to_position(mm/10)
    @queue_top_controller_feeder
    def move_right_bot(self):
        self.base_mod.move_cm(-1)
    @queue_top_controller_feeder    
    def move_left_bot(self):
        self.base_mod.move_cm(1)
    def get_position_bottom(self, coords, event):
        def get_pos_task():
            coords['x'] = self.base_mod.get_position().Position/810
            event()
        self.queue.put(get_pos_task)
        print("Changed")
    """
    The following methods move the top model using serial commands
    """
    def get_position_top(self):
        print(self.top_mod.get_position())
        return self.top_mod.get_position()
    def zero_top_model(self):
        self.top_mod.zero_here()
    def move_right_top(self):
        self.top_mod.move_mm(-10)
    def move_left_top(self):
        self.top_mod.move_mm(10)
    def move_top_mm(self, mm):
        self.top_mod.move_to_position(mm)
    def push_top_to_zero(self):
        self.top_mod.push_to_zero()

    """
    The following methods are meant for oscilloscope capture and viz. To do them, I need to run
    the oscilloscope client first
    """
    def osc_capture(self, x, y):
        self.os_client.get_data(x, y, self.params["orientation"], self.params["att"])
    """
    Helper methods. Since the Arduino fulfills the serial, we need to constantly consume from it
    An alternative is obviously not fulfilling the serial, but knowing what the Arduino does is important
    """
    def top_serial_in_waiting(self):
        return self.top_mod.serial.in_waiting
    def top_serial_read(self):
        return self.top_mod.serial.readline()
    def top_position(self):
        return self.top_mod.get_position()