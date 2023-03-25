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
import threading

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

def is_palindrome(s):
    s = str(s)
    # return str(s) == str(s)[::-1]
    length = len(s) 
    for i in range(int(length / 2)):
        if s[i] != s[length - i - 1]:
            return False
    return True
  
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


def is_conditions_met_with(current_string, debug=False):
    if current_string:
        if is_palindrome(current_string): 
            if debug: print(f"[log] candidate: {current_string}")
            if is_prime(int(current_string)):
                if debug:print(f"WINNER: {current_string}\n")
                return True
    return False


class newThreadSearch(threading.Thread):
    all_winners = []
    hasChanged = False
    counter = 0
    def __init__(self,slice_index, data, size_n,index_search = 0):
        threading.Thread.__init__(self)
        self.data = data
        self.slice_index = slice_index
        self.index_search = index_search
        self.name = f"Thread-{slice_index}"
        self.n = size_n
        self.winners = []
        self.len_slice = len(data)
        newThreadSearch.counter += 1
        
    def run(self, debug=False):
        # print("Starting: " + str(self.slice_index) + "\n")
        # process(data)
        
        hasdata = True 
        while hasdata:
            # already looked half up and down.
            if (self.index_search) > (self.n + len(self.data)/2):
                # only keeping at RAM what was not analyzed:
                self.data = self.data[self.index_search:self.index_search+self.n] 
                # print(self.data)
                hasdata=False
                break #hasdata.
            
            current_string = self.data[self.index_search:self.index_search+self.n]
            inverted_search = self.data[-(1+self.index_search):-(self.n+self.index_search+1):-1]
            
            if debug: print(f"[log] String: { current_string } i:{self.slice_index}; self.index_search:{self.index_search}; len(self.data): {self.len_slice}")
            
            if is_conditions_met_with(current_string) or is_conditions_met_with(inverted_search):
                #save result to file:
                # text_file = open(f"pi_result_{self.n}_{self.slice_index}.txt", "w")
                
                if is_conditions_met_with(current_string): 
                    # text_file.write(current_string)
                    newThreadSearch.all_winners.append({"winner":current_string,"slice_index":self.slice_index, "index_search":self.index_search, "inverted":False, "len_slice": self.len_slice })
                    newThreadSearch.hasChanged = True
                    # text_file.close()
                    # print(newThreadSearch.all_winners)
                    
                if is_conditions_met_with(inverted_search): 
                    # text_file.write(inverted_search)
                    newThreadSearch.all_winners.append({"winner":inverted_search, "slice_index":self.slice_index, "index_search":(self.len_slice - self.index_search), "inverted":True, "len_slice": self.len_slice })
                    newThreadSearch.hasChanged = True
                    # text_file.close()
                    # print(self.winners)
            self.index_search += 1
        # print("Exiting: " + str(self.slice_index) + "\n")
        # if self.winners: 
        #     print(self.winners)
        # return self.winners

def app(n=9, debug = False, offset=0):
    # get n digits of the string representation of pi from the left.
    # move the search to the right by 1 digit at a time
    i = 0 # number of chunks of pi read from the file.

    slices_sizes = n*1000*1000#*1024
        
    print(f"Finding prime palindromes inside pi with size n={n}, offset={offset}")
        
    with open(file_name) as f:
        print("Loading pi...")
        print(f"Each '.' represents a slice with {slices_sizes} digits of pi being processed.")
        threads = []
        all_winners = ""
        old_data = ""
        while True:
            new_data = f.read(slices_sizes)
            if not new_data:
                break 
            if i == 0: new_data = new_data.replace(".", "")
            data = old_data + new_data # To avoid missing "solutions" hidden bitween slices.
            print(".", end="", flush=True)
            if i > offset:
                t = newThreadSearch(i,data,n)
                threads.append(t)
                t.start()
                old_data = data[-n:] # save the end for a new start.
            i += 1
            if newThreadSearch.hasChanged: 
                newThreadSearch.all_winners = sorted(newThreadSearch.all_winners, key=lambda d: d['slice_index'])
                newThreadSearch.hasChanged = False
                all_winners = newThreadSearch.all_winners
                print(f"All winners: { all_winners } " )
        # If 100 trillions digits are over from file, wait processing to end:
        for index, thread in enumerate(threads):
            print(f"Main    : before joining thread {index} .")
            thread.join()
            print(f"Main    : thread {index} done")
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
    # app(9, debug=False, offset=0)
    app(21, debug=False, offset=0)
    # unittest.main()
    
