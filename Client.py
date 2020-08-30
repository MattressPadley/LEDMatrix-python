import os
import pickle
from socket import *

host = "10.0.5.10" # set to IP address of target computer
port = 14000
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)


while True:

    os.system('cls') 
    print('1. Pick RGB Values')
    print('2. Run Animation')
    print('3. Exit server')
    opt = input("Pick an Option:")

    if opt == '1':

        r = input('Red: ') or '0'
        b = input('Blue: ') or '0'
        g = input('Green: ') or '0'

        print(r, g, b)
        rgb = r, g, b
        data = pickle.dumps(rgb)
        
        UDPSock.sendto(data, addr)

    if opt == '2':

        data = pickle.dumps("anim")    
        UDPSock.sendto(data, addr) 

    if opt == '3':

        data = pickle.dumps("exit")    
        UDPSock.sendto(data, addr)

UDPSock.close()
os._exit(0)

