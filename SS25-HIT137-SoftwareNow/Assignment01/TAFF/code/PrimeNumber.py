#Taking user input
lowerRange = int(input('Enter lower range: '))
upperRange = int(input('Enter upper range: '))

primes = []  # List to store found prime numbers


for num in range(lowerRange, upperRange + 1):
    if num > 1:
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            print(num)
            primes.append(num)  # store prime number

# Display results
print("Prime numbers found:", primes)
# print("Prime numbers found:", *primes)
print("Total primes found:", len(primes))
print('Smallest prime number:', min(primes))
print('Largest prime number:', max(primes))
