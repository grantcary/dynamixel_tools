from dynamixel import DMXL

DMXL.connect()
servo1 = DMXL(1)
servo2 = DMXL(2)

servo1.torque()
servo2.torque()

servo1.setGoalPosition(0)
servo2.setGoalPosition(0)