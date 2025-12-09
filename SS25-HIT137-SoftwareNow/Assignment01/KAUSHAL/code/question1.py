# Question 1
# Write a program that asks the user to input a password and checks its strength.
# • Weak: Less than 6 characters
# • Medium: 6-10 characters and contains at least one digit
# • Strong: More than 10 characters and contains at least one digit and at least one
# uppercase letter
# Example:
# Input: "hello123"
# Output: "Medium password"

# taking input(password) from the user
password = input("\tEnter your password.")

# function to check strength of password
def check_password_strength(password):

    # finding the length of the password
    length_of_password = len(password)

    # check if there are any digit in the given password
    has_digit = any(char.isdigit() for char in password)              

    # check if there are any uppercase in the given password
    has_uppercase = any(char.isupper() for char in password)

    # control flow start

    # length of password less than 6
    if length_of_password < 6:
        return 'Weak password'

    # length of password between 6 and 10 (included) and has at least one digit
    elif (6 <= length_of_password <= 10) and has_digit == True:              # Note:can be done by import re, re.search(r'')
        return 'Medium password'

    # length of password greater than 10 and has at least one digit & at least one uppercase
    elif (length_of_password > 10) and (has_digit == True) and (has_uppercase == True):
        return 'Strong password'

    else:
        # If one enter invalid password (example: wfsgwyw -> more than 6 char but no single digit), then try next password.
        print('\nInvalid password.Try next password again.')
        next_password = input('\nEnter another valid password ')
        return check_password_strength(next_password) # call function again
            
    # control flow end

result = check_password_strength(password)
print(f'"{result}"')