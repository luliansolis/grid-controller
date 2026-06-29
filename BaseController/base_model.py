import numpy as np
import libximc.highlevel._highlevel as hl
import libximc.lowlevel._lowlevel as ll

class BaseModel:
    """
    Controls the base of the 2D system
    """
    def __init__(self, dev_id, lib, ten_cm_steps):
        """
        Initiates using the dev_id and the lib
        """
        self.axis = hl.Axis(dev_id)
        self.ll = lib
        self.ten_cm_steps = ten_cm_steps
        
    def open_device(self):
        """
        Opens the device to be able to send commands
        """
        self.axis.open_device()
    def get_position(self):
        """
        Gets the position of the 1D system, useful for debugging
        """
        self.axis.command_wait_for_stop(10) # Necessary, the device only updates after the movement is finished!
        return self.axis.get_position()
    def move_home(self):
        """
        Moves back to home, kind of janky
        """
        self.axis.command_home()
    def get_calb_settings(self):
        """
        Gets the calibration settings. They are not currently being calibrated
        """
        print(self.axis.get_calb())
    def move(self, steps):
        """
        Moves a certain amount of steps
        """
        print(f"Starting position : {self.get_position()}")
        self.axis.command_movr(steps, 0)
        print(f"Finishing position : {self.get_position()}")
    def move_cm(self, cm):
        """
        Moves a certain amount of centimeters using a "calibrated" magic number
        """
        ten_cm_steps = self.ten_cm_steps
        steps = int(ten_cm_steps*cm/10)
        self.move(steps)
    def move_to_position(self, cm):
        ten_cm_steps = self.ten_cm_steps
        print(self.axis.get_position())
        current_position_cm = self.axis.get_position().Position*10/ten_cm_steps
        target_position = cm-current_position_cm 
        self.move_cm(target_position)