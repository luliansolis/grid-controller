# Grid Controller

The grid controller has six main files. They follow MVC (So the GUI is the V, the M are the axis, the C is the controller), just to have this slightly more ordered
### config.json:
-   This file sets a bunch of parameters. The only relevant ones for a general case are:
-   "baudrate": 9600, <- I don't know why this would be changed, but it sets the baud rate of the serial commands from the Arduino to Python
    "top_ten_steps": 336, <- It states how many "steps" are required for 10 cm in the top axis
    "bot_ten_steps": 8100, <- It states how many "steps" are required for 10 cm in the bottom axis
    "dev_id": "xi-com:///dev/ttyACM1", <- Device id of the bottom axis (In Linux the xi-com preamble is necessary, idk if it is in Windows)
    "port": "/dev/ttyACM0", <- Device id of the top axis 
### manual_controller.py: 
-   This file is used to create the GUI and send commands to the controller (Basically, the view).
-   The GUI offers: Movement of 1 cm left/right, and movement to a specific point. The movements are in mm (So 10 = 1 cm)
-   There is a dumb bug with the interface because the direction of the Arduino switched somewhere, so if one has to move to the centimeter 10, we actually
-   need to write -100.
-   There are two zero buttons. They do different things (Peak UX design). In the case of the "base," it brings the base to zero (Because the base knows exactly what the zero is), in the case of the "top" (The Arduino configurable one), it sets the zero at the point you want.
-   The GUI also tracks the coordinates, but it all depends on the specific run. If the system crashes, it doesn't have the memory from before.
-   A trick to solve the previous case is to set the coordinate of the Arduino without the motor (i.e. turn the supply off), then the system will update the coord
-   accordingly (As long as the prior knowledge of the top position is true), and everything will work. Otherwise, moving to zero is a better solution. Committing the coordinates to a file also works, but it requires changing the top axis initialiser too, and it doesn't account for slight manual changes (That is why I didn't implement it)
-   Also, if one flags in the config file "with_osc_client" to 1, then a capture button will be added. The oscilloscope client is a bit "ad-hoc," so I doubt it would be useful
-   If this view is not desirable (i.e., you want to use another way to "view" this), then it is important to either remove the serial print from the Arduino or to code a replacement to empty the Arduino serial.
### system_controller.py 
- This file is used to communicate with both axis classes and the oscilloscope (If required). 
### base_model.py: 
- This is the model for the "bottom" axis. It basically consists of binding all the commands from the lib to Python. The controller takes care of
- initialising the base and creating a queue for each command using a decorator (@queue_top_controller_feeder)
### top_model.py: 
- This is the model for the "top" axis. It binds the Arduino commands to Python. The most important detail is that I'm maintaining the state of the
- Arduino using Python instead of Arduino. The switch is completely transparent to this code; it just serves as a good place to "zero." It is also relevant
- that the top model can have a fake position if one sets the position above the maximum. This wasn't relevant to my case, so I didn't fix it, but it would
- destroy the reference. It is a matter of capping the maximum value to whatever the maximum length of the axis is (Around 146 cm).
### matlab_interface.py:
- This is replaceable, but if it is useful, it sets up a client for a Matlab server, and the capture button binds to the server action.

# Arduino File

- The Arduino file has a set of commands, but they are obviously extendable. I always move with "fast" velocity, which completely depends on the time between cycles. Python interfaces the Arduino using the commands in the "main" function.
- The level switch helps to stop the Arduino, but it is a bit buggy now. The reason is that sometimes it reactivates after release. Since I was using it manually, my personal solution was to move it 1 mm and set the zero afterwards, but setting a state associated with the interruption and creating a logic with it (i.e. If the state is true then you cannot move towards the switch, then if the state is true the interruption cannot happen when you move towards the other side, which is trivial to implement tbh) is a more fitting solution.
