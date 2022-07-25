import serial
import time
 
receiverNum = "+254723989012"
sim800l = serial.Serial(
port='/dev/serial1',
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
      
sim800l.write(str.encode("AT+CFUN=0\r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................3')

sim800l.write(str.encode('AT*MCGDEFCONT="IP","safaricom" \r\n'))
print(sim800l.readline())
print('............................4')


sim800l.write(str.encode("AT+CGCONTRDP \r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................5')


sim800l.write(str.encode("AT+CFUN=1\r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6')


sim800l.write(str.encode("AAT+COPS?\r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6.1')

sim800l.write(str.encode("AT+CSQ?\r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6.2')

sim800l.write(str.encode("AT+CGREG? \r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6.3')


sim800l.write(str.encode("AT+CGPADDR?\r\n"))
print(sim800l.readline())
time.sleep(1)
print('............................6.4')


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

