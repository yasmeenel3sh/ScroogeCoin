from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ScroogeCoin import ScroogeCoin
from Transaction import coinCreation
from User import User
class Scrooge():
    __id=0
    __users=[]
    __buffer=[]
    __coins=[]
    def __init__(self):
        self.__coins=[]
        self.__sk= PrivateKey()
        self.__pk= (self.__sk).publicKey()
        if(Scrooge.__id != 0):
             raise Exception("Only one Scrooge Entity should be created")
        Scrooge.__id+=1

    def getScroogePk(self):
        return self.__pk

    def getScroogeID(self):
        return self.__id

    ##make it private
    def scroogeSign(self,msg):
        return Ecdsa.sign(msg, self.__sk)

    def getUsers(self):
        return self.__users

    def getUserByID(self,userID):
        for user in self.__users:
            if(user.getUserID()==userID):
                return user


    def printBuffer(self):
        print(self.__buffer)

    def createCoin(self):
        coin=ScroogeCoin(1,self.__id)
        coin.Sign(self.scroogeSign(str(coin)))
        creationTransaction=coinCreation(coin,self.__pk)
        creationTransaction.Sign(self.scroogeSign(str(creationTransaction)))
        self.addTransactionToBuffer(creationTransaction)

    def Verify(self,transaction):
        senderID=transaction.getSenderID()
        sender=self.getUserByID(senderID)
        senderPk=sender.getUserPk()
        firstCheck=transaction.isValid(sender.getCoins(),senderPk)
        if(firstCheck):
            #checking in buffer
            for t in self.__buffer:
                if(isinstance(t,Payment)):
                    if(t.getSenderID==senderID):
                        tCions=t.getCoins()
                        for coin in tCions:
                            if(coin in transaction.getCoins()):
                                return false
            return true                     
        else:
            return false    



    def addTransactionToBuffer(self,transaction):
        if(len(self.__buffer)==10):
            #create and public block with pointers and so on and publish it on the blockchain
            print(self.__buffer)
            self.__buffer=[]
            print("Block added to Chain")
        if(len(self.__buffer)<10):
            if(isinstance(transaction,coinCreation)):
                if(transaction.isValid(self.__pk)):
                    self.__buffer.append(transaction)
            elif(isinstance(transaction,Payment)):
                if(self.Verify(transaction)):
                    self.__buffer.append(transaction)
                else:
                    print("Transaction discarded")            
        else:
            raise Exception("Buffer limit exceeded")





scrooge =Scrooge()