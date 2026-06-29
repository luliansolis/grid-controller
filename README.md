# Grid Controller

The grid controller has six main files
### config.json:
-   This file sets a bunch of parameters. The only relevant ones for a general case are:
-   "baudrate": 9600, <- I don't know why this would be changed, but it sets the baudrate from the Arduino to Python
    "top_ten_steps": 336, <- It states how many "steps" are required for 10 cm in the top axis
    "bot_ten_steps": 8100, <- It states how many "steps" are required for 10 cm in the bottom axis
    "dev_id": "xi-com:///dev/ttyACM1", <- Device id of the bottom axis (In Linux the xi-com preamble is necessary, idk if it is in Windows)
    "port": "/dev/ttyACM0", <- Device id of the top axis 
### manual_controller.py: 
-   This file is used to create the GUI and send commands to the controller (Basically, the view).
-   The GUI offers: Movement of 1 cm left/right, and movement to a specific point. The movements are in mm (So 10 = 1 cm)
-   There is a dumb bug with the interface because the direction of the Arduino switched somewhere, so if one has to move to the centimeter 10, we actually
-   need to write -100.
-   There are two zero buttons. They do different things. In the case of the "base," it brings the base to zero (Because the base knows exactly what the zero is),
-   in the case of the "top" (The Arduino configurable one), it sets the zero at the point you want.
-   The GUI also tracks the coordinates, but it all depends on the specific run. If the system crashes, it doesn't have the memory from before.
-   A trick to solve the previous case is to set the coordinate of the Arduino without the motor (i.e. turn the supply off), then the system will update the coord
-   accordingly, and everything will work. Committing the coordinates to a file also works, but it requires changing the top axis initialiser too.
-   Also, if one flags in the config file "with_osc_client", then a capture button. The oscilloscope client is a bit "ad-hoc," so I doubt it would be useful
### system_controller.py 
- This file is used to communicate with both axis classes and the oscilloscope (If required). 
### base_model.py: 
- This is the model for the "bottom" axis. It consists of basically binding all the commands from the lib to python. The controller takes care of
- initialising the base and creating a queue for each command using a decorator (@queue_top_controller_feeder)
### top_model.py: 
- This is the model for the "top" axis. It binds the Arduino commands to Python. The most important detail is that I'm maintaining the state of the
- Arduino using Python instead of Arduino. The switch is completely transparent to this code; it just serves as a good place to "zero." It is also relevant
- that the top model can have a fake position if one sets the position above the maximum. This wasn't relevant to my case, so I didn't fix it, but it would
- destroy the reference. It is matter of capping the maximum value to whatever the maximum length of the axis is (Around 146 cm).
### matlab_interface.py:
- This is replaceable, but if it is useful, it sets up a client for a Matlab server, and the capture button binds to the server action.
