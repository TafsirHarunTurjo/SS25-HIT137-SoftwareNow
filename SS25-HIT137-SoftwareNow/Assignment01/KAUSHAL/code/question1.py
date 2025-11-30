# Question 1
# Write a program that asks the user to input a password and checks its strength.
# • Weak: Less than 6 characters
# • Medium: 6-10 characters and contains at least one digit
# • Strong: More than 10 characters and contains at least one digit and at least one
# uppercase letter
# Example:
# Input: "hello123"
# Output: "Medium password"

# Taking input(password) from the user.
password = input("Enter your password.")
length_of_password = len(password)
has_digit = any(char.isdigit() for char in password)          #Note:can be done by import re, re.search(r'')
has_uppercase = any(char.isupper() for char in password)

if length_of_password < 6:
    print('Weak password')

elif (6 <= length_of_password <= 10) and has_digit == True:
    print('Medium password')

elif (length_of_password > 10) and (has_digit == True) and (has_uppercase == True):
    print('Strong password')

else:
    print('Invalid password.Try again.')