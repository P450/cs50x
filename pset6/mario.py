
# declartion for valid height checker
valid_height = False

# loop until valid height
while not valid_height:
    print("Height: ", end="")
    height = int(input())

    # conditions for valid height
    if 0 < height and height < 24:
        valid_height = True

# for every line in height
for line in range(height):
    # put appropriate number of spaces and ampersands
    for i in range(height + 2 - line, 1, -1):
        print(" ", end="")
    for j in range(0, line + 2):
        print("#", end="")
    # skip line
    print()