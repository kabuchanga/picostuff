import serial
import RPi.GPIO as GPIO     
import os, time

GPIO.setmode(GPIO.BOARD)   

# Enable Serial Communication
port = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write(str.encode('AT \r\n'))
rcv = port.read(10)
print(rcv)
time.sleep(1)


port.write(str.encode("AT+CGREG? \r\n"))
print(port.readline())
time.sleep(1)

port.write(str.encode('AT+CMGF=1\r\n'))  # Select Message format as Text mode
rcv = port.read(10)
print(rcv)
time.sleep(1)

# Sending a message to a particular Number

port.write(str.encode('AT+CMGS="+25472989012"\r\n'))
rcv = port.read(10)
print(rcv)
time.sleep(1)

port.write(str.encode('Hello User\r\n'))  # Message
rcv = port.read(10)
print(rcv)

port.write(str.encode("\x1A\r\n")) # Enable to send SMS
'''
for i in range(10):
    rcv = port.read(10)
    print(rcv)
'''    