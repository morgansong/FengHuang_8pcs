from Driver_Sensors import I2C_Handler
import time

class SEN4x():
    def __init__(self):
        # print("SEN4x")
        self.address_SEN44 = 0x69
        self.My_Handler = I2C_Handler.I2C_Handler()
        
    def SEN44_SN_Read(self):
        self.My_Handler.write_data(self.address_SEN44,[0xD0, 0x33])
        time.sleep(0.02)
        Data_Get = self.read_numbers_bytes(self.address_SEN44,48)
        
        return str(Data_Get[0])+str(Data_Get[1])+str(Data_Get[3])+str(Data_Get[4])
        
    def SEN44_start_measurement(self):
        self.My_Handler.write_data(self.address_SEN44,[0x00,0x21])
        
    def SEN44_stop_measurement(self):
        self.My_Handler.write_data(self.address_SEN44,[0x01,0x04])
        
    def SEN44_ReadMeasurement(self):
        self.My_Handler.write_data(self.address_SEN44,[0x03,0x81]) #read output with Raw signal
        
        time.sleep(0.01)
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SEN44,30)
        
        pm2p5 =int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16)
        
        voc = (int(hex(Data_Get[12]<<8),16)+int(hex(Data_Get[13]),16))/10.
        
        humi = (int(hex(Data_Get[15]<<8),16)+int(hex(Data_Get[16]),16))/100.
        temp = (int(hex(Data_Get[18]<<8),16)+int(hex(Data_Get[19]),16))/200.
        
        
        voc_raw = int(hex(Data_Get[21]<<8),16)+int(hex(Data_Get[22]),16)
        
        humidity_uncomp  = (int(hex(Data_Get[24]<<8),16)+int(hex(Data_Get[25]),16))/100.
        temperature_uncomp  = (int(hex(Data_Get[27]<<8),16)+int(hex(Data_Get[28]),16))/200.
         
        
        return [round(pm2p5,2),round(voc,2),round(temp,2),round(humi,2),voc_raw,round(humidity_uncomp,2),round(temperature_uncomp,2)]
        
        # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),"SEN44 pm2p5: {},VOC: {},temperature: {}, humidity: {},VOC_Raw: {},temperature_uncomp : {}, humidity_uncomp : {}".format(round(pm2p5,2),round(voc,2),round(temp,2),round(humi,2),round(voc_raw,2),round(humidity_uncomp,2),round(temperature_uncomp,2)))















