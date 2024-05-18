import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clientApp import *

KAS_TGS = b"\xf6\x83\x8a|L\x9e\xca\xc5\xbb'H;\x88+&\x87"

# access to everyone's password
with open('UserPublicKey.txt', 'r') as input_file:
    content1 = input_file.read()

Keys = content1.strip().split('||')
Keys = [Key.strip() for Key in Keys]

PU_A = Keys[0]
n_A = Keys[1]
PU_B = Keys[2]
n_B = Keys[3]
PU_C = Keys[4]
n_C = Keys[5]
# PU_C and n_C is copy of B right now
# PU_A (Public Key for User A): 10918241545458707164346272246022548841
# n_A (Parameter for User A): 228228880681173030506413887301289747929
# PU_B (Public Key for User B): 66564982146357233858268702965596204459
# n_B (Parameter for User B): 172802230835666172654130396562467429321
# PU_C (Public Key for User C): 66564982146357233858268702965596204459
# n_C (Parameter for User C): 172802230835666172654130396562467429321

# load message from Client
with open('MfromClient.txt', 'r') as input_file:
    content2 = input_file.read().strip()
# Message C:
# Destination: 01000010 (Binary representation of 'B')
# Message B: 001101110001010011011010000000010000000010011100110011111111110001011010111010011001000011110011111110010101101000110010100110001011101101010101
# Nonce B: 10010011110101100101001000111001110101100011000101100000101111011001010111011000001111110001111011101000111011000111110011011010
# Message D:
# Encrypted Message: 110001011001011011000001
# Nonce D: 01101001000010101111011111110001010010111000101101001110111100101110100111000110110000010011011001111000010010100110000001101010

# Splitting MessageC and MessageD
Messages = content2.strip().split('||')
if len(Messages) < 2:
    raise ValueError("MfromClient.txt must contain two messages separated by a comma.")

Destination = BinaryToString(Messages[0].strip())
MessageB = BinaryToByte(Messages[1].strip())
NonceB = BinaryToByte(Messages[2].strip())
MessageD = BinaryToByte(Messages[3].strip())
NonceD = BinaryToByte(Messages[4].strip())

# print(Destination)
# print(MessageB)
# print(NonceB)
# print(MessageD)
# print(NonceD)
# B
# b'7\x14\xda\x01\x00\x9c\xcf\xfcZ\xe9\x90\xf3\xf9Z2\x98\xbbU'
# b'\x93\xd6R9\xd61`\xbd\x95\xd8?\x1e\xe8\xec|\xda'
# b'\xc5\x96\xc1'
# b'i\n\xf7\xf1K\x8bN\xf2\xe9\xc6\xc16xJ`j'

# Decrypt and Split MessageB
print(f"{NonceB}")
print(f"{MessageB}")
ContentB = DecryptAES(MessageB, KAS_TGS, NonceB)
StringContentB = BinaryToString(ContentB)
print(f"ContentB = {StringContentB}")
MessageB_parts = StringContentB.strip().split('||')

Kc_TGS = bytes.fromhex(MessageB_parts[0].strip())
print(f"Kc = {Kc_TGS}")
ClientSourceAS = MessageB_parts[1].strip()
print(f"Client = {ClientSourceAS}\n")
# Decrypt and Split MessageD
ContentD = DecryptAES(MessageD , Kc_TGS, NonceD)
StringContentD = BinaryToString(ContentD)
print(f"StringD = {StringContentD}")
MessageD_parts = StringContentD.strip().split('||')

print(f"{MessageD_parts}")
ClientSourceTGS = MessageD_parts[0].strip()
Destination = MessageD_parts[1].strip()

#Test Case
# ClientSourceAS = A
# Destination = B
if ClientSourceTGS != ClientSourceAS:
    output_file_path = f'../user{ClientSourceAS}/MfromTGS.txt'
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Wrong Password")
    raise ValueError("Wrong Password")

# Determine the public key to use for encryption based on DesClient
if Destination == "A":
    public_key = PU_A
    n = n_A
elif Destination == "B":
    public_key = PU_B
    n = n_B
elif Destination == "C":
    public_key = PU_C
    n = n_C
else:
    raise ValueError("Unknown destination client")

# Encrypt the session key with the appropriate public key
Messagef = public_key + "||" + n
MessageF, NonceF = EncryptAES(StringToBinary(Messagef), Kc_TGS)

# Write the response to the output file for 
print(f"MessageF = {MessageF}")
print(f"NonceF = {NonceF}")
print(f"{ByteToBinary(MessageF)}||{ByteToBinary(NonceF)}")
output_file_path = f'../user{ClientSourceAS}/MfromTGS.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(f"{ByteToBinary(MessageF)}||{ByteToBinary(NonceF)}")

print(f"Response written to {output_file_path}")
