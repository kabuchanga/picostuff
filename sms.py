import serial
import time
 
receiverNum = "+254723989012"
sim800l = serial.Serial(
port='/dev/serial0',
baudrate = 115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
APN = "safaricom"
 
sms = "Hello World my first serial sms\r\n"
time.sleep(1)
sim800l.write(str.encode('AT\r\n'))
print(sim800l.readline())
print('............................1')



sim800l.write(str.encode('AT+CPIN?\r\n'))
print(sim800l.readline())
time.sleep(1)
print('............................2')

sim800l.write(str.encode("AT+CGREG? \r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6.3')
      

sim800l.write(str.encode('AT+CMGF=1\r\n'))
print(sim800l.readline())
time.sleep(1)
print('............................2')
      

cmd1 = 'AT+CMGS="+254723989012" \r\n'
sim800l.write(str.encode((cmd1)))
print(sim800l.readline())
time.sleep(1)
print('............................7')



sim800l.write(str.encode(sms))
print(sim800l.readline())
time.sleep(1)
print('............................8')

sim800l.write(str.encode("\x1A \r\n"))
print(sim800l.readline())
time.sleep(1)
