from Hash import hash
from Transaction import Transaction, coinCreation, Payment
from ScroogeCoin import ScroogeCoin
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
class Block():
    __id=0
    hash=None
    def __init__(self,pointer=None,previosHash=None):
        #max ten transactions
        self.__transactions=[]
        self.hashPointer=HashPointer(pointer,previosHash)
        self.__id=Block.__id
        Block.__id+=1
        self.hash=self.setBlockHash()


        
    
    def getBlockTransactions(self):
        return  self.__transactions

    def setBlockHash(self):
        return hash(self)
    
    def addTransaction(self,transaction,scroogePk):
        #check if it is instance of transaction first
        #check signature
        if(isinstance(transaction, Transaction) and len(self.__transactions)<10 and transaction.isValid(scroogePk)):
            self.__transactions.append(transaction)
            return True
        else:
            return False    

    def __str__(self):
        ##LOOP on transactions and put them in a string then append them
        return 'BlockId: '+str(self.__id)+", TransList: "+str(self.__transactions)

class HashPointer():
    def __init__(self,pointer,previosHash):
        self.pointer=pointer
        self.previosHash=previosHash
    
# x=Block()
# c=ScroogeCoin(1)
# c1=ScroogeCoin(1)
# c.Sign(scrooge.scroogeSign(str(c)))
# c1.Sign(scrooge.scroogeSign(str(c1)))

# t=coinCreation(c)
# t.Sign(scrooge.scroogeSign(str(t)))
# t1=coinCreation(c1)
# x.addTransaction(t)
# x.addTransaction(t1)

# print(x)


