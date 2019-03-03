# coding: utf8

#import unicodedata


alphabet = ''

for i in range(1000, 2000):
    letter = chr(i)#.encode('utf-8')
    #print(letter)
    alphabet += letter

print(alphabet.encode('utf-8'))

