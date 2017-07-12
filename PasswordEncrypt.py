from EntryClass import *
import random
import math

def stringToBitList(message):
    """bitList = []
    for character in message:
        b = bin(ord(character))[2:] # don't include the first two characters because they will contain 0b, not the actual value
        b = '00000000'[len(b)]+b
        for bit in b:
            bitList.append(int(bit))
    return bitList """
    total = []
    for character in message:
        c = ord(character)
        indiv = []
        #if c == 0:
        #    return [0]
        while c > 0:
            indiv = [(c % 2)] + indiv
            c = c / 2
        indiv = padBits(indiv,8)
        total = total + indiv
    return total


    def charToBit(c):
        return padBits(convertToBits(ord(c)), ASCII_BITS)
    return [b for group in
            map(charToBit, message)
            for b in group]

def bitListToInt(bitList):
    return int(''.join([('0','1')[e] for e in bitList]),2)

def stringToInt(message):
    """Wrapper function for above two funtions to convert a string to a base 10 integer based on the ASCII values of its characters"""
    return bitListToInt(stringToBitList(message))

def binstringToBitList(binstring): 
    bitList = []
    for bit in binstring:
        bitList.append(int(bit))
    return bitList

def padBits(bits, padding):
    return [0] * (padding-len(bits)) + bits

def bitsToString(paddedBitSeq):
    charBuilder = ''
    for segment in range(0,len(paddedBitSeq),8): # count by 8's because each padded bit sequence is 8 bits long
        charBuilder = charBuilder + bitsToChar(paddedBitSeq[segment: segment+8]) # concatenate each new char onto the built up string
    return charBuilder

def bitsToChar(bitSeq):
    """Convert each 8 bit length padded bit sequences back to a char based on its ASCII value"""
    value = 0
    for bit in bitSeq:
        value = (value * 2) + bit # This for loop will determine the numeric value of the binary bit sequence input
    return chr(value)

def intToString(integer):
    """Wrapper function for above four funtions to convert an integer of base 10 to a string based on the ASCII values of its characters"""
    binary = bin(integer)[2:]
    bitSeq = binstringToBitList(binary)
    return bitsToString(padBits(bitSeq,(len(bitSeq)+(8-(len(bitSeq)%8)))))

def extendedGCD(a, b):
    """return gcd,x and y so that a*x+b*y = gcd(x,y)"""
    if a == 0:
        return (b,0,1)
    else:
        gcd, x, y = extendedGCD(b%a,a)
        return (gcd, y-(b/a)*x, x)

def modularInverse(a,mod):
    gcd,x,y = extendedGCD(a,mod)
    if gcd != 1:
        raise ValueError
    return x%mod

def isPrime(num):
    smallPrimes = []
    # Two basic cases where number can be quickly seen as prime or not prime
    if (num<2):
        return False
    elif num%2==0:
        return num == 2 # Two is the only even prime number

    # Start of Rabin Miller Primality Test
    s = num - 1
    counter1 = 0
    # if r is even keep halving it
    while s%2 == 0:
        s = s/2
        counter1 += 1 # increment counter1
    trial = 8 # Number of times we will check num's primailty. Accuracy is improved with increased trials
    while trial>0:
        rando = random.randrange(2,num)
        modNum = pow(rando,s,num) # modNum is equal to rando^r mod num
        if modNum != 1: # Rabin miller test does not apply if v = 1
            counter2 = 0
            while modNum != (num - 1):
                if counter2 == counter1-1:
                    return False
                else:
                    counter2 += 1 # increment counter2
                    modNum = (modNum**2)%num # update v
        trial -= 1
    return True # if none of these conditions have been met, num is likely true


def generateLargePrime():
    # Return a random prime number of keysize bits in size.
    while True:
        num = random.randrange(2**(1023), 2**(1024))
        if isPrime(num):
            return num

def encrypt(message,n,totient,e,printKeys):
    d = modularInverse(e,totient) # the inverse of k mod totient is our private key
    numMsg = stringToInt(message)
    encryptedMsg = pow(int(numMsg),e,n)
    if printKeys:
        f = open("publicKey.txt",'w+')
        f.write(str(n))
        f.close()
        f1 = open("privateKey.txt",'w+')
        f1.write(str(d))
        f1.close()
    return encryptedMsg

def decrypt(encryptedMsg,publickey,privateKey):
    decryptedMsg = pow(int(encryptedMsg),int(privateKey),int(publicKey))
    outputString = intToString(decryptedMsg)
    return outputString

if __name__ == '__main__':
    R1 = raw_input("Would you like to encrypt or decrypt a list of passwords? ")
    while (R1 not in {"Encrypt","encrypt","Decrypt","decrypt"}):
        R1 = raw_input("Please enter one of the key words 'encrypt' or 'decrypt': ")
    R2Text = raw_input("Enter the name of the text file containing your list of passwords (in the format Website/App Name,username,Password;) ")
    with open(R2Text,'r') as f1:
            R2 = f1.read()
    entryList = []
    p = generateLargePrime()
    q = generateLargePrime()
    n = p*q
    totient = (p-1)*(q-1)
    e = 65537 # Can use 65537 as our default value for k (our public key), unless k is a factor of the totient
    while ((e%totient)==0): 
        p = generateLargePrime()
        q = generateLargePrime()
        n = p*q
        totient = (p-1)*(q-1)
    #    e = generateSmallPrime(min(totient,9223372036854775807))
    printKeys = False
    encryptedOutput =''
    decryptedOutput = ''
    if R1 in {"Encrypt","encrypt"}:
        builder = ""
        placer = 0
        for a in str(R2):
            if (a not in{",",";"}):
                builder = builder + str(a)
            else:
                if placer%3 == 0:
                    newTitle = builder
                    builder = ''
                elif placer%3 == 1:
                    newUser = builder
                    builder = ''
                else:
                    newPass = builder
                    builder = ''
                    newEntry = Entry(newTitle,newUser,newPass)
                    entryList.append(newEntry)
                placer = placer + 1
        for i in range (len(entryList)):
            if (i == len(entryList)-1):
                printKeys = True
            encryptedOutput = encryptedOutput + str(entryList[i].appName) + ',' + str(encrypt(str(entryList[i].username),n,totient,e,False)) + ',' + str(encrypt(str(entryList[i].password),n,totient,e,printKeys)) + ';'
        f = open("encryptedList.txt",'w+')
        f.write(encryptedOutput)
        f.close()
        print "Please find a file named encryptedList.txt containing your list of encrypted usernames/passwords, a file named publicKey.txt containing your public key which may stored anywhere, and a file named privateKey.txt which must be stored safely"

    elif R1 in {"Decrypt","decrypt"}:
        publicText = raw_input("Enter the name of a the text file containing the public key: ")
        with open(publicText,'r') as f:
            publicKey = f.read()
        privateText = raw_input("Enter the name of the text file containing private key: ")
        with open(privateText,'r') as f2:
            privateKey = f2.read()
        builder = ""
        placer = 0
        for a in str(R2):
            if (a not in {",",";"}):
                builder = builder + str(a)
            else:
                if placer%3 == 0:
                    newTitle = builder
                    builder = ''
                elif placer%3 == 1:
                    newUser = builder
                    builder = ''
                else:
                    newPass = builder
                    builder = ''
                    newEntry = Entry(newTitle,newUser,newPass)
                    entryList.append(newEntry)
                placer = placer + 1
        for i in range (len(entryList)):
            decryptedOutput = decryptedOutput + str(entryList[i].appName) + ',' + str(decrypt(str(entryList[i].username),int(publicKey),int(privateKey))) + ',' + str(decrypt(str(entryList[i].password),int(publicKey),int(privateKey))) + ';'
        f5 =open("decryptedList.txt",'w+')
        f5.write(decryptedOutput)
        f5.close()
        print "Please find a file named decryptedList.txt containing your list of decrypted usernames/passwords"





