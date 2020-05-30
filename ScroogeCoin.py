from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
class ScroogeCoin():
    __id=0
   
    """
    constructor, with protected attributes 
    """
    def __init__(self, value,ownerID):
        self.__id=ScroogeCoin.__id
        ScroogeCoin.__id+=1
        self.__value=value
        self.__signature=None
        self.__createdAt=None
        self.__lastRef=None

 
    def getCoinOwner(self):
        return self.__owner

    def setCreatedAt(self,createdAt):
        self.__createdAt=id(createdAt)

    def getCreatedAt(self):
        return self.__createdAt       

    def setLastRef(self,ref):
        self.__lastRef=id(ref)   

    def getLastRef(self):
        return self.__lastRef 


    def getCoinID(self):
        return self.__id    

    def __str__(self):
        return str(self.__id)

    
    def __repr__(self,mode=0):
        return "CoinID: "+str(self.__id)+" CreatedAt: "+str(self.__createdAt)+" ScroogeSentItToUserAt: "+str(self.__lastRef)+"\n"  
    
    def Sign(self,signature):
        self.__signature= signature

    def isValid(self,scroogePk):
        if(self.__signature==None):
            return False
        return Ecdsa.verify(str(self),self.__signature , scroogePk)

        
