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

given_limit = int(input('Enter the given limit for the prime number (max 100)'))

list_prime = []
sum_prime = 0
for i in range(2, given_limit + 1):
    count = 0
    for j in range(1,i+1):
        if i % j == 0:
            count = count + 1
    if count == 2:      
        list_prime.append(i)
        sum_prime = sum_prime + i
print(list_prime)
print(len(list_prime))
print(max(list_prime))
print(min(list_prime))
print(sum_prime)