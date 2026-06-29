import tkinter as tk
from top_model import TopModel
from base_model import BaseModel
from system_controller import SystemController
import threading
class ControllerGUI:
    """
    Creates a GUI for Axis movement
    """
    def __init__(self):
        """
        Lots of stuff to create the buttons and whatnot
        """
        
        self.coord = {"x": 0, "y": 0}
        self.root = tk.Tk()
        self.root.title("2D Control")
        self.controller = SystemController("config.json")
        tk.Label(self.root, text = "Base Movement").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text = "Top Movement").grid(row=0, column=2, columnspan=2)
        self.text_input_bot = tk.Entry(self.root)
        self.text_input_bot.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.text_input_bot.bind("<Return>", self.move_bot_mm)
        self.text_input_top = tk.Entry(self.root)
        self.text_input_top.grid(row=1, column=2, columnspan=2, padx=10, pady=10)
        self.text_input_top.bind("<Return>", self.move_top_mm)
        tk.Button(self.root, text="Left", width=10, command=self.left_bot).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Right", width=10, command=self.right_bot).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Left", width=10, command=self.left_top).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Right", width=10, command=self.right_top).grid(row=2, column=3, padx=5, pady=5)
        tk.Button(self.root, text="Zero", width=10, command=self.zero_bot).grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        tk.Button(self.root, text="Zero", width=10, command=self.zero_top).grid(row=3, column=2, columnspan=2, padx=10, pady=5)
        self.text_coords = tk.StringVar()
        self.text_coords_label = tk.Label(self.root, textvariable=self.text_coords)
        self.text_coords_label.grid(row = 4, column = 1, columnspan = 2, padx = 10, pady = 10)
        self.text_coords.set(f"Coords : [{self.coord['x']}, {self.coord['y']}]")
        if self.controller.os_client is not None:
            tk.Button(self.root, text="Capture", width = 40, command = self.osc_capture).grid(row = 5)

    def threaded(fn):
        """
        Creates a thread for each command
        """
        def wrapper(*args, **kwargs):
            threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
        return wrapper
    def _set_coords(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.set_coords()
            return
        return wrapper
    @threaded
    def set_coords(self):
        event = threading.Event()
        self.controller.get_position_bottom(self.coord, event.set)
        event.wait()
        print(f"Value is: {self.coord['x']}")
        self.coord["y"] = self.controller.get_position_top()
        self.text_coords.set(f'Coords : [{self.coord["x"]}, {self.coord["y"]}]')
 
    """
    Send commands to the System Controller
    """
    @threaded
    def check_coords(self):
        print("Top")
        self.controller.push_top_to_zero()
        self.set_coords()

    @threaded
    def osc_capture(self):
        self.controller.osc_capture(self.coord["x"], self.coord["y"])
    @threaded
    @_set_coords
    def left_bot(self):
        self.controller.move_left_bot()
    @threaded
    @_set_coords
    def right_bot(self):
        self.controller.move_right_bot()
    @threaded
    @_set_coords
    def left_top(self):
        self.controller.move_left_top()
    @threaded
    @_set_coords
    def right_top(self):
        self.controller.move_right_top()
    @threaded
    @_set_coords
    def zero_bot(self):
        self.controller.zero_base_model()
        self.coord["y"] = 0
    @threaded
    @_set_coords
    def zero_top(self):
        self.controller.zero_top_model()
        self.coord["x"] = 0
    @threaded
    @_set_coords
    def move_top_mm(self, event):
        val = self.text_input_top.get()
        try:
            val_int = int(val)
        except:
            print("Not Valid Integer")
        print(f"val_int is {val_int}")
        self.controller.move_top_mm(val_int)
        self.text_input_top.delete(0, tk.END)
    @threaded
    @_set_coords
    def move_bot_mm(self, event):
        val = self.text_input_bot.get()
        try:
            val_int = int(val)
        except:
            print("Not Valid Integer")
        self.controller.move_bot_mm(val_int)
        self.text_input_bot.delete(0, tk.END)
    @threaded

    def _serial_reader(self):
        """
        Necessary to empty serial
        """
        while True:
            if self.controller.top_serial_in_waiting():
                empty_ser = self.controller.top_serial_read()  # just drain it, or log it if useful
                

    def run(self):
        """
        Runs both the serial reader and the UI
        """

        self._serial_reader()
        self.check_coords()

        self.root.mainloop()
ControllerGUI().run()