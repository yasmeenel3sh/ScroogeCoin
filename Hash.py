from hashlib import sha256

def hash(obj):
    return sha256(str(obj).encode('utf-8')).hexdigest()

