#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   sigmageek_nvl1.py
@Time    :   2022/08/19
@Author  :   Felipe Maion 
@Version :   1.0
@Contact :   felipe.maion@gmail.com
@License :   MIT
@Desc    :   "Encontre o primeiro primo palíndromo de 21 dígitos na expansão decimal do π (3,1415…)"
            Find the first 12-digit palindrome prime number in the decimal expansion of π (3,1415…).
'''
import unittest
from math import pi
import requests

# https://pi2e.ch/blog/2017/03/10/pi-digits-download/#download
# https://api.pi.delivery/v1/pi?start=3743238221084&numberOfDigits=100&radix=10



def get_a_slice_of_pi_from_api(start=0, numberOfDigits=1000, radix=10):
    # was not useful since the numberOfDigits is max 1000.
    url = f"https://api.pi.delivery/v1/pi?start={start}&numberOfDigits={numberOfDigits}&radix={radix}"
    request = requests.get(url).json()
    return request["content"].replace(".", "")

def build_pi(big_pi, page):
    ## still slow.
    for j in range(0, 50000): # populate 50.000.000 digits of pi
        page += 1
        big_pi = big_pi + get_a_slice_of_pi_from_api(start=1000*page, numberOfDigits=1000, radix=10)
    return big_pi, page
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


file_name = "//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_01.txt"


def is_conditions_met_with(current_string, debug=True):
    if current_string:
        if is_palindrome(current_string): 
            if debug: print(f"[log] candidate: {current_string}")
            if is_prime(int(current_string)):
                print(f"WINNER: {current_string}\ni:")
                return True
    return False





def app(n=9, debug = False, offset=0):
    # get n digits of the string representation of pi from the left.
    # move the search to the right by 1 digit at a time
    i = 0 # number of chunks of pi read from the file.
    winners = {}

    big_pi = ""
    
        
    print(f"Finding prime palindromes inside pi with size n={n}")
        
    with open(file_name) as f:
        print("Loading pi...")
        print(f"Each '.' represents {n}*1024*1024 digits of pi:")
        while True:
            data=f.read(n*1024*1024)
            if i == 0: data = data.replace(".", "")
            
            if not data:
                # break # might have big_pi data to analyze.
                data = ""
            big_pi += data
            len_big_pi = len(big_pi)
            print(".", end="", flush=True)
            j = 0 # position of the search in the current chunk of pi.
            # [log] String: 025748214449257865146 Size Pi ==> i: 4947676 * 1024: 5066420224
            # [log] String: 257482144492578651463 Size Pi ==> i: 4947677 * 1024: 5066421248
            # [log] String: 574821444925786514631 Size Pi ==> i: 4947678 * 1024: 5066422272
            # Rescue point: I've analized 4933470 * 1024 digits of pi.
            # 
            hasdata = True if i > offset else False
            while hasdata:
                # If we are running out of digits, we need to get more.
                if (j+n) > len(big_pi):
                    # only keeping at RAM what was not analyzed:
                    big_pi = big_pi[j:j+n] 
                    hasdata=False
                    break #hasdata.
                
                current_string = big_pi[j:j+n]
                inverted_search = big_pi[-(1+j):-(n+j+1):-1]
                
                if debug: print(f"[log] String: { current_string } i:{i}; j:{j}; len(big_pi): {len(big_pi)}")
                
                if is_conditions_met_with(current_string) or is_conditions_met_with(inverted_search):
                    #save result to file:
                    text_file = open(f"pi_result_{n}.txt", "w")
                    
                    if is_conditions_met_with(current_string): 
                        text_file.write(current_string)
                        winners[current_string] = {"i":i, "j":j, "inverted":False, "len_big_pi": len_big_pi }
                        text_file.close()
                        print(winners)
                        return current_string
                    if is_conditions_met_with(inverted_search): 
                        text_file.write(inverted_search)
                        winners[inverted_search] = {"i":i, "j":j, "inverted":True, "len_big_pi": len_big_pi }
                        text_file.close()
                        print(winners)
                j += 1
            i += 1
# 3.020.482.560
# 5.021.579.264
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
        scrap_pi = get_a_slice_of_pi_from_api(start=0, numberOfDigits=100, radix=10)
        self.assertEqual(decimal_expansion_of_pi(10), int(scrap_pi[:10]))
        self.assertEqual(decimal_expansion_of_pi(5),int(scrap_pi[:5]))
        
    def test_app(self):
        self.assertEqual(app(9), '318272813') # Nivel 1: To be tested with n=9.
            

if __name__ == '__main__':
    
    # app(21, debug=False, offset=4947676)
    app(9, debug=False, offset=0)
    app(21, debug=False, offset=1000)
    # unittest.main()
    