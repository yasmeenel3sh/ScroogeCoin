from hashlib import sha256

def Hash(obj):
    return sha256(str(obj).encode('utf-8')).hexdigest()

class HashPointer():
    def __init__(self,pointer,previosHash):
        self.pointer=pointer
        self.previousHash=previosHash
        self.signature=None
    def Sign(self,signature):
        self.signature=signature
    def __str__(self):
        pointer= "None" if(self.pointer== None) else str(id(self.pointer))
        return "(Pointer: "+pointer+", Previous Hash: "+str(self.previousHash)+")\n"  