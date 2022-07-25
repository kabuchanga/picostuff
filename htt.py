"""
Raspberry Pi Pico (MicroPython) exercise:
work with SIM800C UART Module
"""
from machine import Pin, ADC 
import os
import utime
import binascii
#import ujson

#print sys info
print(os.uname())

#using pin defined
ADC0= ADC(Pin(26))
sensor_temp = ADC(4)
led_pin =25  #onboard led
pwr_en = 14  #pin to control the power of sim7020x
uart_port = 0
uart_baute = 9600

APN = "safaricom"

i=0
reading=0
temperature=0

#indicate program started visually
led_onboard = machine.Pin(led_pin, machine.Pin.OUT)

def led_blink():
    led_onboard.value(1)
    utime.sleep(0.5)
    led_onboard.value(0)
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(0.5)
    led_onboard.value(0)

def hexStr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

#power on the sim800c
def powerOn(pwr_en):
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
    pwr_key.value(1)
"""
    pwr_key.value(0)
    utime.sleep(1)
    pwr_key.value(1)
    utime.sleep(5)
"""

def ADC_temp():
    global reading
    global temperature
    reading = ADC0.read_u16()*33/65535
    print("ADC0 voltage = {0:.2f}V \r\n".format(reading))
    print(str(temperature))
    if temperature > 25:
        led_blink()
    reading = sensor_temp.read_u16()*3.3/65535
    temperature = 27 - (reading - 0.706)/0.001721
    print("temperature = {0:.2f}℃ \r\n".format(temperature))

#power down the sim800c
def powerDown(pwr_en):
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
    pwr_key.value(0)

#2 sec timeout is arbitrarily chosen
def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write((cmd).encode())
    waitResp(timeout)
    print()
    
def waitResp(timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print((resp).decode())

def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write((cmd+'\r\n').encode())
    waitRespLine(timeout)
    print()
    
def waitRespLine(timeout=2000):
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            print((uart.readline()).decode())
            
#APN Manual configuration
def apnConfig(APN):
    sendCMD_waitResp("AT+CFUN=0")        #Disable RF
    sendCMD_waitResp("AT*MCGDEFCONT=\"IP\",\""+ APN +"\"")        #Set the APN manually
    sendCMD_waitResp("AT+CFUN=1")        #Enable RF
    utime.sleep(1)
    sendCMD_waitResp("AT+CGATT?")        #Inquiry PS service
    sendCMD_waitResp("AT+CGCONTRDP")      #Attached PS domain and got IP address automatically
    sendCMD_waitResp("AT+CSQ")          #received signal strength
    print("Done APN config............................................")
    
#AT commands test
def atCommandTest():
    sendCMD_waitResp("AT")
    sendCMD_waitResp("ATE1")
    sendCMD_waitResp("AT+CGMM")
    sendCMD_waitResp("AT+CPIN?")        #whether some password is required or not
    sendCMD_waitResp("AT+CSQ")          #received signal strength
    sendCMD_waitResp("AT+CGREG?")        #the registration of the ME.
    sendCMD_waitResp("AT+CGATT?")       #GPRS Service’s status
    sendCMD_waitResp("AT+CGACT?")       #PDN active status
    sendCMD_waitResp("AT+COPS?")       #Query Network information
    sendCMD_waitResp("AT+CGCONTRDP")       #Attached PS domain and got IP address automatically

# HTTP GET TEST
def httpGetTest():
    '''
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://api.seniverse.com\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,0,\"/v3/weather/now.json?key=SwwwfskBjB6fHVRon&location=shenzhen&language=en&unit=c\"")  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance
    '''
    
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://api.plos.org\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,0,\"/search?q=title:%22Drosophila%22%20and%20body:%22RNA%22&fl=id,abstract\"")  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance


# HTTP POST TEST
def httpPostTest():
    global i
    i=i+1
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://pico.wiki/post-data.php\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,1,\"/post-data.php\",4163636570743a202a2f2a0d0a436f6e6e656374696f6e3a204b6565702d416c6976650d0a557365722d4167656e743a2053494d434f4d5f4d4f44554c450d0a,\"application/x-www-form-urlencoded\","+str_to_hexStr("api_key=tPmAT5Ab3j888&value1="+str(temperature)+"&value2="+str(reading)+"&value3="+str(i)))  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance
    
def smsTest():
    sendCMD_waitResp("AT")
    sendCMD_waitResp("ATE1")
    sendCMD_waitResp("AT+CGMM")
    sendCMD_waitResp("AT+CPIN?")        #whether some password is required or not
    sendCMD_waitResp("AT+CSQ")          #received signal strength
    sendCMD_waitResp("AT+CGREG?")        #the registration of the ME.
    sendCMD_waitResp("AT+CGATT?")       #GPRS Service’s status
    sendCMD_waitResp("AT+CGACT?")       #PDN active status
    sendCMD_waitResp("AT+COPS?")       #Query Network information
    sendCMD_waitResp("AT+CGCONTRDP")       #Attached PS domain and got IP address automatically
    
    
    sendCMD_waitRespLine('AT+CMGF=1') #socket_id = 0,connect TCP server   
    sendCMD_waitRespLine('AT+CMGS="0723989012"')
    sendCMD_waitRespLine('AT+CMGS="+254723989012" Hellow world')
    
    sendCMD_waitRespLine('Hellow world sim7020E sms')
    #sendCMD_waitResp(chr(26))
    waitResp()
    
def engineerTest():
    utime.sleep(5)
    sendCMD_waitResp("AT+CPIN?\r")
    sendCMD_waitResp("AT+CFUN=0\r")        #Disable RF
    sendCMD_waitResp("AT*MCGDEFCONT=\"IP\",\""+ APN +"\"\r")        #Set the APN manually       
    sendCMD_waitResp("AT+CGCONTRDP\r")   
    sendCMD_waitResp("AT+CFUN=1\r")        #Enable RF
    sendCMD_waitResp("AT+CSMP=17,167,0,0\r")
    sendCMD_waitRespLine('AT+CSCA="+254722500029"\r') #mesaging service center no.
    sendCMD_waitResp("AT+GMI\r")
    sendCMD_waitResp("AT+CGMM\r")
    sendCMD_waitResp("AT+CGMR\r")
    sendCMD_waitResp("AT+CGSN\r")
    sendCMD_waitResp("AT+CMGF?")
    sendCMD_waitResp("AT+CGPADDR\r")   #e IP address of the Mobile WAN interface
    sendCMD_waitResp("AT+CBAND?\r")       #Query Network information
    #utime.sleep(20)
    sendCMD_waitResp("AT+COPS?\r")       #Query Network information
    sendCMD_waitResp("AT+CSQ\r")          
    sendCMD_waitResp("AT+CGREG?\r")
    sendCMD_waitResp("AT+CFUN?\r")    
    
    sendCMD_waitResp('AT+CMGR=1\r') #read message 
    
    sendCMD_waitRespLine('AT+CMGF=1\r') #socket_id = 0,connect TCP server AT+CNMP=2
    
    sendCMD_waitRespLine('AT+CMGS="+254723989012"')   
    sendCMD_waitRespLine('This is my SMS message')    
    sendCMD_waitRespLine('^Z')
    
    
    
    #sendCMD_waitResp("AT+CNMP?")        
    
   
    
            
#print uart info
uart = machine.UART(uart_port, uart_baute, bits=8, parity=None, stop=1)
print(uart)

#power on the board
powerOn(pwr_en)

#clear bufer in UART
waitResp()

#AT commands test
#atCommandTest()

#APN Manual configuration
#apnConfig(APN)

#smsTest()
engineerTest()


'''
while True:
    # HTTP GET TEST ,for more: SIM7020_HTTP(S)_Application Note.pdf
    #httpGetTest()

    # HTTP POST TEST ,for more: SIM7020_HTTP(S)_Application Note.pdf
    #ADC_temp()
    httpPostTest()    
    utime.sleep(1)
    #led_blink()
'''    

#print(hexStr_to_str("7b22726573756c7473223a5b7b226c6f636174696f6e223a7b226964223a2257533130373330454d384556222c226e616d65223a225368656e7a68656e222c22636f756e747279223a22434e222c2270617468223a225368656e7a68656e2c5368656e7a68656e2c4775616e67646f6e672c4368696e61222c2274696d657a6f6e65223a22417369612f5368616e67686169222c2274696d657a6f6e655f6f6666736574223a222b30383a3030227d2c226e6f77223a7b2274657874223a22436c6f756479222c22636f6465223a2234222c2274656d7065726174757265223a223235227d2c226c6173745f757064617465223a22323032312d30332d31335431353a32303a30302b30383a3030227d5d7d"))
#print(str_to_hexStr("api_key=tPmAT5Ab3j888&value1=26.44&value2=57.16&value3=1002.95"))

powerDown(pwr_en)
print("Power off")



