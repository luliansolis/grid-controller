import numpy as np
import serial
from pynput import keyboard
import time
class TopModel:
    """
    Controls the top 2D belt
    """
    def __init__(self, port, baudrate, ten_cm_steps):
        """
        Initiates the instance using a port and baudrate
        """
        self.port = port 
        self.current_position = 0 # Manually set the position at zero for each 
        self.ten_cm_steps = ten_cm_steps
        self.start_serial(baudrate)

    def start_serial(self, baudrate):
        """
        Starts the serial channel to the Arduino
        """
        self.serial = serial.Serial()
        self.serial.port = self.port
        self.serial.baudrate = baudrate
        self.serial.open()
    def get_position(self):
        return self.current_position
    def zero_here(self):
        self.current_position = 0
    def reverse(self):
        """
        Reverses the belt
        """
        self.serial.write(b"R\n")
    def stop(self):
        """
        Stops the belt
        """
        self.serial.write(b"S\n")
    def move_mm(self, mm):
        ten_cm_steps = self.ten_cm_steps
        
        conv = int(mm/100*ten_cm_steps)
        print(f"We get the conv {conv} with {self.ten_cm_steps} as step and {mm} as input")
        self.current_position -= mm/10
        if self.current_position < 0:
            self.current_position = 0
        #print(f"I:{conv}\n".encode())
        self.serial.write(f"I:{conv}\n".encode())
    def move_to_position(self, mm):
        """
        Move to certain position in mm 
        """
        mm_inverse = -mm # Change because my dumbass has reversed signs in Arduino

        target_position = mm_inverse-self.current_position*10 
        #if target_position < -self.current_position:
        #    target_position = -self.current_position
        self.move_mm(-target_position)
    def push_to_zero(self):
        print("Top 2")
        self.move_mm(100)
        self.current_position = 0
    def on_press(self, key):
        if key == keyboard.Key.right:
            self.serial.write(f"I:{-10}\n".encode())
            time.sleep(0.1)
        if key == keyboard.Key.left:
            self.serial.write(f"I:{10}\n".encode())
            time.sleep(0.1)
        if key == keyboard.Key.esc:
            return False
    def start(self):
        with keyboard.Listener(on_press = self.on_press) as listener:
            listener.join()