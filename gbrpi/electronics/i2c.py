from smbus2 import SMBus
import time
def check_request(dist, angle):
    bus = SMBus(1)
    b = bus.read_byte_data(1, 0)
    bus.close()
    if b == 1:
        send_target(dist, angle)
    else:
        return(1)

def send_target(dist, angle):
    data = bytearray(dist)
    data2 = bytearray(angle)
    data.append(data2)
    bus = SMBus(1)
    bus.write_i2c_block_data(2, 0, data)

def main():
    dist = 22.2
    angle = 187
    z = 1
    while True:
        if check_request(dist,angle) != 1:
            break
        z =+ 1
        time.sleep(0.01)
        if z == 10000:
            break