import random
import math
from Crypto.Hash import SHA256

def stringToBitList(message):
    """Converts a string with alphabetic, numeric and special characters to a list of 0's and 1's"""
    total = []
    for character in message:
        # Store Unicode code point of the character in c
        c = ord(character) 
        indiv = []
        # Convert the value in c to binary, and store this binary as a list of 0's and 1's
        while c > 0:
            indiv = [(c % 2)] + indiv
            c = c / 2
        # Pad the binary representation to 8 bits
        indiv = padBits(indiv,8)
        # Sum the padded binary representations of each character 
        total = total + indiv
    return total

def bitListToInt(bitList):
    """Converts a list of 0's and 1's, to an int of base 10"""
    return int(''.join([('0','1')[b] for b in bitList]),2)

def stringToInt(message):
    """Wrapper function for above two funtions to convert a 
    string to a base 10 integer based on the ASCII values of
     its characters"""
    return bitListToInt(stringToBitList(message))

def binstringToBitList(binstring): 
    """Converts a string of '0's and '1's to a list of 0's and 1's"""
    bitList = []
    for bit in binstring:
        bitList.append(int(bit))
    return bitList

def padBits(bits, padding):
    """Pad the input bits with 0's so that it is of length padding"""
    return [0] * (padding-len(bits)) + bits

def bitListToString(paddedBitSeq):
    """Converts a list of 0's and 1's to a string of alpha/numeric characters"""
    charBuilder = ''
    # Iterate through by 8's becaause each padded bit sequence is 8 bits long
    for segment in range(0,len(paddedBitSeq),8): 
        # concatenate each new char onto the built up string
        charBuilder = charBuilder + bitsToChar(paddedBitSeq[segment: segment+8]) 
    return charBuilder

def bitsToChar(bitSeq):
    """Converts each 8 bit length padded bit sequences 
    back to a char based on its unicode value"""
    value = 0
    for bit in bitSeq:
        value = (value * 2) + bit # This for loop will determine the numeric value of the binary bit sequence input
    return chr(value)

def intToString(integer):
    """Wrapper function for above four funtions to convert an i
    nteger of base 10 to a string based on the ASCII values of 
    its characters"""
    binary = bin(integer)[2:]
    bitSeq = binstringToBitList(binary)
    return bitListToString(padBits(bitSeq,(len(bitSeq)+(8-(len(bitSeq)%8)))))

def extendedGCD(a, b):
    """Returns gcd, x and y so that a*x+b*y = gcd(x,y)"""
    # Base case (when a = 0)
    if a == 0:
        return (b,0,1)
    # Recursive case
    else:
        gcd, x, y = extendedGCD(b%a,a)
        return (gcd, y-(b/a)*x, x)

def modularInverse(a,mod):
    """Returns the value whose product with (a % mod) is equal to 1"""
    gcd,x,y = extendedGCD(a,mod)
    return x%mod

def isPrime(num):
    """"Return True if the number is prime, and False otherwise."""
    # Two basic cases where number can be quickly seen as prime or not prime
    if (num<2):
        return False
    elif num%2==0:
        return num == 2 # Two is the only even prime number

    # Start of Rabin Miller Primality Test
    s = num - 1
    counter1 = 0
    # if s is even keep halving it
    while s%2 == 0:
        s = s/2
        # increment counter1
        counter1 += 1 
    trial = 8 # Number of times we will check num's primailty. Accuracy is improved with increased trials
    while trial>0:
        rando = random.randrange(2,num)
        modNum = pow(rando,s,num) # modNum is equal to rando^r mod num
        if modNum != 1: # Rabin miller test does not apply if v = 1
            counter2 = 0
            while modNum != (num - 1):
                # case that would mean that num is not prime
                if counter2 == counter1-1:
                    return False
                else:
                    # increment counter2 
                    counter2 += 1
                    # update v
                    modNum = (modNum**2)%num 
        trial -= 1
    # if none of these conditions have been met, num is likely tru   
    return True 

def generateLargePrime():
    """""Returns a prime number in the range from 2^1023 to (2^1024)-1"""
    while True:
        num = random.randrange(2**(1023), 2**(1024)-1)
        if isPrime(num):
            return num

def padOAEP(message):
    # Set the messge to 768 bits because the modulus we generated in 
    # the generateLargePrime() function is 1024 bits, so are message
    # is covered for exactly 768 bits.
    message = message + (768 - len(message))*'0'

    len_K0 = 128
    len_K1 = 128
    # Set r to be a random value between 2^127 and 2^128
    r = random.randrange(2**127,2**128)
    # Add K1 zeroes to the back of our message
    m = int(message,2) << len_K1

    # Use hash function from imported Crypto.hash library to expand r.
    # We need r to be 896 bits so we will actually hash it 4 times
    hashlist = []
    hash1 = SHA256.new()
    hash1.update(bin(r)[2:])
    hash1 = int(hash1.hexdigest(),16)
    hashlist.append(hash1)
    hash2 = SHA256.new()
    hash2.update(bin(r+1)[2:])
    hash2 = int(hash2.hexdigest(),16)
    hashlist.append(hash2)
    hash3 = SHA256.new()
    hash3.update(bin(r+2)[2:])
    hash3 = int(hash3.hexdigest(),16)
    hashlist.append(hash3)
    hash4 = SHA256.new()
    hash4.update(bin(r+3)[2:])
    # Shift our last hash to the right by 128 to get to 896
    hash4 = int(hash4.hexdigest(),16) >> 128
    hashlist.append(hash4)


def encrypt(message,n,totient,e,printKeys):
    """Returns an encrypted form of the unencrypted message input"""
    # The inverse of k mod totient is our private key. Store in d
    d = modularInverse(e,totient) 
    # Convert our message of alpha/numeric/special to an int of base 10 based on its unicode values
    numMsg = stringToInt(message)
    # message^e mod n is our encrypted message. Store in encryptedMsg
    encryptedMsg = pow(res,e,n) 
    if printKeys:
        # Write new text file titled "publicKey"
        pubf = open("publicKey.txt",'w+') #
        pubf.write(str(n)) # Note: the totient and n values, are both referred to as public keys, but because only the n
                        # value is used to decrypt the message later on, this will be our only public key
        pubf.close()
        # Write new text file titled "privateKey"
        privf = open("privateKey.txt",'w+')
        privf.write(str(d))
        privf.close()
    return encryptedMsg

def decrypt(encryptedMsg,publickey,privateKey):
    """Returns the decrypted form of the encrypeted message input"""
    # The decrypted message is equal to (encryptedMsg^privatekey) mod publicKey
    x = unpad(encryptedMsg)
    decryptedMsg = pow(int(x),int(privateKey),int(publicKey))
    # Conver th
    outputString = intToString(decryptedMsg)
    return outputString


if __name__ == '__main__':
    R1 = raw_input("Would you like to encrypt or decrypt a list of passwords? ")
    # Keep asking for input until one the key words indicating encrypt or decrypt has been entered
    while (R1 not in {"Encrypt","encrypt","Decrypt","decrypt"}):
        R1 = raw_input("Please enter one of the key words 'encrypt' or 'decrypt': ")
    R2Text = raw_input("Enter the name of the text file containing your list of passwords " +
        '\n' + "(Your list should be in the format:" +'\n' "website/app name " + '\n' + "username" + '\n'+"password):")
    with open(R2Text,'r') as listf:
        R2 = listf.read()
        lines = R2.split("\n") # lines is a list of strings, each item in the list representing a line in the 
                               # the text file that was input
        # Remove all empty strings that represent blank lines                        
        lines = filter(None, lines)
    # linenum will represent the line number in the text file containing list of passwords
    linenum = 0
    p = generateLargePrime()
    q = generateLargePrime()
    n = p*q
    totient = (p-1)*(q-1)
    e = 65537 # Can use 65537 as our default value for k (our public key), unless k is
              # a factor of the totient
    # In the rare case when 65537 is not a unit of the totient, 
    # pick two new random numbers and calculate a new totient. 
    # Keep generating two random numbers until a unit of the the
    # totient is found. 
    while ((e%totient)==0): 
        p = generateLargePrime()
        q = generateLargePrime()
        n = p*q
        totient = (p-1)*(q-1)
    printKeys = False
    # Case when user wants to encrypt list
    if R1 in {"Encrypt","encrypt"}:
        # elist will be the text file containing the encrypted list of passcodes we will write to
        elist = open("encryptedList.txt","a")
        for i in range (len(lines)):
            if linenum%3 == 0:
                # Don't encrypt when linenum%3 is equal to 0. This is the line that carries the title.
                # Simply write to the text file elist.
                elist.write(str(lines[i]))
                elist.write('\n')
            elif linenum%3 == 1:
                # Encrypt when linenum%2 is equal to 1. This is the line that carries the username.
                elist.write(str(encrypt(padOAEP(str(lines[i])),n,totient,e,False)))
                elist.write('\n')
            else:
                if (i == len(lines)-1):
                    printKeys = True 
                # Encrypt when linenum%3 is equal to 2. This is the line that carries the password.
                elist.write(str(encrypt(padOAEP(str(lines[i])),n,totient,e,printKeys)))
                elist.write('\n')
            # increment linenum by 1
            linenum = linenum + 1
        print ("Please find a file named encryptedList.txt containing your list of encrypted "
            "usernames/passwords, a file named publicKey.txt containing your public key which may "
            "stored anywhere, and a file named privateKey.txt which must be stored safely")
    # Case when user wants to decrypt list
    elif R1 in {"Decrypt","decrypt"}:
        # Access the value of the public key
        publicText = raw_input("Enter the name of a the text file containing the public key: ")
        with open(publicText,'r') as pub:
            publicKey = pub.read()
        # Access the value of the private key
        privateText = raw_input("Enter the name of the text file containing private key: ")
        with open(privateText,'r') as pri:
            privateKey = pri.read()
        dlist = open("decryptedList.txt","a")
        for i in range(len(lines)):
            if linenum%3 == 0:
                # Don't decrypt when linenum%3 is equal to 0. This is the line that carries the title
                # and has not been enrypted. Simply write to the text file dlist.
                dlist.write(str(lines[i]))
                dlist.write('\n')
            elif linenum%3 == 1:
                # Encrypt when linenum%3 is equal to 1. This is the line that carries the username.
                dlist.write(str(decrypt(str(lines[i]),int(publicKey),int(privateKey))))
                dlist.write('\n')
            else:
                # Decrypt when linenum%3 is equal to 2. This is the line that carries the password.
                dlist.write(str(decrypt(str(lines[i]),int(publicKey),int(privateKey))))
                dlist.write('\n')
                # Make second new line for clarity to separate the entries in the list
                dlist.write('\n') 
                #increment linenum by 1
            linenum = linenum + 1
        print "Please find a file named decryptedList.txt containing your list of decrypted usernames/passwords"





