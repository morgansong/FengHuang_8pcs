from Driver_Sensors import I2C_Handler
import time


class SHT3x():
    def __init__(self):
        # print("SHT4x") 
        self.address_SHT3x = 0x44
        self.My_Handler = I2C_Handler.I2C_Handler()
        
    def SHT3x_SN_Read(self):
        self.My_Handler.write_data(self.address_SHT3x,[0x37,0x80])
        time.sleep(0.02) 
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SHT3x,6)
        
        return str(Data_Get[0])+str(Data_Get[1])+str(Data_Get[3])+str(Data_Get[4])
        
    def SHT3x_Read(self):
        self.My_Handler.write_data(self.address_SHT3x,[0x2C,0x06])
        time.sleep(0.02) 
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SHT3x,6)
        
        temp =-45+175.0*(int(hex(Data_Get[0]<<8),16)+int(hex(Data_Get[1]),16))/65535.0 
        humi =100.0*(int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16))/65535.0
        
        # print(time.strftime("%Y-%m-%d,%H:%M:%S******>", time.localtime()),"SHT3x temperature: {}, humidity: {}".format(round(temp,2),round(humi,2)))
        
        return [round(temp,2),round(humi,2)]
        