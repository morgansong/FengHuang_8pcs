from smbus2 import SMBus,i2c_msg


class I2C_Handler():
    def __init__(self): 
        self.bus = SMBus(1)
        
    def write_data(self, address, value):
        # print("I2C write")
        msg = i2c_msg.write(address, value)
        self.bus.i2c_rdwr(msg)
        
    def read_numbers_bytes(self, address, num):
        # print("I2C read")
        msg = i2c_msg.read(address, num)
        self.bus.i2c_rdwr(msg)
        data = list(msg)
        return data













