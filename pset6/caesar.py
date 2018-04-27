import sys

if len(sys.argv) != 2:
    print("Incorrect number of arguments")
    
    
else:
    # get an int key
    key = int(sys.argv[1])
    
    # grab plaint text
    print("plaintext: ", end="")
    plain = input()
    
    print("ciphertext: ", end="")
    
    # repeat for every char in string input
    for char in plain:
        
        # if alphabet
        if char.isalpha():
            
            # if lowercase
            if char.islower():
                
                # convert unicode char to int and apply key
                lower = chr((ord(char) - 97 + key) % 26 + 97)
                print(lower, end="")

            # if uppercase
            if char.isupper():
                upper = chr((ord(char) - 65 + key) % 26 + 65)
                print(upper, end="")

        # not alphabet
        else:
            print(char, end="")
            
    # new line
    print()

    
