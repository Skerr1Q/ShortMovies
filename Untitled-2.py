x = input("write a number")

def check_p(x):    
    y = str(x)
    i = 0
    while i != (len(y)/2):
        if y[i] == y[i - 1]:
            i =+ 1
        else:
            return ("not a palindrome")
    return ("palindrome")

print(check_p(x))
