# Abaixo está uma mensagem que foi trocada entre dois geeks.
# Seu desafio é descriptografar a mensagem e digitar a 
# resposta na caixa fornecida abaixo.

import string
# Python code to implement
# Vigenere Cipher
 
# This function generates the
# key in a cyclic manner until
# it's length isn't equal to
# the length of original text
def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
     
# This function returns the
# encrypted text generated
# with the help of the key
def cipherText(string, key):
    cipher_text = []
    for i in range(len(string)):
        x = (ord(string[i]) +
             ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))
     
# This function decrypts the
# encrypted text and returns
# the original text
def originalText(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return("" . join(orig_text))
     

 

alphabet = string.ascii_uppercase
header = [l for l in alphabet]
# print(header)
# for i in range(0,26):
#     print(*(header[i % 26::] + header[0: i % 26]))
    
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
# B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
# C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
# D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
# E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
# F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
# G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
# H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
# I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
# J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
# K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
# L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
# M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
# N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
# O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
# P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
# Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
# R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
# S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
# T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
# U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
# V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
# W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
# X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
# Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
# Z A B C D E F G H I J K L M N O P Q R S T U V W X Y
a = ["ACCAG", "EAEEI", "KXAAX", "ENNXS", "GDGNL"]
b = ["SEXXP", "XMOEX", "LIKHS", "UAATE", "BEGXE"]
c = ["OZTGC", "KEDMW", "XLZXE", "OXXXA", "HCVLS"]
d = ["EM"]
# Encryption
# The plaintext(P) and key(K) are added modulo 26.
# Ei = (Pi + Ki) mod 26

# Decryption
# Di = (Ei - Ki + 26) mod 26
msg = [a,b,c,d]
print(msg)
delta = 8
old = 5
# for m in msg:
#     for word in m:
#         pass
    
string = "EAEEI"
keyword = "WQYOC"
key = generateKey(string, keyword)
cipher_text = string#cipherText(string,key)
print(key)
print("Ciphertext :", cipher_text)
print("Original/Decrypted Text :",
        originalText(cipher_text, key))