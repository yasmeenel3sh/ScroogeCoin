from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from Transaction import Payment
from random import randint

class User():
    __id=1
    def __init__(self):
        self.__sk= PrivateKey()
        self.__pk= (self.__sk).publicKey()
        self.__id=User.__id
        User.__id+=1
        self.coins=[]


    def getUserPk(self):
        return self.__pk

    def getUserID(self):
        return self.__id    

    def createPayment(self,receiverID,blockChain):
        coins=self.getCoins(blockChain)
        if(len(coins)==0):
            return None
        if(len(coins)==1):
            amount=1
        elif(len(coins)>1):    
            amount=randint(1,len(coins)-1)
        coinsToSend=[]
        for i in range(0,amount):
            index=randint(0,len(coins)-1)
            coinsToSend.append(coins.pop(index))
        paymentCreation=Payment(coinsToSend,self.__id,receiverID)
        paymentCreation.Sign(Ecdsa.sign(str(paymentCreation), self.__sk))
        return paymentCreation

    def createPaymentTest(self,receiverID,blockChain):
        coins=self.getCoins(blockChain)
        if(len(coins)==0):
            return None
        amount=1
        coinsToSend=[]
        for i in range(0,amount):
            index=randint(0,len(coins)-1)
            coinsToSend.append(coins.pop(index))
        paymentCreation=Payment(coinsToSend,self.__id,receiverID)
        paymentCreation.Sign(Ecdsa.sign(str(paymentCreation), self.__sk))
        return paymentCreation

    def createPaymentTestDoubleSpend(self,receiverID,blockChain):
        coins=self.getCoins(blockChain)
        amount=1
        coinsToSend=[]
        coinsToSend.append(coins.pop(0))
        paymentCreation=Payment(coinsToSend,self.__id,receiverID)
        paymentCreation.Sign(Ecdsa.sign(str(paymentCreation), self.__sk))
        return paymentCreation

    def getCoins(self,blockChain):
        coins = []
        for block in blockChain:           
            transactions=block.getBlockTransactions()
            for t in transactions:
                if(isinstance(t,Payment)):
                    if(t.getSenderID()==self.__id):
                        for coin in t.getCoins():
                            coins.remove(coin)
                    if(t.getReceiverID()==self.__id):
                        coins=coins+t.getCoins()
        return coins

                     