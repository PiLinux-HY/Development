PWR_MGMT_1 = 0x6b
ACCL_XOUT_H = 0x3b
ACCL_XOUT_L = 0x3c
ACCL_YOUT_H = 0x3d
ACCL_YOUT_L = 0x3e
ACCL_ZOUT_H = 0x3f
ACCL_ZOUT_L = 0x40

GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48

class MPU6050:
	def _init_(self,bus,address=0x68): #객체 생성시
		self.bus = bus
		self.address = address
		self._writeByte(PWR_MGMT_1, 0x00)
	def read_gyro(self):
		GyX = self._readByte(Gyro_XOUT_H)<<8
		GyX |= self._readByte(Gyro_XOUT_L)
		GyY = self._readByte(Gyro_YOUT_H)<<8
		GyY |= self._readByte(Gyro_YOUT_L)
		GyZ = self._readByte(Gyro_ZOUT_H)<<8
		GyZ |= self._readByte(Gyro_ZOUT_L)
	

		if(GyX >=0x8000) : GyX =-((65535-GyX)+1)
		if(GyY >=0x8000) : GyY =-((65535-GyY)+1)
		if(GyZ >=0x8000) : GyZ =-((65535-GyZ)+1)
		
		return GyX,GyY,GyZ
	def read_accl(self):
		AcX = self._readByte(ACCL_XOUT_H)<<8
		AcX |= self._readByte(ACCL_XOUT_L)
		AcY = self._readByte(ACCL_YOUT_H)<<8
		AcY |= self._readByte(ACCL_YOUT_L)
		AcZ = self._readByte(ACCL_ZOUT_H)<<8
		AcZ |= self._readByte(ACCL_ZOUT_L)
		
		if(AcX >=0x8000): AcX =-((65535-AcX)+1)
		if(AcY >=0x8000): AcY =-((65535-AcY)+1)
		if(AcZ >=0x8000): AcZ =-((65535-AcZ)+1)
		
		return AcX, AcY, AcZ
def _writeByte(self, reg, value):
		self.bus.write_byte_data(self.address, reg, value)
def _readByte(self, reg):
		value = self.bus.read_byte_data(self.address, reg)
		return value


import smbus
import mpu6050

i2c_bus = smbus.SMBus(1)
mpu6050 = mpu6050.MPU6050(i2c_bus)

try:
	while True:
		GyX,_,_ = mpu6050.read_gyro()
		print("GyX = %5d" %GyX)
except KeyboardInterrupt:
	pass

i2c_bus.close()
