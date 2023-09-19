import socket
from DHKeyEX import *

BUFF_SIZE = 65536
def main():
    host_ip, server_port = socket.gethostname(), 9999

    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host_ip, server_port))
    printfw("Hello I am Alice")
    step = 1
    Alices_nonce = 0
    Bobs_nonce   = 0
    Bobs_Cert     = {}
    Bobs_pblc_RSA_key = b''
    Alices_prvt_ECC_key = 0
    Alices_pblc_ECC_key = 0
    Alices_premaster_secret = 0
    Alices_prvt_RSA_key_pair, Alices_pblc_RSA_key = gen_RSA_sign_keys() 
    Alices_symm_enc_key = b'' 
    Bobs_symm_enc_key   = b''
    
    while True:
        # Establish connection to TCP server and exchange data
        if step == 1:
            pnl()
            printfw("Step 01:")
            printfw("Alice sends Bob a random number 32 bytes/256 bits (clear text) indicate she wants to communicate with Bob")
            Alices_nonce = gen_nonce(32)
            printfw("Alice's nonce: " + str(Alices_nonce))
            tcp_client.sendall(long_to_bytes(Alices_nonce))
            step +=1
        if step == 2:
            # Read data from the TCP server and close the connection
            data = tcp_client.recv(BUFF_SIZE)
            Bobs_nonce = bytes_to_long(data)
            pnl()
            printfw("Step 02:")
            printfw("Bob replies with his own random number (clear text), indicating he is interested in communicating with Alice")
            printfw("Bob's nonce: " + str(Bobs_nonce))
            step +=1
        # wait_or_quit()
        if step == 3:
            # data = tcp_client.recv(BUFF_SIZE)
            data = tcp_client.recv(BUFF_SIZE)
            Bobs_Cert = json.loads(data.decode())
            signature = tcp_client.recv(BUFF_SIZE)
            Bobs_pblc_RSA_key = RSA.importKey(tcp_client.recv(BUFF_SIZE), passphrase=None)
            pnl()
            printfw("Bob's Cert: " + str(Bobs_Cert))
            pnl()
            printfw("Bob's singature raw: " + str(signature))
            pnl()
            printfw("Bobs public RSA signing key: " + str(Bobs_pblc_RSA_key))
            if RSA_verify(json.dumps(Bobs_Cert), signature, Bobs_pblc_RSA_key) == True:
                printfw("Alice verified Bob's ECC Cert!")
            else:
                printfw("Verification Failed")
            step +=1
        if step == 4:
            pnl()
            printfw("Step 04:")
            printfw("Alice genates the premaster secret from Bob'b public key and sends Bob her ECC public key")
            Alices_prvt_ECC_key = getRandomRange(2, Bobs_Cert['Order']-1)
            while GCD(Alices_prvt_ECC_key, Bobs_Cert['Order']) != 1:
                Alices_prvt_ECC_key = getRandomRange(2, Bobs_Cert['Order']-1)
            Alices_pblc_ECC_key     = (Alices_prvt_ECC_key*Bobs_Cert['Gener'][0])%Bobs_Cert['Prime']
            Alices_premaster_secret = (Alices_prvt_ECC_key*Bobs_Cert['Pub_key'])%Bobs_Cert['Prime']
            printfw("Alice's private ECC key: " + str(Alices_prvt_ECC_key))
            printfw("Alice's public ECC key: " + str(Alices_pblc_ECC_key))
            printfw("Alice's calculated Shared Secret: " + str(Alices_premaster_secret))
            data = long_to_bytes(Alices_pblc_ECC_key)
            tcp_client.sendall(data)
            signature = RSA_sign(data, Alices_prvt_RSA_key_pair)
            tcp_client.sendall(signature)
            tcp_client.sendall(Alices_pblc_RSA_key.exportKey(format='PEM', passphrase=None, pkcs=1))
            step += 2
        if step == 6:
            pnl()
            printfw("Step 06:")
            printfw("Both Bob and Alice generate the same master secret from the Premaster secret, the phrase 'master secret' and the two random number that were previously exchanged. These values are hashed to make the Master Secret")
            Alices_master_secret = long_to_bytes(Alices_premaster_secret) + b"master secret" + long_to_bytes(Alices_nonce) + long_to_bytes(Bobs_nonce)
            printfw("Alices master secret: " + str(Alices_master_secret))
            printfw("Master Secret Length: " + str(len(Alices_master_secret)))
            step +=1
        if step == 7:
            pnl()
            printfw("Step 07:")
            printfw("Bob and Alice generate the Symmetric Server Encryption key, and the Client Encryption key using the Master Secret")
    #           "key expansion" and the two random numbers. This uses a Pseudo Random Function to generate a digest with the number of bits needed for the keys.
            Alices_symm_enc_key, Bobs_symm_enc_key = gen_symmetric_keys(Alices_master_secret)
            printfw("Client symmetric encrytpion key: " + str(Alices_symm_enc_key))
            printfw("Server symmetric encrytpion key: " +  str(Bobs_symm_enc_key))
            step +=1
        if step == 8:
            pnl()
            printfw("Step 08:")
            printfw("Alice sends a message to Bob using Client symmetric key to encrypt")
            pnl()
            msg_to_Bob = input("    Write a message for Alice to send Bob, once Bob completes Step 07:")
            ciphertext = AES_GCM_encrypt(msg_to_Bob, Alices_symm_enc_key)
            signature  = RSA_sign(msg_to_Bob, Alices_prvt_RSA_key_pair)
            data       = ciphertext.encode()
            tcp_client.sendall(data)
            tcp_client.sendall(signature)
            pnl()
            printfw("The ciphertext sent to Bob: " + str(ciphertext))
            pnl()
            printfw("The signature sent to Bob: " + str(signature))
            step +=2
        if step == 10:
            pnl()
            printfw("Step 10:")
            printfw("Alice receives Bob's reply and decrypts it with the Server sysmmetric encryption key")
            data = tcp_client.recv(BUFF_SIZE)
            ciphertext = data.decode()
            plaintext = AES_GCM_decrypt(ciphertext, Bobs_symm_enc_key)
            signature = tcp_client.recv(BUFF_SIZE)
            
            printfw("Bob's singature raw: " + str(signature) + "\n\n")
            if RSA_verify(plaintext, signature, Bobs_pblc_RSA_key) == True:
                printfw("Alice verified Bob's signature!")
                step +=1
            else:
                printfw("Verification Failed")
            pnl()
            printfw("Plaintext received by Alice: " + str(plaintext))
        wait_or_quit("any")
    tcp_client.close()

if __name__ == '__main__':
    main()
