from EntryClass import *
import random
import math

def stringToBitList(message):
    bitList = []
    for character in message:
        b = bin(ord(character))[2:] # don't include the first two characters because they will contain 0b, not the actual value
        b = '00000000'[len(b)]+b
        for bit in b:
            bitList.append(bit)
    return bitList 

def bitListToInt(bitList):
    return int(''.join([('0','1')[int(e)] for e in bitList]),2)

def stringToInt(message):
    return bitListToInt(stringToBitList(message))

def NumToString(message):
    pass

def modularInverse(a,mod):
    pass

def generateLargePrime():
    pass

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
    outputString = NumToString(decryptedMsg)
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
    printKeys = False
    encryptedOutput =''
    decryptedOutput = ''
    if R2 in {"Encrypt","encrypt"}:
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





