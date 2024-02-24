import dynamixel_sdk as dmxl
import platform
from tqdm import tqdm

PLATFORM_SYSTEM_MAP = {
    'Windows': 'COM1',
    'Mac': '/dev/tty.usbserial-*',
    'Linux': '/dev/ttyUSB0'
}

DEVICENAME = PLATFORM_SYSTEM_MAP.get(platform.system())

def scan(devices=None):
    port_handler = dmxl.PortHandler(DEVICENAME)
    port_handler.openPort()

    device_data, device_count = {}, 0
    pbar = tqdm(total=4048, position=0, leave=True)
    for baudrate in [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000, 4500000]:
        port_handler.setBaudRate(baudrate)
        
        for protocol in [1.0, 2.0]:
            packet_handler = dmxl.PacketHandler(protocol)

            for id in range(0, 253):
                model, result, _ = packet_handler.ping(port_handler, id)

                if result == 0:
                    device_data[id] = (protocol, baudrate)
                    tqdm.write(f'Model: {model} | ID: {id} {packet_handler.getTxRxResult(result)}')

                    if devices is not None:
                        device_count += 1
                        if device_count == devices:
                            pbar.close()
                            return device_data
                pbar.update(1)
    pbar.close()
    return device_data