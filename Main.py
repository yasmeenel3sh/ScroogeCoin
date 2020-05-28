from pynput import keyboard
from Scrooge import Scrooge
import time



if __name__ == "__main__":
    scrooge =Scrooge()
    for i in range(0,100):
        scrooge.createCoin()
    users=scrooge.getUsers()    
    for i in range(0,10):
        scrooge.addUser()
        scrooge.createPayment(users[i].getUserID(),10)
    for i in range(0,10):
        print(users[i].getCoins(scrooge.getBlockChain()))

terminate = False
def on_press(key):
    global terminate
    if key == keyboard.Key.space:
        print ('Program Terminating')
        #scrooge.printBlockChain()
        terminate = True
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while terminate == False:
        print ('program running')

        time.sleep(0.5) 
    listener.join()
    