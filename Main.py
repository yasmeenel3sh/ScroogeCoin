from pynput import keyboard
from Scrooge import Scrooge
import time
from random import randint



if __name__ == "__main__":

    scrooge =Scrooge()
    print("Starting Initialization Phase, please wait...")
    for i in range(0,1000):
        scrooge.createCoin()
    users=scrooge.getUsers()    
    for i in range(0,100):
        scrooge.addUser()
        scrooge.createPayment(users[i].getUserID(),10)
    scrooge.finishInitialization()

terminate = False
def on_press(key):
    global terminate
    if key == keyboard.Key.space:
        print ('Program Terminating')

        scrooge.printBlockChain()
        terminate = True
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while terminate == False:
        senderIndex=randint(0,99)
        receiverIndex=randint(0,99)
        transaction=users[senderIndex].createPayment(users[receiverIndex].getUserID(),scrooge.getBlockChain())
        scrooge.addTransactionToBuffer(transaction)
        time.sleep(0.1) 
    listener.join()
    