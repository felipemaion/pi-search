# pi-search-palindromes
This was the first SigmaGeek challenge ,which involved 4 phases: 

Phase 1: What is the first 9-digit palindromic prime found in the decimal expansion of Pi? 

1023 competitors passed this phase and found the right number: 318272813

Phase 2: What is the first 21-digit palindromic prime found in the decimal expansion of Pi? 

152 passed this phase and found the right number: 151978145606541879151 

Phase 3: What is the largest palindromic prime found in the decimal expansion of Pi? 

26 passed this phase and found the right number: 9609457639843489367549069 

Final Phase: What is the next number in the sequence? 

961212169
102454201
337515733
347676743
?


## Position
After tha challenge ended, I was informed that my position was 87th. 
Not bad for my first coding challange.

## USAGE EXAMPLE:

```python autopi.py -s /Volumes/SSD/pi-delivery -i 111 -m 5```

Where: 
    "-s" or "--storage" is the Folder to store 100GB of Pi" (THIS WILL BE UPDATED)
    "-i" or "--index" is the start Index: 1 == first 100B digits
    "-m","--mod" is how many terminals will be processing in parallel. So it will increment Index by mod terminals.