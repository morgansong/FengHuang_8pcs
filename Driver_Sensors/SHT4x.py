from Driver_Sensors import I2C_Handler
import time

class SHT4x():
    def __init__(self):
        # print("SHT4x") 
        self.address_SHT4x = 0x44
        self.My_Handler = I2C_Handler.I2C_Handler()
        
    def SHT4x_SN_Read(self):
        self.My_Handler.write_data(self.address_SHT4x,[0x89])
        time.sleep(0.02)
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SHT4x,6)
        
        return str(Data_Get[0])+str(Data_Get[1])+str(Data_Get[3])+str(Data_Get[4])
        
    def SHT4x_Read(self):
        self.My_Handler.write_data(self.address_SHT4x,[0xFD])  
        time.sleep(0.02) ###must have a delay for SHT4x
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SHT4x,6)
        
        temp =-45 + 175.0*(int(hex(Data_Get[0]<<8),16)+int(hex(Data_Get[1]),16))/65535.0 
        humi =-6 + 125.0*(int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16))/65535.0
        
        # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),"SHT4x temperature: {}, humidity: {}".format(round(temp,2),round(humi,2)))
        
        return [round(temp,2),round(humi,2)]
        
















