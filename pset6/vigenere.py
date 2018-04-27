import sys

def main():
    # ensure correct command line
    if len(sys.argv) != 2 or not sys.argv[1].isalpha():
        print("Key must be a single alphabetic string")
    
    else:
        # input
        print("plaintext: ", end="")
        plain = input()
        
        # output
        print("ciphertext: ", end="")
        
        # variable declaration
        key = []
        counter = 0
        keyLength = len(sys.argv[1])

        # convert key to int then store
        for i in (sys.argv[1]):
            key.append(keygen(i))
        
        # iterate over plaintext
        for char in plain:
            if char.isalpha():
                if char.isupper():
                    upper = chr( ((ord(char) - 65) + (key[counter % keyLength]) ) % 26 + 65)
                    print(upper, end="")

                elif char.islower():
                    lower = chr(( (ord(char) - 97) + (key[counter % keyLength]) ) % 26 + 97)
                    print(lower, end="")
                counter += 1
                
            else:
                print(char, end="")

        print()    


def keygen(char):
    # zero-index the key (i.e. 0 - 25)
    return ord(char.upper()) - 65



if __name__ == "__main__":
    main()
