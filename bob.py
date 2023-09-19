import socket
from DHKeyEX import *
BUFF_SIZE = 65536

Bobs_prvt_RSA_key_pair, Bob_pblc_RSA_key = gen_RSA_sign_keys()
printfw("Hello I am Bob. I am a server with an secp521r1 ECC certificate\n")
# openssl ecparam -name secp521r1 -out secp521r1.pem -param_enc explicit
# openssl ecparam -in secp521tr1.pem -text -noout > parameters
# mv parameters parameters_EC
# run param_readerEC()
# edit by hand to get in json format 
Bobs_Cert = {}
f = open("parameters_secp521r1.json", 'r')
json_file = f.read().strip()
Bobs_Cert = json.loads(json_file)
Bobs_Cert['Gener'] = tuple(Bobs_Cert['Gener'])
prime = Bobs_Cert['Prime']
A = Bobs_Cert['A']
B = Bobs_Cert['B']
G = Bobs_Cert['Gener']
order = Bobs_Cert['Order']
# Bob generates his
Bobs_prvt_ECC_key = getRandomRange(2, order)
while GCD(Bobs_prvt_ECC_key, order-1) != 1:
        Bobs_prvt_ECC_key = getRandomRange(2, order-1)

# #calculate bP mod(p), Bob's public key is the x value, not both points
Bobs_pblc_ECC_key = (Bobs_prvt_ECC_key*G[0]%prime, Bobs_prvt_ECC_key*G[1]%prime)
# printfw(" Bob's public key B\n", Bobs_pblc_ECC_key[0])
Bobs_Cert.update({'Pub_key': Bobs_pblc_ECC_key[0]})
printfw("Bobs Cert:")
printfw(json_file)

# printfw("\n\n Bob's private key b:\n", Bobs_prvt_ECC_key)

# TO DO - Bob needs to sign Key

def main ():
    # get the hostname
    host = socket.gethostname()
    port = 9999  # initiate port no above 1024
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    pnl()
    printfw("Please start Alice in another window, so I have someone to talk with")
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    printfw("Connection from: " + str(address))
    step = 1
    Alices_nonce = 0
    Bobs_nonce   = 0
    Alices_pblc_ECC_key = 0
    Alices_pblc_RSA_key = b''
    Bobs_premaster_secret = 0
    Bobs_master_secret    = 0
    Alices_symm_enc_key = b''
    Bobs_symm_enc_key   = b''
    while True:
        # receive data stream. it won't accept data packet greater than BUFF_SIZE bytes
        if step == 1:
            pnl()
            printfw("Step 01:")
            printfw("Alice sends Bob a random number 32 bytes/256 bits (clear text) indicate she wants to communicate with Bob")
            wait_or_quit("Step 01")
            data = conn.recv(BUFF_SIZE)
            Alices_nonce = bytes_to_long(data)
            printfw("Alices nonce: " + str(Alices_nonce))
            step +=1
        if step == 2:
            pnl()
            printfw("Step 02:")
            printfw("Bob replies with his own random number (clear text), indicating he is interested in communicating with Alice")
            wait_or_quit("Step 02")
            Bobs_nonce = gen_nonce(32)
            printfw("Bob's nonce: " + str(Bobs_nonce))
            conn.sendall(long_to_bytes(Bobs_nonce))
            step += 1
        if step == 3:
            pnl()
            printfw("Step 03:")
            printfw("Bob sends Alice the certficate, which consists of the ECDH parameters and Bob's public RSA signing key")
            wait_or_quit("Step 03")
            printfw("Bobs Cert: " + json.dumps(Bobs_Cert))
            conn.sendall(json.dumps(Bobs_Cert).encode())
            signature = RSA_sign(json.dumps(Bobs_Cert), Bobs_prvt_RSA_key_pair)
            conn.sendall(signature)
            conn.sendall(Bob_pblc_RSA_key.exportKey(format='PEM', passphrase=None, pkcs=1))
            step +=1
        # wait_or_quit()
        if step == 4:
            pnl()
            printfw("Step 04:")
            printfw("Alice genates the premaster secret from Bob'b public key and sends Bob her ECC public key")
            data = conn.recv(BUFF_SIZE)
            Alices_pblc_ECC_key = bytes_to_long(data)
            signature = conn.recv(BUFF_SIZE)
            Alices_pblc_RSA_key = RSA.importKey(conn.recv(BUFF_SIZE), passphrase=None)
            wait_or_quit("Step 04")
            printfw("Alice genates the premaster secret from Bob'b public key and sends Bob her ECC public key")
            pnl()
            printfw("Alices public ECC key:" + str(Alices_pblc_ECC_key))
            pnl()
            printfw("Alice's singature raw:" + str(signature))
            pnl()
            printfw("Alice's signature key: " + str(Alices_pblc_RSA_key))
            if RSA_verify(data, signature, Alices_pblc_RSA_key) == True:
                printfw("Bob verified Alice's public ECC key!")
                step +=1
            else:
                printfw("Verification Failed")
        if step == 5:
            pnl()
            printfw("Step 05:")
            printfw("Bob generates the premaster secret from Alice's public key - confirm it is the same as Alice's")
            wait_or_quit("Step 05")
            Bobs_premaster_secret = (Bobs_prvt_ECC_key*Alices_pblc_ECC_key)%Bobs_Cert['Prime']
            printfw("Bob's calculated Shared Secret: " + str(Bobs_premaster_secret))
            step += 1
        if step == 6:
            pnl()
            printfw("Step 06:")
            printfw("Both Bob and Alice generate the same master secret from the Premaster secret, the phrase 'master secret' and the two random number that were previously exchanged. These values are hashed to make the Master Secret")
            wait_or_quit("Step 06:")
            Bobs_master_secret = long_to_bytes(Bobs_premaster_secret) + b"master secret" + long_to_bytes(Alices_nonce) + long_to_bytes(Bobs_nonce)
            printfw("Bobs master secret: " + str(Bobs_master_secret))
            printfw("Master Secret Length: " + str(len(Bobs_master_secret)))
            step +=1
        if step == 7:
            pnl()
            printfw("Step 07")
            printfw("Bob and Alice generate the Symmetric Server Encryption key, and the Client Encryption key using the Master Secret")
            wait_or_quit("Step 07")
    #           "key expansion" and the two random numbers. This uses a Pseudo Random Function to generate a digest with the number of bits needed for the keys.
            Alices_symm_enc_key, Bobs_symm_enc_key = gen_symmetric_keys(Bobs_master_secret)
            printfw("Client symmetric encrytpion key: " + str(Alices_symm_enc_key))
            printfw("Server symmetric encrytpion key: " + str(Bobs_symm_enc_key))
            pnl()
            printfw("Confirm these symmetric encrytpion keys match the ones calculated by Alice")
            step +=1
        if step == 8:
             pnl()
             printfw("Step 08:")
             printfw("Alice sends a message to Bob using Client key pair to encrypt and sign")
             wait_or_quit("Step 08")
             printfw("Go to Alice's window and enter a message for Bob")
             step +=1
        if step == 9:
            data       = conn.recv(BUFF_SIZE)
            ciphertext = data.decode()
            plaintext  = AES_GCM_decrypt(ciphertext, Alices_symm_enc_key)
            signature  = conn.recv(BUFF_SIZE)
            printfw("Step 09:")
            printfw("Bob decrypts Alice's message using the Client symmetric key")
            wait_or_quit("Step 09")
            pnl()
            printfw("Alice's singature raw: " + str(signature))
            if RSA_verify(plaintext, signature, Alices_pblc_RSA_key) == True:
                printfw("Bob verified Alice's signature!")
            else:
                printfw("Verification Failed")
            pnl()
            printfw("Plaintext message received by Bob: " + str(plaintext))
            step +=1
        if step == 10:
            pnl()
            printfw("Step 10:")
            printfw("Bob sends a reply to Aice using Server key pair to encrypt and sign")
            wait_or_quit("Step 10")
            msg_to_Alice  = input("    Write a reply from Bob to Alice: ")
            ciphertext    = AES_GCM_encrypt(msg_to_Alice, Bobs_symm_enc_key)
            data          = ciphertext.encode()
            signature     = RSA_sign(msg_to_Alice, Bobs_prvt_RSA_key_pair)
            conn.sendall(data)
            conn.sendall(signature)
            # printfw("The ciphertext sent to Alice: \n" + str(ciphertext))
            # printfw("The signature sent to Alice: \n" + str(signature))
            printfw("Verify with Alice that this is the message received.")
        wait_or_quit("any")
    conn.close()  # close the connection

if __name__ == '__main__':
    main()