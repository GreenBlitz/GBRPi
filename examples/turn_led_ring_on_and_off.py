import gbrpi
import time


def main():
    led_ring = gbrpi.LedRing(8)
    while True:
        time.sleep(5)
        led_ring.on()
        time.sleep(5)
        led_ring.off()

if __name__ == '__main__':
    main()
