import can

def listen_can_messages(interface='vcan0'):
    bus = can.interface.Bus(bustype='socketcan', channel=interface, bitrate=500000)
    print(f"Listening on {interface}...")
    while True:
        msg = bus.recv()
        if msg:
            print(f"{msg}")

if __name__ == "__main__":
    listen_can_messages('vcan0')
