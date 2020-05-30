from Hash import Hash, HashPointer
from Transaction import Transaction, coinCreation, Payment
from ScroogeCoin import ScroogeCoin
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
class Block():
    __id=0
    hash=None
    def __init__(self,pointer,previosHash):
        #max ten transactions
        self.__transactions=[]
        self.hashPointer=HashPointer(pointer,previosHash)
        self.__id=Block.__id
        Block.__id+=1
        self.hash=None
        

    def __repr__(self):
        return 'BlockId: '+str(self.__id)+"\n, MemoryID: "+str(id(self))+"\nBlockHash: "+str(self.hash)+"\n BlockHashPointer: "+str(self.hashPointer)+"\n"     
    
    def getBlockTransactions(self):
        return  self.__transactions

    def setBlockHash(self):
        self.hash=Hash(self)
    
    def addTransactions(self,transactions):
        if(all(isinstance(t, Transaction) for t in transactions )):
            self.__transactions=transactions
            return True
        else:
            return False    

    def __str__(self):
        ##LOOP on transactions and put them in a string then append them
        return 'BlockId: '+str(self.__id)+", TransList: "+str(self.__transactions)
    
    def isValid(self,scroogePk):
        return (Hash(self) == self.hash) and (Hash(pointer)==self.hashPointer.previosHash) 

   
        # return 'BlockId: '+str(self.__id)+"\n, MemoryID: "+str(id(self))+",\n TransList:\n "+repr(self.__transactions)+"\n"+"BlockHash: "+str(self.hash)+"\n BlockHashPointer: "+str(self.hashPointer)+"\n"\
        # +"Transactions that were discarded while creating this block: \n"+repr(self.__discardedTransactions)+"\n

 

    


