import md5
import time
from string import ascii_lowercase
from itertools import product
MAP64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def convertTo64 (dat):
    s = ''
    for i in range(22):
        s += MAP64[dat & 0b00111111]
        dat = dat >> 6
    return s

def MD5_crypt(password, salt):
    
    magic = '$1$'

    alternateSum = md5.md5(password + salt + password).digest()

# initialize temp to password concat by magic and salt
    temp = password + magic + salt

# append len(password) bytes from front of alternateSum to end of temp
    for i in range(len(password)):
            temp = temp + alternateSum[i]

# go through the binary representation of len(password) from LSB to MSB
# if it is a 1 concat a byte of 0x00
# if it is a 0 concat the first byte (char) of password
    i = len(password)
    while i > 0:
        if i & 1:
            temp = temp + chr(0)
        else:
            temp = temp + password[0]
        i = i >> 1

# Calculate Intermediate0
    intermediate0 = md5.md5(temp).digest()


    prevIntermediate = intermediate0

# For i = 0 to 999 (inclusive), compute Intermediatei+1 by concatenating the following:
# If i is even, concat Intermediatei
# If i is odd, concat password
# If i is not divisible by 3, concat salt
# If i is not divisible by 7, concat password
# If i is even, concat password
# If i is odd, concat Intermediatei
# Hash the result to get Intermediatei+1

    for i in range(1000):
        temp2 = ''
        if i & 1:
            temp2 += password
        else:
            temp2 += prevIntermediate

        if i % 3:
            temp2 += salt

        if i % 7:
            temp2 += password

        if i & 1:
            temp2 += prevIntermediate
        else:
            temp2 += password
            
            
        prevIntermediate = md5.md5(temp2).digest()

    final = prevIntermediate

    order = [11, 4, 10, 5, 3, 9, 15, 2, 8, 14, 1, 7, 13, 0, 6, 12]

# Rearrange the bytes int the specified order
    temp = 0
    for i in range(16):
        temp = (temp << 8) + int(ord(final[order[i]]))

# read the bytes 6 bits at a time using the base64 conversion table to get 22 characters
    passwd = convertTo64(temp)

    return passwd

# Test it gives the correct answer for a known hash
# print(MD5_crypt("czormg", "hfT7jp2q"))

# team31:$1$4fTgjp6q$PQDcVf/DoQC6PzvLki2PE/:16653:0:99999:7:::
givenSalt = "4fTgjp6q"
givenHash = "PQDcVf/DoQC6PzvLki2PE/"

# givenSalt = "hfT7jp2q"
# givenHash = "rhb3sPONC2VlUS2CG4JFe0" #pass = czormg; salt = hfT7jp2q
# Test it can recover a password on a smaller length password
# givenHash = "Vd693H7jroUcmcZV3RJ1S/" #pass = zzz; salt = hfT7jp2q

found = False

i = 0
start = time.time()
for x in range(1, 7):
    if found == True:
        break
    for combo in product(ascii_lowercase, repeat=x):
        i+=1
        potentialPassword = ''.join(combo)
        calculatedHash = MD5_crypt(potentialPassword, givenSalt)
        if calculatedHash == givenHash:
            print "Password: ", potentialPassword
            found = True
            break

end = time.time()

# print "\nTime Elapsed: ", end - start
print "Passwords Tested: ", i
print "\nPasswords Per Second: ", i / (end - start)
