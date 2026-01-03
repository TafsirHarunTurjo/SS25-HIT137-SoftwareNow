'''
Question 1 Write a program that asks the user to input a password and checks its strength.
• Weak: Less than 6 characters
• Medium: 6-10 characters and contains at least one digit
• Strong: More than 10 characters and contains at least one digit and at least one uppercase letter
Example:
Input: "hello123"
Output: "Medium password" 
'''

# takes input(password) from user
password = input("\nEnter your password. ")

def check_password_strength(password):
    """
    this function classify a password as Weak, Medium or Strong.

    it expects 1 parameter 

    rules:
    - Weak   : less than 6 characters
    - Medium : length 6–10 (inclusive) AND contains at least one digit
    - Strong : length > 10 AND contains at least one digit AND at least one uppercase letter
    - Invalid : try new password again (eg: rameshrai)

    example:
    - Input: "Ramesh123"
    - Output: "Medium password" 

    """

    # finds length of the password
    length_of_password = len(password)

    # checks any digit in password
    has_digit = any(char.isdigit() for char in password)              

    # checks any uppercase in password
    has_uppercase = any(char.isupper() for char in password)

    # control flow start

    if length_of_password < 6:
        return 'Weak password'

    elif (6 <= length_of_password <= 10) and has_digit == True:              # Note:can be done by import re, re.search(r'')
        return 'Medium password'

    elif (length_of_password > 10) and (has_digit == True) and (has_uppercase == True):
        return 'Strong password'

    else:
        # Invalid password
        print('\nInvalid password.Try next password again.')
        next_password = input('\nEnter another valid password ')
        return check_password_strength(next_password) # call function 
            
    # control flow end

result = check_password_strength(password)
print(f'"{result}"') # final output