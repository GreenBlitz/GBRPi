from smbus2 import SMBus


def check_request(dist, angle):
    bus = SMBus(1)
    b = bus.read_byte_data(1, 0)
    bus.close()
    if b == 1:
        send_target(dist, angle)


def send_target(dist, angle):
    data = bytearray(dist)
    data2 = bytearray(angle)
    data.append(data2)
    bus = SMBus(1)
    bus.write_i2c_block_data(2, 0, data)

