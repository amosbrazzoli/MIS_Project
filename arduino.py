class MIS_Arduino:
    def __init__(self, serial, baud):
        self.serial = serial
        self.baud = baud

        self.last_read = 0

        self.ECG = 0

        self.pressure1 = 0
        self.pressure2 = 0

        self.x = 0
        self.y = 0
        self.z = 0

        self.relays = {}

    def read_update(self, read):
        try:
            self.last_read = read["time"]
            self.ECG = read["ECG"]
            self.pressure1 = read["pressure1"]
            self.pressure2 = read["pressure2"]
            self.x = read["x"]
            self.y = read["y"]
            self.z = read["z"]
        except:
            print("ARDUINO INVALID READ: ", read)

    def write_update(self, write):
        self.realys[write["fan"][0]] = write["fan"][1]

    def command(self, json_dict):
        try:
            pin, state = json_dict["fan"]
            self.relays[pin] = state
        except Exception as e:
            print(e)
            print("ARDUINO INVALID COMMAND: ", json_dict)
            return False


    def state_dict(self):
        out_dict = self.__dict__
        return out_dict


if __name__ == "__main__":
    arduino = MIS_Arduino("/dev/ttyACM0", 11520)

    print(arduino.state_dict())

