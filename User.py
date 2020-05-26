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

    def createPayment(self,receiverID):
        coins=getCoins()
        amount=randint(1,len(coins)-1)
        coinsToSend=[]
        for i in range(0,amount):
            index=randint(0,len(coins)-1)
            coinsToSend.append(coins.pop(index))
        paymentCreation=Payment(coinsToSend,self.__id,receiverID)
        paymentCreation.Sign(self.__sk)



    def getCoins(blockChain):
        coins = []
        for block in blockchain.blocks:           
            transactions=block.getBlockTransactions()
            for t in transactions:
                if(isinstance(t,Payment)):
                    if(t.getSenderID()==self.__id):
                        for coin in t.getCoins():
                            coins.remove(coin)
                    if(t.getReceiverID()==self._id and t.getCoin().getCoinOwner==self.__id):
                        coins=coins+t.getCoins()
        return coins                    