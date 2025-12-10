#Get password from user
password = input("Enter your password: ")
#Let the program check length of password
length = len(password)
#Check Digit of password
hasDigit = False
hasUpper = False

for char in password:
    if char.isdigit():
        hasDigit = True
    if char.isupper():
        hasUpper = True

#Validating Strength of the password
if length < 6:
    print('Weak Password')
elif 6 < length < 10:
    print ('Medium Password')
elif length >10 and hasDigit and hasUpper:
    print ('Strong Password')
else:
    print('Please re-enter your password')