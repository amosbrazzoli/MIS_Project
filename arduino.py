class MIS_Arduino:
    def __init__(self, serial, baud):
        self.serial = serial
        self.baud = baud

        last_read = 0

        self.ECG = 0
        self.pressure1 = 0
        self.pressure2 = 0
        self.relay1 = None
        self.realy2 = None
        self.realy3 = None
        self.realy4 = None
        self.x = 0
        self.y = 0
        self.z = 0

    def read_update(read):
        


