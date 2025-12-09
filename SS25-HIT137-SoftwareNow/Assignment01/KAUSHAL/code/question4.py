# Question 4
# Create a program that asks the user to input a sentence, and display:
# • Count total words
# • Find the longest word
# • Display the sentence in:
# o All uppercase
# o All lowercase
# o Title case (first letter of each word capitalized)
# o Reversed
# Example:
# Input: "The quick brown fox"
# Output:
# Total words: 4
# Longest word: Quick (5 letters)
# Uppercase: THE QUICK BROWN FOX
# Lowercase: the quick brown fox
# Title case: The Quick Brown Fox
# Reversed: xof nworb kciuq ehT


import string # importing for punctuation
# taking user input (a sentence)
sentence = input("\nEnter a sentence:\t").strip()
# use strip to remove punctuation(like ,) and split for splitting sentence, handling multiple spaces & tabs
split_sentence = [word.strip(string.punctuation) for word in sentence.split()]
total_words = len(split_sentence)

# find longest word in the given list(split_sentence) based on length of word
# note: gives first longest word (eg: A quick brown fox -> quick and brown has 5 letters but output is 'quick')
longest_word = max(split_sentence, key=len) 
longest_count = len(longest_word)

# using functions - upper(), lower() and title()
upper_case = sentence.upper()
lower_case = sentence.lower()
title_case = sentence.title()
# slice that returns the string in reverse order
reversed_sentence = sentence[::-1]

# outputs according to question
print(f'Total words: {total_words}')
print(f'Longest word: {longest_word.title()} ({longest_count} letters)')
print(f'Uppercase: {upper_case}')
print(f'Lowercase: {lower_case}')
print(f'Title case: {title_case}')
print(f'Reversed: {reversed_sentence}')
