from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ScroogeCoin import ScroogeCoin
from Transaction import coinCreation, Payment
from Block import Block
from User import User
from Hash import Hash, HashPointer
class Scrooge():
    __id=0
    __Name="Scrooge"
    __users=[]
    __buffer=[]
    __coins=[]
    __blockChain=[]

    __previousHashPointer=None
    lastHashPointer=None
    def __init__(self):
        self.__coins=[]
        self.__sk= PrivateKey()
        self.__pk= (self.__sk).publicKey()
        self.__id=Scrooge.__id
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

    def addUser(self):
        self.__users.append(User())    

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
        self.__coins.append(coin)

    #only used by scrooge to make payment at the beginning of starting the blockChain
    def createPayment(self,receiverID,amount):
        coinsToSend=[]
        if(amount <= len(self.__coins)):
            for i in range(0,amount):
                coinsToSend.append(self.__coins.pop(0))
        else:
             raise Exception("Not enough coins scrooge")

        if(len(coinsToSend)>0):
            paymentCreation=Payment(coinsToSend,self.__id,receiverID)
            paymentCreation.Sign(self.__sk) 
            print(paymentCreation.getReceiverID())
            self.addTransactionToBuffer(paymentCreation)   

    def Verify(self,transaction):
        senderID=transaction.getSenderID()
        #initialization by scrooge
        if(senderID==0):
            return True
        sender=self.getUserByID(senderID)
        senderPk=sender.getUserPk()
        firstCheck=transaction.isValid(sender.getCoins(self.__blockChain),senderPk)
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
        if(len(self.__buffer)==10):
            #create and public block with pointers and so on and publish it on the blockchain
            self.createBlock(self.__buffer)
            
            self.__buffer=[]
            print("Block added to Chain")            

    def createBlock(self,buffer):
        self.__previousHashPointer=self.lastHashPointer
        if(len(self.__blockChain)==0):
            block=Block(None,None)
        else:
            block=Block(self.__previousHashPointer.pointer,self.__previousHashPointer.previousHash) 

        block.addTransactions(buffer)
        self.lastHashPointer=HashPointer(block,Hash(block)) 
        #signing
        self.lastHashPointer.Sign(self.scroogeSign(str(self.lastHashPointer)))
        self.__blockChain.append(block)  
        
    def printBlockChain(self):
        print(len(self.__blockChain))
        print(self.__blockChain)
        print("Block under construction\n")
        print(self.__buffer)




scrooge =Scrooge()