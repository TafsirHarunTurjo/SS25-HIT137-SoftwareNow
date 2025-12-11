'''
Question 2 Write a program that finds all prime numbers up to a given limit (maximum 100), and
display:
• the total count of prime numbers found
• the smallest and largest prime number in the range
• the sum of all prime numbers found
Example:
Input: 20
Output:
Prime numbers found: 2 3 5 7 11 13 17 19
Total primes found: 8
Largest prime: 19
Smallest prime: 2
Sum of all primes: 77
'''

def is_prime(n):
    """
    it return True if n is a prime number (n >= 2), otherwise False.
    it expects 1 parameter 
    only need to check up to the square root of n

    """
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


"""
ask input within given limit (2-100), otherwise give error message and ask for another value

"""
while True:
    raw_input = input("Enter any value between 2 to 100 (inclusive): ")
    try:
        limit = int(raw_input)
        if 2 <= limit <= 100:
            break
        else:
            print("Error: value must be between 2 and 100.")
    except ValueError:
        print("Error: please enter a whole number.")

# finds all prime numbers up to the limit
primes = []
for number in range(2, limit + 1):
    # call is_prime function
    if is_prime(number):
        primes.append(number) # append number to the primes (list)

# total primes, smallest, largest and sum of prime
total_primes = len(primes)
smallest_prime = primes[0]
largest_prime = primes[-1]
sum_of_primes = sum(primes)

# output section (as per question)

# to get output not in list format, but in a plain, clean format
print("\nPrime numbers found:", " ".join(str(p) for p in primes))

print("Total primes found:", total_primes)
print("Largest prime:", largest_prime)
print("Smallest prime:", smallest_prime)
print("Sum of all primes:", sum_of_primes)



