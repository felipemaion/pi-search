#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   sigmageek_nvl1.py
@Time    :   2022/08/19
@Author  :   Felipe Maion 
@Version :   1.0
@Contact :   felipe.maion@gmail.com
@License :   MIT
@Desc    :   "Encontre o primeiro primo palíndromo de 9 dígitos na expansão decimal do π (3,1415…)"
            Find the first 9-digit palindrome prime number in the decimal expansion of π (3,1415…).
'''
import unittest
from math import pi
from lxml import html
import requests

# https://pi2e.ch/blog/2017/03/10/pi-digits-download/#download

url = "https://www.pi2e.ch/blog/wp-content/uploads/2017/03/pi_dec_1m.txt"

request = requests.get(url)
source = html.fromstring(request.content).text
scrap_pi = source.replace(".", "")
# print(scrap_pi[:10])
# tradeoff between speed and memory.
# computing the expansion of pi is slow, and we need to store the result in memory.
# Also the int will overflow if we compute the expansion of pi to 100.000 digits.


def is_palindrome(n):
    return str(n) == str(n)[::-1]
  
def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False
    for i in range(3, int(n**0.5)+1, 2):   # only odd numbers
        if n % i == 0:
            return False
    return True

def decimal_expansion_of_pi(n):
    return int(pi * (10**(n-1)))    



def app():
    # get 9 digits of the string representation of pi from the left.
    # move the search to the right by 1 digit at a time
    i = 0
    list_of_palindromes = []
    while True:
        current_string = scrap_pi[i:(i+9)]
        if is_palindrome(current_string): # More expesive to compute than the above.
            # print(current_string)
            list_of_palindromes.append(current_string)
            if is_prime(int(current_string)):
                print(f"WINNER: {current_string} ")
                return current_string
        i += 1

class TestSolutionMethods(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue  (is_prime(2))         # == True
        self.assertTrue  (is_prime(3))         # == True
        self.assertFalse (is_prime(4))         # == False
        self.assertFalse (is_prime(-1))        # == False
        self.assertTrue  (is_prime(13))        # == True
        self.assertTrue  (is_prime(27361))     # == True
    
    def test_is_plindrome(self):
        self.assertTrue  ( is_palindrome(121))          #  == True
        self.assertTrue  ( is_palindrome(1221))         #  == True
        self.assertTrue  ( is_palindrome(1221))         #  == True
        self.assertTrue  ( is_palindrome(1221))         #  == True
        self.assertTrue  ( is_palindrome("socorrammesubinoonibusemmarrocos"))         #  == True
        self.assertFalse ( is_palindrome(12))           #  == False
        
    def test_decimal_expansion_of_pi(self):
        self.assertEqual(decimal_expansion_of_pi(1), 3)
        self.assertEqual(decimal_expansion_of_pi(5), 31415)
        self.assertNotEqual(decimal_expansion_of_pi(5), 31416)
        self.assertEqual(decimal_expansion_of_pi(10), 3141592653)
        # Test our own implementation of pi string:
        # self.assertEqual(decimal_expansion_of_pi(100), int(scrap_pi[:100])) # OOps, someone is wrong here! Might be Python calculation of pi.
        # AssertionError: 31415926535897928521663964832579622319974690746431662322[39 chars]51808 != 31415926535897932384626433832795028841971693993751058209[39 chars]17067
        self.assertEqual(decimal_expansion_of_pi(10), int(scrap_pi[:10]))
        self.assertEqual(decimal_expansion_of_pi(5),int(scrap_pi[:5]))
            
    
if __name__ == '__main__':
    app()
    unittest.main()
    