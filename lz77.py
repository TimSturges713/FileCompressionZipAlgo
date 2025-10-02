"""
filename: lz77.py

@author: Timothy Sturges

The compression and decompression functions of my personal implementation
of the LZ77 algorithm in Python.
"""

import struct

WINDOW_SIZE = 255
LOOK_AHEAD = 18                 # size of lookahead
SEARCH_BUFFER = 255 - 18       # size of the search buffer


"""
Compresses a textfile using the LZ77 algorithm.

@param filename     the path of the file to compress

@return pointers    the list of the corresponding LZ77 compressed pointers to the text file
"""
def compress(filename:str):
    pointers = []               # the array of pointers to represent the compressed data (tuples)
    with open(filename) as file:    # open the file provided
        data = file.read()          # access all text from the file        
    pos = 0
    while pos < len(data):
        # Define the sliding windows
        lookAhead = data[pos : pos + LOOK_AHEAD]
        searchBuffer = data[max(0, pos - SEARCH_BUFFER) : pos]

        # Find the longest match
        match = longestMatch(searchBuffer, lookAhead, len(searchBuffer), len(lookAhead))
        pointers.append(match)

        # Extract offset/length/nextChar from the packed 24-bit integer
        offset = match >> 16
        length = (match >> 8) & 0xFF
        next_char = match & 0xFF

        # Slide window forward
        pos += length + 1
    return pointers
            
            
            
            
"""
Finds the longest repeating subsequence present in the search buffer compared to the look ahead buffer.

@param searchBuffer     sequence of characters from file of length SEARCH_BUFFER
@param lookAhead        sequence of characters from file of length LOOK_AHEAD

@return longestSub      a tuple of format (offset, length, next char) that makes the algorithm function properly
"""
def longestMatch(searchBuffer, lookAhead, searchLen, lookLen):
    longestSub = ord(lookAhead[0])   # the tuple representing the pointer to the longest matching subseq, default
    if(searchLen == 0):             # if there's no search buffer yet, then there's no longest match, return
        return longestSub
    tmp = ''                 # sets the first part of longest sequence
    l = 1                               # initial length of sequence
    for i in range(lookLen):         # go through the look ahead buffer
        tmp += lookAhead[i]           # if found, increase the size of tmp to find a bigger one possibly
        flag = False
        for j in range(l, searchLen+1):  # go through the search buffer backwards 
            if(l == 1):             # to avoid index out of bounds for substring slices
                if(searchBuffer[searchLen-j] == tmp):   # backwards as seen here, if rightmost is a match to the tmp subseq then it's the longest 
                    if(i + 1 == lookLen): 
                        if i + 1 < lookLen:   # still inside lookAhead
                            next_char = ord(lookAhead[i+1])
                        else:
                            next_char = 0     # or pick a sentinel, e.g. 0 meaning "no next char"
                        pt = (j << 16) | (l << 8) | next_char
                        longestSub = pt

                        longestSub = pt
                    else:                   
                        if i + 1 < lookLen:   # still inside lookAhead
                            next_char = ord(lookAhead[i+1])
                        else:
                            next_char = 0     # or pick a sentinel, e.g. 0 meaning "no next char"
                        pt = (j << 16) | (l << 8) | next_char
                        longestSub = pt

                        longestSub = pt
                    l += 1                  # length increased by 1 since longer subseq is found
                    flag = True             # longer subseq found at this length
                    break                   # move on to the next highest length
            else:
                
                if(searchBuffer[searchLen-j:searchLen-j+l] == tmp):   # backwards as seen here, if rightmost is a match to the tmp subseq then it's the longest
                    if(i + 1 == lookLen):
                        
                        if i + 1 < lookLen:   # still inside lookAhead
                            next_char = ord(lookAhead[i+1])
                        else:
                            next_char = 0     # or pick a sentinel, e.g. 0 meaning "no next char"
                        pt = (j << 16) | (l << 8) | next_char
                        longestSub = pt
                    else:                   
                        if i + 1 < lookLen:   # still inside lookAhead
                            next_char = ord(lookAhead[i+1])
                        else:
                            next_char = 0     # or pick a sentinel, e.g. 0 meaning "no next char"
                        pt = (j << 16) | (l << 8) | next_char
                        longestSub = pt

                        longestSub = pt
                    l += 1                  # length increased by 1 since longer subseq is found
                    flag = True             # longer subseq found at this length
                    break                   # move on to the next highest length
        if(flag == False):              # if no higher subseq found, no need to continue
            break
        
    return longestSub


"""
Decompresses a textfile using the LZ77 algorithm.
"""
def decompress(pointers):
    finalAnswer = ""

    for pointer in pointers:
        offsetAndLength = pointer
        
        tmp = offsetAndLength
        tmp = tmp >> 16
        offset = tmp
        tmp = offsetAndLength
        tmp = tmp >> 8
        tmp = tmp & 0xFF
        length = tmp
        tmp = offsetAndLength
        tmp = tmp & 0xFF
        nextChar = tmp
          
        for i in range(length):
            finalAnswer += finalAnswer[len(finalAnswer)-offset]
        if nextChar != 0:
            finalAnswer += chr(nextChar)
    return finalAnswer

def decompressionProcessing(filename):
    with open(filename, "rb") as f:
                pointers = []
                while True:
                    chunk = f.read(3)
                    if not chunk:
                        break             
                    if len(chunk) != 3:
                        raise EOFError(f"Incomplete token: expected 3 bytes, got {len(chunk)}")
                    offset, length, next_byte = struct.unpack(">BBB", chunk)
                    pointer = (offset << 16) | (length << 8) | next_byte
                    pointers.append(pointer)    
                englishAnswer = decompress(pointers)
            
                try:
                    with open(filename[:len(filename)-4] + ".txt", "w") as write:
                        write.write(englishAnswer)
                except:
                    f = open(filename[:len(filename)-4] + ".txt", "x")
                    f.close()
                    with open(filename[:len(filename)-4] + ".txt", "w") as write:
                        write.write(englishAnswer)

def compressionProcessing(filename):
    pointers = compress(filename)
    name = filename[:len(filename)-4]
    try:
        with open(name + ".tim", "wb") as write:
            for pointer in pointers:
                offset = pointer >> 16
                length = (pointer >> 8) & 0xFF
                next_char = pointer & 0xFF
                write.write(struct.pack(">BB", offset, length))
                write.write(struct.pack("B", next_char))  
    except: 
        f = open(name + ".tim", "x")
        f.close()
        with open(name + ".tim", "wb") as write:
            for pointer in pointers:
                offset = pointer >> 16
                length = (pointer >> 8) & 0xFF
                next_char = pointer & 0xFF
                write.write(struct.pack(">BB", offset, length))
                write.write(struct.pack("B", next_char))   

def main():
    print("Welcome to the text file compression software!")
    compOrDecomp = input("Do you want to compress (0) or decompress (1) a text file? Enter 0 or 1:")
    if compOrDecomp == "0":
        while True:
            try:
                while True:
                    filename = input("Enter the path of the text file to compress:")
                    if filename[len(filename)-4:] == ".txt":
                        break
                    else:
                        print("Please enter a valid .txt file path")
                compressionProcessing(filename)
                break
            except:
                print("Please try a valid .txt file path")
                continue
        print("Compressed into " + filename[:len(filename)-4] + ".tim successfully!")
    else: 
        while True:
            try:
                while True:
                    filename = input("Enter the path of the .tim file to decompress:")
                    if filename[len(filename)-4:] == ".tim":
                        break
                    else:
                        print("Please enter a valid .tim file path")
                decompressionProcessing(filename)
                break
            except:
                print("Please try a valid .tim file path")
                continue
                
            
        print("Decompressed into " + filename[:len(filename)-4] + ".txt successfully!")


if __name__ == "__main__":
    main()