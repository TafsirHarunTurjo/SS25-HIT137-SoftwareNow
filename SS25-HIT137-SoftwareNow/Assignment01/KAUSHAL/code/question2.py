# Question 2
# Write a program that finds all prime numbers up to a given limit (maximum 100), and
# display:
# • the total count of prime numbers found
# • the smallest and largest prime number in the range
# • the sum of all prime numbers found
# Example:
# Input: 20
# Output:
# Prime numbers found: 2 3 5 7 11 13 17 19
# Total primes found: 8
# Largest prime: 19
# Smallest prime: 2
# Sum of all primes: 77

# take input (max limit for prime numbers) from user
given_limit = int(input('\tEnter the given limit for the prime number (max 100) '))

# if given limit is greater than 100, then retake the input within the limit
while given_limit > 100:
    given_limit = int(input('\tYour maximum limit is 100. Enter value within the limit '))

# function for prime number
def prime_number(given_limit):
    list_prime = [] #initialize empty list
    sum_prime = 0
    for i in range(2, given_limit + 1):
        count = 0
        for j in range(1,i+1):
            if i % j == 0:
                count = count + 1
        if count == 2:   # prime number is divisible by itself and 1.So, when count is exactly 2, its prime.  
            list_prime.append(i) # putting all prime numbers one by one in the list
            sum_prime = sum_prime + i
    
    print("Prime numbers found: ", *list_prime) # * is for unpacking the list
    print(f'Total primes found: {len(list_prime)}')
    print(f'Largest prime: {max(list_prime)}')
    print(f'Smallest prime: {min(list_prime)}')
    print(f'Sum of all primes: {sum_prime}')

prime_number(given_limit) # function call
