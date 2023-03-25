#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   sigmageek_nvl3.py
@Time    :   2022/09/03
@Author  :   Felipe Maion 
@Version :   1.0
@Contact :   felipe.maion@gmail.com
@License :   MIT
@Desc    :   "Encontre o maior primo palíndromo na expansão decimal do π (3,1415…)"
            Find the biggest prime palindrome in the decimal expansion of π (3,1415…).
            
            ONLY 1 TRILLION DIGITS WERE CHECKED DUE TO LACK OF SUPPORT FOR Y-CRUNCHER FOR MAC (M1)
            
            
'''

import unittest
import asyncio
import logging
from aiohttp import ClientSession
import requests
import threading
import json
import sys
import os
import argparse
import traceback
from math import pi
import random
from datetime import datetime
from pathlib import Path

# https://pi2e.ch/blog/2017/03/10/pi-digits-download/#download
# https://api.pi.delivery/v1/pi?start=3743238221084&numberOfDigits=100&radix=10

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


def get_a_slice_of_pi_from_api(start=0, numberOfDigits=1000, radix=10):
    # was not useful since the numberOfDigits is max 1000.
    url = f"https://api.pi.delivery/v1/pi?start={start}&numberOfDigits={numberOfDigits}&radix={radix}"
    request = requests.get(url).json()
    return request["content"].replace(".", "")

async def fetch_html(session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    numberOfDigits = kwargs.get('numberOfDigits',"1000")
    start = kwargs.get('start',"0")
    radix = kwargs.get('radix',"10")
    url = f"https://api.pi.delivery/v1/pi?start={start}&numberOfDigits={numberOfDigits}&radix={radix}"
    
    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    print(f"Got response { resp.status } for URL: { url }", flush=True)
    html = await resp.text()
    return html


async def calc(start, n, session:ClientSession):
    data = await fetch_html(start=start, session=session)
    t = newThreadSearch(slice_index=start,data = data,size_n=n, debug=False)
    t.start()
    

async def bulk_crawl_and_write() -> None:
#     Got response 200 for URL: https://api.pi.delivery/v1/pi?start=1000014927000&numberOfDigits=1000&radix=10
# ERROR!! 429, message='Too Many Requests', url=URL('https://api.pi.delivery/v1/pi?start=1000013193000&numberOfDigits=1000&radix=10')
# as expected.
    total_pi_digits = int(100000000000000)
    lower = int(total_pi_digits/100)
    step = 100000000
    upper = lower + step
    i = lower
    async with ClientSession() as session:
        tasks = []
        while i < upper:
            tasks.append(
                calc(start=i, n=21, session=session)
            )
            if newThreadSearch.hasChanged: break
            i += 1000
        await asyncio.gather(*tasks)
        print(newThreadSearch.all_winners)
        
class newThreadRequest(threading.Thread):
    counter = 0
    def __init__(self,start=0, numberOfDigits=1000,radix=10):
        threading.Thread.__init__(self)
        self.data = ""
        self.startDigit = start
        self.numberOfDigits = numberOfDigits
        self.radix = radix
        newThreadRequest.counter += 1
        
    def run(self):
        # print("Starting: " + str(self.slice_index) + "\n")
        # process(data)
        self.data = get_a_slice_of_pi_from_api(start=self.startDigit, numberOfDigits=self.numberOfDigits, radix=self.radix)



def build_pi(big_pi, page=0):
    ## still slow.
    for j in range(0, 50000): # populate 50.000.000 digits of pi
        page += 1
        big_pi = big_pi + "" + get_a_slice_of_pi_from_api(start=1000*page, numberOfDigits=1000, radix=10)
    return big_pi, page
# tradeoff between speed and memory.
# computing the expansion of pi is slow, and we need to store the result in permanent memory.
# Also the int will overflow if we compute the expansion of pi to +100.000 digits.

def is_palindrome(s):
    s = str(s)
    # return str(s) == str(s)[::-1]
    length = len(s) 
    for i in range(int(length / 2)):
        if s[i] != s[length - i - 1]:
            return False
    return True


prime_list = [151978145606541879151, 999915579464975519999, 775486787555787684577, 359342190050091243953]

# Lower performance 
def is_prime(n):
    if n in prime_list : return True # Let's not loose time here. (checked also by wolfgram alpha)
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False
    for i in range(3, int(n**0.5)+1, 2):   # only odd numbers
        if n % i == 0:
            return False
    return True


####### miller-rabin for Prime performance
# https://youtu.be/8i0UnX7Snkc
# https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

# returns (x^y) % p
def power(x, y, p):
    res = 1
    # Update x if it is more than or
    # equal to p
    x = x % p
    while (y > 0):
         
        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p
 
        # y must be even now
        y = y>>1; # y = y/2
        x = (x * x) % p
     
    return res
 
# This function is called
# for all k trials. It returns
# false if n is composite and
# returns true if n is
# probably prime. d is an odd
# number such that d*2<sup>r</sup> = n-1
# for some r >= 1
def miillerTest(d, n):
     
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4)
 
    # Compute a^d % n
    x = power(a, d, n)
 
    if (x == 1 or x == n - 1):
        return True
 
    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n
        d *= 2
 
        if (x == 1):
            return False
        if (x == n - 1):
            return True
 
    # Return composite
    return False
 
# It returns false if n is
# composite and returns true if n
# is probably prime. k is an
# input parameter that determines
# accuracy level. Higher value of
# k indicates more accuracy.
def isPrime( n, k):
     
    # Corner cases
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
 
    # Find r such that n =
    # 2^d * r + 1 for some r >= 1
    d = n - 1
    while (d % 2 == 0):
        d //= 2
 
    # Iterate given number of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False
 
    return True

k = 40

print(isPrime(999915579464975519999, k))



def decimal_expansion_of_pi(n):
    return int(pi * (10**(n-1)))    



# file_name = "//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_02.txt"
# file_name = "//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_01.txt"
palindromes = []
def is_conditions_met_with(current_string, debug=True):
    if current_string:
        if is_palindrome(current_string): 
            if debug: print(f"[log] candidate: {current_string}")
            palindromes.append(current_string)
            # with open(f"palindromes.txt", 'w') as p:
            #     p.writelines(palindromes)
            #     print("\n\tPalindromes:")
            #     print(palindromes)
            # p.close()
            if isPrime(int(current_string),40):
                if debug:print(f"WINNER: {current_string}\n")
                return True
    return False


class newThreadSearch(threading.Thread):
    all_winners = []
    hasChanged = False
    counter = 0
    def __init__(self,slice_index, data, size_n,index_search = 0, debug = False, digits_counter=0, file_index=0):
        threading.Thread.__init__(self)
        self.data = data
        self.slice_index = slice_index
        self.index_search = index_search
        self.name = f"Thread-{slice_index}"
        self.n = size_n
        self.winners = []
        self.len_slice = len(data)
        self.debug = debug
        self.digits_counter = digits_counter
        self.file_index = file_index
        newThreadSearch.counter += 1
        
    def run(self):
        # print("Starting: " + str(self.slice_index) + "\n")
        # process(data)
        try: 
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
                
                if self.debug:

                    print(f"[log] {self.name} String: { current_string };  slice_index:{self.slice_index}; index_search:{self.index_search}; len(data): {self.len_slice}; Global Digits Counter: {self.digits_counter}")
                    print(f"[log] {self.name} String: { inverted_search }; slice_index:{self.slice_index}; index_search:{(self.len_slice - self.index_search)}; len(data): {self.len_slice}; Global Digits Counter: {self.digits_counter}")

                found = is_conditions_met_with(current_string, debug=self.debug)
                inverted_found = is_conditions_met_with(inverted_search, debug=self.debug)
                if found or inverted_found:             
                    if found:
                        if self.slice_index != 0:
                            pi_digit =  ((self.slice_index) * (self.len_slice-self.n) + self.index_search - self.n) - 1
                        else:
                            pi_digit = (self.slice_index * self.len_slice + self.index_search)
                        newThreadSearch.all_winners.append({"primePalindrome":current_string,"slice_index":self.slice_index, "index_search":self.index_search, "inverted":False, "len_slice": self.len_slice, "pi_digit":pi_digit, "digits_counter" : self.digits_counter, "file_index":self.file_index})
                        
                    if inverted_found:
                        if self.slice_index != 0:
                            pi_digit =  (self.slice_index * (self.len_slice - self.n) + (self.len_slice - 2*self.n - self.index_search)) -1
                        else:
                            pi_digit =  (self.len_slice - self.index_search) - self.n
                        newThreadSearch.all_winners.append({"primePalindrome":inverted_search, "slice_index":self.slice_index, "index_search":(self.len_slice - self.index_search), "inverted":True, "len_slice": self.len_slice, "pi_digit":pi_digit, "digits_counter" : self.digits_counter, "file_index":self.file_index })
                        
                    newThreadSearch.hasChanged = True

                self.index_search += 1
        except KeyboardInterrupt:
            print(f"\n Killed:\n\index_search= \t{self.index_search:,};\n\tlen(data)= \t{len(self.data):,};\n\tsize_n= \t{self.n:,}\n\tslice_index:{self.slice_index}")
        except Exception as e:
            print(f"\n ERROR: {e}\n\index_search= \t{self.index_search:,};\n\tlen(data)= \t{len(self.data):,};\n\tsize_n= \t{self.n:,}\n\tslice_index:{self.slice_index}")
        # print("Exiting: " + str(self.slice_index) + "\n")
        # if self.winners: 
        #     print(self.winners)
        # return self.winners


file_index = 11
# kwargs please...
def app(n=9, debug = 0, offset=0, slice_size=1024*1024, file_output="", file_input="", old_data = "", multi_file = False, file_index=file_index, file_name=f"//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_0{file_index}.txt", digits_counter = 0):
    if multi_file: print("Multi file support activated.")
    if file_output=="": file_output = f"pi_result_{n}.txt"
    if file_input=="": file_input = file_name
    
    print(f"file_input:{file_input}")
    print(f"file_output:{file_output} (if solution is found)")
    # print(f"file_name:{file_name}")
    # get n digits of the string representation of pi from the left.
    # move the search to the right by 1 digit at a time
    i = 0 # index of the chunk (slice) of pi read from the file.
    if debug == 0:
        debug = False
        int_debug = False
    elif debug == 1:
        debug = True
        int_debug = False
    elif debug == 2:
        debug = True
        int_debug = True
    # slice_size = n*1000*1000#*1024*1024
        
    print(f"Main: Finding prime palindromes inside pi with size n={n}")
    try:    
        print("Main: Loading pi...")
        with open(file_input) as f:
            print(f"Main: Each '.' represents a slice with {slice_size:,} digits of pi being processed. Offset={offset:,} digits")
            threads = []
            all_winners = ""
            
            while True:
                new_data = f.read(slice_size).rstrip('\x00')
                
                if not new_data:
                    break 
                if i == 0: 
                    new_data = new_data.replace(".", "")
                digits_counter += len(new_data)
                # find_all_palindrome_substrings(new_data)
                data = old_data + new_data # To avoid missing "solutions" hidden bitween slices.
                if file_index > 1 and i == 0: 
                    print(f"Old Data:{old_data}; New Data: {new_data[0:n]}...{new_data[-n:]} (size:{len(new_data)}) --> data: {data[0:n]}...{data[-n:]} (size:{len(data)})")
                print(".", end="", flush=True)
                old_data = data[-n:] # save the end for a new start.
                
                
                
                if digits_counter >= offset: #((i+1)*slice_size)
                    t = newThreadSearch(slice_index=i,data= data,size_n=n, debug=int_debug, digits_counter=digits_counter)
                    threads.append(t)
                    t.start()
                    
                i += 1
                if newThreadSearch.hasChanged: 
                    newThreadSearch.all_winners = sorted(newThreadSearch.all_winners, key=lambda d: d['pi_digit'])
                    newThreadSearch.hasChanged = False
                    all_winners = newThreadSearch.all_winners
                    if debug: print(f"\nMain: {datetime.now()} \nAll winners: " )
                    text_file = open(file_output, "w")
                    for winner in all_winners:
                        if debug: print(f"\t { winner }")
                        text_file.write(f"{winner}\n")
                    text_file.close()
            # If 100 trillions digits are over from file, wait processing to end:
            print("\nWaiting threads to finish processing.", end="\n")
            for index, thread in enumerate(threads):
                thread.join()
            print("Processing done.")
            print(f"Global Digits Counter:{digits_counter:,}")
        if multi_file:
            file_index += 1
            file_name = f"//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_0{file_index}.txt"
            print(f"Current Time: {datetime.now()}")
            print(f"File Index:{file_index}")
            print(f"OLD_DATA: {old_data}")
            app(n=n,debug=debug,offset=offset, slice_size=slice_size, multi_file=multi_file, old_data=old_data, file_output=file_output, file_index=file_index, file_input=file_name, digits_counter=digits_counter)
    except KeyboardInterrupt:
        print(f"\n Killed:\n\tslice_index= \t{i:,};\n\tlen(data)= \t{len(data):,};\n\tsize_n= \t{n:,}")
    except IOError:
        print(f"No input file found")
    except Exception as e:
        print(e)
        



maximumNumberOfThreads = 200
threadLimiter = threading.BoundedSemaphore(maximumNumberOfThreads)
       
class newThreadPalindrome(threading.Thread):     
    def __init__(self, data, slice_index, slice_size, palindrome_min_size, global_counter, file_id):
        threading.Thread.__init__(self)
        self.data = data
        self.palindromes = []
        self.palindrome_counter = 0
        self.size = palindrome_min_size
        self.global_counter = global_counter
        self.file_id = file_id
        self.slice_index = slice_index
        self.slice_size = slice_size
        
    def run(self):
        threadLimiter.acquire()
        try:
            self.palindrome_counter = self.find_all_palindrome_substrings(self.data)
        finally:
            threadLimiter.release()
            self.data = "" # free memory
            return self.palindromes
        

    def find_palindromes_in_sub_string(self, pi_string, j, k):
        count = 0
        
        while j >= 0 and k < len(pi_string):
            if pi_string[j] != pi_string[k]:
                break
            palindrome = pi_string[j: k + 1]
            palindrome_size = len(palindrome)
            if palindrome_size >= self.size:
                # dot_fix = 0 if int(self.file_id) == 1 else -1 #to be checked.
                pi_position = int(self.global_counter) - int(self.slice_size) - self.size + j + (int(self.file_id) - 1)*100000000000 + 1#+ dot_fix
                is_prime = isPrime(int(palindrome), 40)
                print(f"{datetime.now()} - {self.name} found palindrome: \t{palindrome};\t size:{palindrome_size},\t pi_position:{pi_position},\t isPrime:{is_prime}")
                self.palindromes.append({"palindrome":palindrome,"pi_position":pi_position, "j":j, "k":k, "size":palindrome_size, "global_counter":self.global_counter,"file_id":self.file_id, "slice_index":self.slice_index, "slice_size":self.slice_size, "is_prime":is_prime})
                json_data = json.dumps(self.palindromes)
                print("Saving this one...")
                
                Path(f"Threads-pi/{self.file_id}").mkdir(parents=True, exist_ok=True)
                thread_file = f"Threads-pi/{self.file_id}/{self.name}_big_palindromes_{self.file_id}.txt"
                with open(thread_file, "w") as f:
                    f.write(json_data)
                    f.close()
            # print(pi_string[j: k + 1])
                count += 1

            j -= 1
            k += 1

        return count

    def find_all_palindrome_substrings(self, pi_string):
        count = 0
        # for each char go up and down, even or odd:
        for i in range(0, len(pi_string)):
            count += self.find_palindromes_in_sub_string(pi_string, i - 1, i + 1)
            count += self.find_palindromes_in_sub_string(pi_string, i, i + 1)

        return count

def merge_palindromes_file_threads(output_file, file_id):
    rules = ["Thread", "big_palindromes", "txt"]
    files_to_merge = []
    palindromes = []
    # Will look for the files with the name pattern: "{self.name}_big_palindromes_{self.file_id}.txt" get the list of palindrome objects found by each thread in each instance.
    # And add them to the palindromes list.
    Path(f"Threads-pi/{file_id}").mkdir(parents=True, exist_ok=True)
    thread_dir = f"Threads-pi/{file_id}/"
    for fname in os.listdir(thread_dir):
        if all([rule in fname for rule in rules]):
            files_to_merge.append(fname)
            print(fname)
            with open(thread_dir + fname) as ffile:
                data = json.load(ffile)
                if not data: break
                for palindrome in data:
                    palindromes.append(palindrome)
    # Sort it be the biggest palindrome:
    try:
        palindromes = sorted(palindromes, key=lambda d: int(d['palindrome']), reverse=True)
        json_pal = json.dumps(palindromes)
        with open(output_file, "w") as main_file:
            main_file.write(json_pal)
            
        print(f"These ({len(files_to_merge)}) files threads were merged to '{main_file.name}'")
    except Exception as e:
        # print(palindromes)
        print(f"{e} traceback.format_exc(): {traceback.format_exc()}")
    finally:
        return palindromes

                        
# def appMaestro():
#     TotalDigits = 100000000000000 # One hundred trillion digits.
#     AlreadyChecked = 1000000000000 # One trillion already checked (10x100GB downloaded .txt)
#     LimitStorage = 400000000000 # 400GB
#     # go run ./cmd/extract -s 1457000000 -n 1000000000 > ComeçoEm1457000000ComFimEm2457000000.txt
    
    
    
    
#     pass           

        
def appPalindrome(size, file_input, slice_size, file_output, offset):
    # slice_size = n*1000*1000#*1024*1024
    if file_output=="": file_output = f"palindromes.txt"
    digits_counter = 0
    
    print(f"file_input: {file_input}")
    print(f"file_output: {file_output} (after merging thread files)")
    i = 0
    file_id = file_input[-7:-4].replace("_","0")
    print(f"file_id:{file_id}")
    old_data = ""
    print(f"Main: Finding palindromes inside pi.")
    try:    
        print("Main: Loading pi...")
        with open(file_input) as f:
            print(f"Main: Each 'Thread' represents a slice with {slice_size:,} digits of pi being processed. Offset={offset:,} digits")
            threads = []            
            while True:
                new_data = f.read(slice_size).rstrip('\x00')
                
                if not new_data:
                    break 
                if i == 0: 
                    new_data = new_data.replace(".", "")
                
                digits_counter += len(new_data)
                new_data = old_data + "" + new_data
                old_data = new_data[-size:]
                if digits_counter >= offset:
                    t = newThreadPalindrome(data=new_data,slice_index = i, slice_size=slice_size,palindrome_min_size=size, global_counter=digits_counter, file_id=file_id)
                    threads.append(t)
                    t.start()
            for thread in threads: # Wait to finishing processing threads.
                thread.join()
            palindromes = merge_palindromes_file_threads(file_output, file_id)
            return palindromes    
    except Exception as e:
        # print(palindromes)
        print(f"{e} traceback.format_exc(): {traceback.format_exc()}")
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
        
    # def test_app(self):
    #     self.assertEqual(app(9), '318272813') # Nivel 1: To be tested with n=9.
    # Nivel 2: solution:
        # https://api.pi.delivery/v1/pi?start=140672630233&numberOfDigits=1000&radix=10
    #Nv3; {"palindrome": "38898292453535429289883", "pi_position": 2143728293286, "j": 293306, "k": 293328, "size": 23, "global_counter": 43728750000, "file_id": "22", "slice_index": 0, "slice_size": 750000, "is_prime": true}
            

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--digits",
                        required=True,
                        default=None,
                        help="(Minimum) Number of digits to look for the (prime) palindrome")
    parser.add_argument("-o", "--offset",
                        required=False,
                        default=0,
                        help="Don't process data until offset digit position is reached")
    parser.add_argument("-s", "--size",
                        required=False,
                        default=100000,
                        help="Size of the slice of data read from pi to be analized by a thread")
    parser.add_argument("-v", "--verbose",
                        required=False,
                        default=1,
                        help="0-> No verbose. 1-> Only results. 2-> Processing (slow)")
    parser.add_argument("-of", "--output",
                        required=False,
                        default="",
                        help="Output file for results")
    parser.add_argument("-if", "--input",
                        required=False,
                        default="",
                        help="Input file with pi digits")
    parser.add_argument("-pa","--palindrome",
                        required=False,
                        default=0,
                        help="Palindrome mode only. Only look for Palindromes. Not primes. Default 0:OFF; 1:To turn ON.")
    parser.add_argument("-ppfc", "--primepalindromefilechecker",
                       required=False,
                       default=0,
                       help="Default (0). If 1 then the --input <file> (palindromes.txt as default) from the palindrome mode (-pa) will be checked for primes.")
    parser.add_argument("-mf", "--multifile",
                        required=False,
                        default=0,
                        help="O: False, 1: True. Multi File Support (see code comments)") # the support is for files located in the forlder and format below:
    file_index = 11
    # I don't know how to add support to this in the terminal (args) ToDo: revisit it someday.
    file_name = f"//Volumes//SSD//pi-delivery//pi_dec_1t_{file_index}.txt"
   
    
    
    try:
        args = parser.parse_args()
        argv = sys.argv[1:]
        if len(argv) > 0:
            
            size = int(args.digits)
            offset = int(args.offset)
            debug = int(args.verbose)
            slice_size = int(args.size) #1000*size
            file_output = args.output
            file_input = args.input
            multi_file = [False, True][int(args.multifile)]
            palindrome_mode = [False, True][int(args.palindrome)]
            primepalindromefilechecker = [False, True][int(args.primepalindromefilechecker)]
            initial_time = datetime.now()
            print(f"Main: {initial_time}")
            #web mode is out:
            # asyncio.run(bulk_crawl_and_write()) # ERROR!! 429, message='Too Many Requests', url=URL('https://api.pi.delivery/v1/pi?start=1000013193000&numberOfDigits=1000&radix=10')
            if palindrome_mode:
                if file_input =="": 
                    print("\tERROR:Please provide a file source for pi with --input/-if <file.txt>")
                    file_input ="//Volumes//SSD//bigpi//pi_dec_1t//pi_dec_1t_01.txt"
                    print(f"\tTrying to use '{ file_input }' as source.")
                if multi_file:
                    print("\tMulti file not supported with Palindrome Mode (yet)")
                    print("\tConsider running instances in parallel, one for each file as input.")
                          
                appPalindrome(size, file_input,slice_size=slice_size, offset=offset, file_output=file_output)
            if primepalindromefilechecker:
                if file_input == "": file_input = "palindromes.txt"
                if file_output == "": file_output = "prime_palindromes.txt"
                with open(file_input) as file:
                    palindromes = json.load(file)
                primes = []
                
                for p in palindromes:
                    print(f"Checking: {p['palindrome']} ")
                    if isPrime(int(p['palindrome']),k):
                        print("Prime: ", p)
                        primes.append(p)
                json_data = json.dumps(primes)
                with open(file_output, "w") as prime_file:
                    prime_file.write(json_data)
                    
            if not palindrome_mode and not primepalindromefilechecker:    
                app(size, debug=debug, offset=offset, slice_size=slice_size, file_output=file_output, file_input=file_input, multi_file=multi_file, file_index=file_index, file_name=file_name)
            
        
    except Exception as e:
        print(f"ERROR!! {e} traceback.format_exc(): {traceback.format_exc()}")
        
    final_time = datetime.now()
    print(f"Main: {final_time}")
    print(f"Total running time: {final_time - initial_time}")
    # unittest.main()
    