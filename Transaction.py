from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ScroogeCoin import ScroogeCoin
from Hash import HashPointer
class Transaction():
    __id=0

    def __init__(self):
        if type(self) == Transaction:
            raise Exception("Transaction must be subclassed.")
        self.__id=Transaction.__id
        self.__signature= None
        Transaction.__id+=1
        self.__hashPointers=[]
        
   

    def __repr__(self):
        return str(self)
    
    def getTranID(self):
        return self.__id

    def Sign(self,signature): 
        self.__signature=signature
    
    def getSignature(self):
        return self.__signature
    
    def addHashPointer(self,hashPointer):
        self.__hashPointers.append(hashPointer)    
     
    def getHashPointers(self):
        return self.__hashPointers 


class coinCreation(Transaction):

    def __init__(self,coin,scroogePk):
        if(isinstance(coin,ScroogeCoin) and coin.isValid(scroogePk)):
            super(coinCreation,self).__init__() 
            self.__coin=coin
            
            
            
        else:
             raise Exception("Coin must be an instace of ScroogeCoin and Should be signed by Scrooge")

    def __str__(self):
        return "{TransType: CoinCreation, TransID: "+str(self.getTranID())+", "+" MemoryID: "+str(id(self))+", "+ str(self.getCoin())+", TransactionPointers:"+str(self.getHashPointers())+"}\n"

    def isValid(self,scroogePk):
        if(self.getSignature() == None):
            print("Transaction must be signed by scrooge")
            return False
        return Ecdsa.verify(str(self),self.getSignature(), scroogePk)
    
    def getCoin(self):
        return self.__coin

    def addTransactionHashPointer(pointer):
        self.__hashPointers.append(pointer)    

class Payment(Transaction):

    def __init__(self,coins,senderID,receiverID):
        super(Payment, self).__init__()   
        self.__senderID=senderID
        self.__receiverID=receiverID
        self.__coins=coins

    def isValid(self,senderCoins,senderPk):
        if(self.getSignature() == None):
            print("Transaction must be signed by Coin Owner")
            return False

        for coin in self.__coins:
            if(coin not in senderCoins):
                return False
        return Ecdsa.verify(str(self),self.getSignature(), senderPk)
            
    def __str__(self):
        senderID ="Scrooge" if self.__senderID==0 else str(self.__senderID)
        return "{TransType: Payment, TransID: "+str(self.getTranID())+" MemoryID: "+str(id(self)) + " ,SenderID: "+senderID+" ,ReceiverID: "+\
        str(self.__receiverID)+", Amount: "+str(len(self.__coins))+" Coins: \n"+ str(self.__coins) +", TransactionPointers: "+str(self.getHashPointers())+"}\n"
    
    def getSenderID(self):
        return self.__senderID

    def getReceiverID(self):
        return self.__receiverID    

    def getCoins(self):
        return self.__coins    

# # Generate new Keys
# privateKey = PrivateKey()
# publicKey = privateKey.publicKey()
# p2= PrivateKey()
# pk2=p2.publicKey()

# message = "My test message"

# # Generate Signature
# signature = Ecdsa.sign(message, privateKey)

# # To verify if the signature is valid
# print(Ecdsa.verify(message, signature, pk2))
# print("hi")