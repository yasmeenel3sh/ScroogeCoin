from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ScroogeCoin import ScroogeCoin
from Transaction import coinCreation, Payment, DiscardedTransaction
from Block import Block
from User import User
from Hash import Hash, HashPointer

import binascii
class Scrooge():
    __id=0
    __Name="Scrooge"
    __users=[]
    __buffer=[]

    __coins=[]
    __blockChain=[]
    initialization=True
    text_file = open("Output.txt", "w")

    __previousHashPointer=HashPointer(None,None)
    lastHashPointer=HashPointer(None,None)
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
     
    def getBlockChain(self):
        return self.__blockChain
    
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

    def finishInitialization(self):
        print("Initialization Finished\n")
        print("AdminID: Scrooge\n AdminPublic key: "+str(binascii.hexlify(self.__pk.toString().encode('utf8')))+"\n")
        print("*******************************************************************************\n")
        print("Current Users\n")

        self.text_file.write("Initialization Finished\n")
        self.text_file.write("AdminID: Scrooge\n AdminPublic key: "+str(binascii.hexlify(self.__pk.toString().encode('utf8')))+"\n")
        self.text_file.write("************************************************************************************************************\n")
        self.text_file.write("Current Users\n")

        for user in self.__users:
            print("UserID: "+str(user.getUserID())+"\n UserPublicKey: "+str(binascii.hexlify(user.getUserPk().toString().encode('utf8')))+"\n Coins: "+repr(user.getCoins(self.__blockChain)))
            print("*******************************************************************************\n")
            self.text_file.write("UserID: "+str(user.getUserID())+"\n UserPublicKey: "+str(binascii.hexlify(user.getUserPk().toString().encode('utf8')))+"\n Coins: "+repr(user.getCoins(self.__blockChain))+"\n")
            self.text_file.write("************************************************************************************************************\n")
        print("##########################Blockchain After initialization#######################\n")
        print(repr(self.__blockChain)+"\n")
        print("__________________________________________________________________________\n")
        self.text_file.write("##########################Blockchain After initialization#######################\n")
        self.text_file.write(repr(self.__blockChain)+"\n")
        self.text_file.write("__________________________________________________________________________\n")    
        self.initialization=False
    

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
            self.addTransactionToBuffer(paymentCreation)   

    def Verify(self,transaction):
        senderID=transaction.getSenderID()
        #initialization by scrooge
        if(senderID==0):
            return True
        sender=self.getUserByID(senderID)
        senderPk=sender.getUserPk()
        #checking the coins belong to the owner
        firstCheck=transaction.isValid(sender.getCoins(self.__blockChain),senderPk)
        if(not firstCheck):
            print("Transaction Coins don't belong to sender")
            discardedTransaction=DiscardedTransaction(transaction,"Transaction Coins don't belong to sender")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
            print("Transaction discarded\n")
            print(discardedTransaction)
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n") 

            self.text_file.write("Transaction Coins don't belong to sender")
            self.text_file.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
            self.text_file.write("Transaction discarded\n")
            self.text_file.write(str(discardedTransaction))
            self.text_file.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n") 
            return False

        
        #checking in buffer
        for t in self.__buffer:
            if(isinstance(t,Payment)):
                if(t.getSenderID()==senderID):
                    tCions=t.getCoins()
                    for coin in tCions:
                        if(coin in transaction.getCoins()):
                            discardedTransaction=DiscardedTransaction(transaction,"Double Spending")
                            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
                            print("Transaction discarded\n")
                            print(discardedTransaction)
                            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n") 
                            self.text_file.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
                            self.text_file.write("Transaction discarded\n")
                            self.text_file.write(str(discardedTransaction))
                            self.text_file.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n") 
                            return False
        return True                    

    def addTransactionToBuffer(self,transaction):
        if(transaction==None):
            return   
        if(len(self.__buffer)<10):
            if(isinstance(transaction,coinCreation)):
                if(transaction.isValid(self.__pk)):
                    self.__buffer.append(transaction)
                    transaction.addHashPointer(None)
                    transaction.getCoin().setCreatedAt(transaction)
                    transaction.getCoin().setLastRef(transaction)
            elif(isinstance(transaction,Payment)):
                if(self.initialization==False):
                    print("***********************Processing Transaction***********************\n")
                    self.text_file.write("***********************Processing Transaction***********************\n")
                if(self.Verify(transaction)):
                    coins=transaction.getCoins()
                    for coin in coins:
                        transaction.addHashPointer(coin.getLastRef())
                        coin.setLastRef(transaction)                       
                    self.__buffer.append(transaction)
                    if(self.initialization==False):
                        print(repr(transaction))
                        print("Transaction Added Successfully \n")
                        print("**********************************************************************\n")
                        print("###############################Current Block Under Construction######################################### \n")
                        self.text_file.write(repr(transaction))
                        self.text_file.write("Transaction Added Successfully \n")
                        self.text_file.write("**********************************************************************\n")
                        self.text_file.write("###############################Current Block Under Construction######################################### \n")
                        for t in self.__buffer:
                            print("Transaction ID: "+str(t.getTranID())+"\n")
                            print("Transaction MemoryID: "+str(id(t))+"\n")
                            print("___________________________________________ \n")  
                            self.text_file.write("Transaction ID: "+str(t.getTranID())+"\n")
                            self.text_file.write("Transaction MemoryID: "+str(id(t))+"\n")
                            self.text_file.write("___________________________________________ \n")                   
                
                               
        else:
            raise Exception("Buffer limit exceeded")
        if(len(self.__buffer)==10):
            #create and public block with pointers and so on and publish it on the blockchain
            self.createBlock(self.__buffer)
            
            self.__buffer=[]
            if(self.initialization==False):
                
                print("Block added to Chain\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                print("Current Blockchain\n")
                self.text_file.write("Block added to Chain\n")
                self.text_file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.text_file.write("Current Blockchain\n")
                print(repr(self.__blockChain)+"\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.text_file.write(repr(self.__blockChain)+"\n")
                self.text_file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")  

              

    def createBlock(self,buffer):
        self.__previousHashPointer=self.lastHashPointer
        if(len(self.__blockChain)==0):
            block=Block(None,None)
        else:
            block=Block(self.__previousHashPointer.pointer,self.__previousHashPointer.previousHash) 
        
        block.addTransactions(buffer)
        block.setBlockHash()
        self.lastHashPointer=HashPointer(block,Hash(block)) 
        #signing
        self.lastHashPointer.Sign(self.scroogeSign(str(self.lastHashPointer)))
        self.__blockChain.append(block)  
        
    def printBlockChain(self):
        # print(self.__blockChain)
        # print(colored("Block under construction\n","green"))
        # print(colored(self.__buffer,"green"))

        self.text_file.close()


