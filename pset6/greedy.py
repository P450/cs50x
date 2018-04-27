def main():
    print("O hai! How much change is owed?")
    
    counter = 0
    
    # loop until input is totally valid
    while True:
        try:
            balance = askchange()
            
            # quarater
            change = balance % 25
            counter += (balance - change)/25
            
            # dime
            balance = change
            change = balance % 10
            counter += (balance - change)/10            

            # nickel
            balance = change
            change = balance % 5
            counter += (balance - change)/5
            
            # penny
            balance = change
            change = balance % 1
            counter += (balance - change)/1
            
            print(int(counter))
            return True

        # if non float is returned
        except Exception:
            print("Retry: ", end="")
            
            continue
    
    


# ask user for positive float input and return in cents
def askchange():
    
    # boolean check for positive input
    pos_input = False
    
    # loop until positive
    while not pos_input:
        dollars = float(input())
        if dollars > 0:
            pos_input = True
            break
        print("How much change is owed?")

                
    # convert to cents and round
    balance = round(dollars * 100, 0)

    return balance






if __name__ == "__main__":
    main()