
import serial
import threading
import re
import time
import struct


class Evo_60m(object):

	def __init__(self):
			self.portname = "/dev/ttyUSB0"  # To be adapted if using UART backboard
			self.baudrate = 115200  # 3000000 for UART backboard

		# Configure the serial connections (the parameters differs on the device you are connecting to)
			self.port = serial.Serial(
        	port=self.portname,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )

			self.port.isOpen()
			self.serial_lock = threading.Lock()

	def send_command(self, command):

		##command = "\x00\x11\x01\x45" ##text formatna
        	with self.serial_lock:# This avoid concurrent writes/reads of serial
				self.port.flushInput()
				self.port.write(command) #
				self.port.flushOutput()

	def start_sensor(self):
		if self.send_command("\x00\x11\x02\x4C"):
			print "Sensor started successfully"

	#def text_sensor(self):
    #    	if self.send_command("\x00\x11\x01\x45"):
	#		print "Sensor in text mode successfully"




	def get_mesafe(self):
			while(1):
				with self.serial_lock:
					byte = self.port.read(4)
				testBytes = struct.unpack('>BBBB', byte)
				#time.sleep(0.02)

				if (1!=0):  #testBytes[0] == 84
					crc = testBytes[0] + testBytes[1] + testBytes[2]
					actualcrc = testBytes[3]
					##mesafe = testBytes[1]*256 + testBytes[2]
					##print mesafe
					if (1!=0):  #crc == actualcrc
						##mesafe datasi mm cinsinden
						mesafe = testBytes[1]*256 + testBytes[2] #distance is mesafe
						print mesafe
			return mesafe
	def run(self):
		#print "mesafe"
		self.port.flushInput()
		self.start_sensor()
		#self.get_mesafe()


if __name__ == '__main__':
	evo_60m = Evo_60m()
	evo_60m.run()
	#print "mesafe"
	x = evo_60m.get_mesafe() #you can use x as returned distance
	while(1):
		print x
