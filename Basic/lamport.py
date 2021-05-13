import uuid
import hashlib
CHAR_ENC = "utf-8"

def verifySignature(sig,passhash):
    '''Verify if passhash = hash(sig)'''
    #passhash = hash(password) stored in server
    #Hash - SHA256 
    temp1 = hashlib.sha256(sig.encode(CHAR_ENC)).hexdigest()
    if temp1 == passhash:
        return True
    return False

def genSalt():
    '''Generated salt for more secure hashing of passwords'''
    salt = uuid.uuid4.hex
    return salt

def genHashwithSalt(password,salt,n):
    """Generates hash of password after appending with salt at the end
       Hash = SHA256^n(password | salt) i.e. SHA256 is applied on (password|salt) n times     
    """
    assert isinstance(password,str), "Password must be a string"
    assert isinstance(salt,str), "Salt must be a string"
    assert isinstance(n,int), "Number must be an integer"
    temp = "".join(password+salt)

    for i in range(n):
        temp1 = hashlib.sha256(temp.encode(CHAR_ENC)).hexdigest()
        temp = str(temp1)
    encode = temp
    return encode
    pass

def genHash(password,n):
    """Generates hash of password without any salting
       Hash = SHA256^n(password) i.e. SHA256 is applied on (password) n times     
    """
    assert isinstance(password,str), "Password must be a string"
    assert isinstance(n,int), "Number must be an integer"
    temp = "".join(password)

    for i in range(n):
        temp1 = hashlib.sha256(temp.encode(CHAR_ENC)).hexdigest()
        temp = str(temp1)
    encode = temp
    return encode


