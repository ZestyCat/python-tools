# -*- coding: utf-8 -*-

'''
Repeatedly sends AK commands to instruments through HyperTerminal.

Instructions:
    Run the program from Spyder or your preferred Python environment.
    Write the commands to send into the COMMAND variable in 1D list form ['cmd1', 'cmd2' ... 'cmdn']
    Write the sampling rate into the Sample_rate_s variable
    Run the program
    Place cursor in HyperTerminal
    Press enter to start sending the command
    Press esc to quit the program
'''

'''User input'''

COMMAND = [' AKON K0', ' ASYZ K0'] # List of commands to send
Sample_rate_s = 1 # Sample rate in seconds

'''End user input'''

from pynput.keyboard import Key, Controller, Listener
import threading
import time

kb = Controller()

def send_command(cmd):
    for c in cmd:
        with kb.pressed(Key.ctrl):
            kb.press('b')
            kb.release('b')
            
        kb.type(c)
        
        with kb.pressed(Key.ctrl):
            kb.press('c')
            kb.release('c')
            
        time.sleep(Sample_rate_s/len(COMMAND))
    
def sending():
    while run:
        send_command(COMMAND)
        print('sending...')
    
def on_press(key):
    global stop
    global run    
    t = threading.Thread(target=sending)
   
    if key == Key.enter:
        run = True
        t.start()
        
def stop(key):
    global run 
    if key == Key.esc:
        run = False
        return False
    
def execute():
    with Listener(
            on_press=on_press,
            on_release=stop) as listener:
        listener.join()

execute()

