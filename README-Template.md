# Message Encrypt

The program asks the user for the name of a .txt file to be encrypted/decrypted (and for the public and private keys if the user has selected to decrypt), and uses the RSA algorithm and optimal asymmetric encryption padding to encrypt/decrypt the message.

## Installing

Pull the directory as is.  On the command line, run `pip install -r requirements.txt`.  This command will install the necessary pycrypto library (pycrypto 2.6.1).


## Example Encryption

The program prompts the user to select *encrypt* or *decrypt*. If the user selects *encrypt*, the program will prompt the user to input the name of the text file containing the message to be encrypted. It will then output a text file containing an encrypted message, a text file containing a public key, and a text file containing a private key. <br />
If we have a .txt file *"myMessage"*: <br />
![myMessage.txt](example/A.png) <br />
saved in the current directory, and we run `python messageEncrypt.py` the command line will present the prompt:  <br />
*Would you like to encrypt or decrypt a message?* <br />
Answer with *"Encrypt"* and the following prompt will appear: <br />
*Enter the name of the text file containing your message to be encrypted or decrypted:* <br />
Reply with the name of the .txt file we want to encrypt which is "myMessage.txt". <br />
The program then performs the encryption.  When encryption is complete the program displays on the command line *Please find a file named encryptedMessage.txt containing your encrypted message, a file named publicKey.txt containing your public key which may be stored anywhere and a file named privateKey.txt which must be stored safely*.  All of the specified files are  found in current the directory:  <br />
![encryptedMessage.txt](/example/B.png)
![publicKey.txt](/example/C.png)
![privateKey.txt](/example/D.png)



## Example Decryption
(We will continue from our example above and use the files encryptedMessage.txt, publicKey.txt, and privateKey.txt; these could be saved under any names when executed by the user). <br />

If the user selects *decrypt*, the program will then prompt the user to input the name of a text file containing an encrypted message, the name a text file containing the public key associated with that message, and the name of the text file containing the private key associated with that message. The program will output a text file containing the decrypted message. <br />
If we have the text files containing an encrypted message, and the public and private keys associated with that message saved in the current directory, and we run: `python messageEncrypt.py` the command line will present the prompt:  <br />
*Would you like to encrypt or decrypt a message?*  </center> <br />
Answer with *"Decrypt"* and the following prompt will appear: <br />
*Enter the name of the text file containing your message to be encrypted or decrypted:* </center>  <br />
Reply with the name of the .txt file we want to decrypt which is *"encryptedMessge.txt"*. The command line will then ask for the public and private keys, as follows:<br />
*Enter the name of a the text file containing the public key:* </br>
*Enter the name of a the text file containing the private key:*</br>
After entering both requests, the command line will display
*Please find a file named decryptedMessage.txt containing your decrypted mesaage* </br>
In our directory we will find decryptedMessage.txt which contains our original message!
![decryptedMessage.txt](/example/E.png)



## Implementation

In the encryption process of the RSA algorithm, I used the Rabin Miller Primality Test to test whether the large primes I was generating using the random library were random. <br />
Also in the encryption process of the RSA algorithm, I used a recursive GCD algorithm in order to calculate the modular inverse, which serves as the private key.



## Built With

* [random](The Python Standard Library: Lib/random.py) - Library used in RSA implementation
* [math](The Python Standard Library) - Dependency Management
* [Crypto](https://github.com/dlitz/pycrypto) - Used hash functions from this library to implement padding.



## License

This project is licensed under the MIT License. The rest are copyright/licensed by their respective authors.

## Acknowledgments

* Rajesh Pavuluru, Indiana State University: http://cs.indstate.edu/~rpavuluru/Abstract.pdf.  Implemented the Rabin Miller Primality test by reading this paper.  The primality test is used when generating large primes in the RSA algorithm.


