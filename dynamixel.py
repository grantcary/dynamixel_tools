import dynamixel_sdk as dmxl
from utils import DEVICENAME

PROTOCOL_VERSION = 2.0
BAUDRATE = 57600

# XL430-W250-T
MODEL = 0
FIRMWARE_VERSION = 6
SHUTDOWN = 63
TORQUE_ENABLE = 64
LED = 65
GOAL_POSITION = 116

class DMXL:
    def __init__(self, id, protocol_version=PROTOCOL_VERSION, baudrate=BAUDRATE):
        self.id = id
        self.protocol_version = protocol_version
        self.baudrate = baudrate

    @classmethod
    def connect(cls, baudrate=BAUDRATE, protocol_version=PROTOCOL_VERSION):
        cls.port_handler = dmxl.PortHandler(DEVICENAME)
        cls.port_handler.openPort()
        cls.port_handler.setBaudRate(baudrate)
        cls.packet_handler = dmxl.PacketHandler(protocol_version)

    def getModel(self):
        return DMXL.packet_handler.read2ByteTxRx(DMXL.port_handler, self.id, MODEL)[0]

    def getFirmwareVersion(self):
        return DMXL.packet_handler.read2ByteTxRx(DMXL.port_handler, self.id, FIRMWARE_VERSION)[0]
    
    def torque(self, toggle=True, readout=False):
        result, error = DMXL.packet_handler.write2ByteTxRx(DMXL.port_handler, self.id, TORQUE_ENABLE, toggle)
        if readout: self.printErrors(result, error)

    def LED(self, toggle=True, readout=False):
        result, error = DMXL.packet_handler.write2ByteTxRx(DMXL.port_handler, self.id, LED, toggle)
        if readout: self.printErrors(result, error)

    def setGoalPosition(self, goal, readout=False):
        result, error = DMXL.packet_handler.write4ByteTxRx(DMXL.port_handler, self.id, GOAL_POSITION, goal)
        if readout: self.printErrors(result, error)
    
    def printErrors(self, result, error):
        result = DMXL.packet_handler.getTxRxResult(result)
        error = DMXL.packet_handler.getRxPacketError(error)
        print(f'{result} | {error}')