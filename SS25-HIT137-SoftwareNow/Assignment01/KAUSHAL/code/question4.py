'''
Question 4 Create a program that asks the user to input a sentence, and display:
• Count total words
• Find the longest word
• Display the sentence in:
o All uppercase
o All lowercase
o Title case (first letter of each word capitalized)
o Reversed
Example:
Input: "The quick brown fox"
Output:
Total words: 4
Longest word: Quick (5 letters)
Uppercase: THE QUICK BROWN FOX
Lowercase: the quick brown fox
Title case: The Quick Brown Fox
Reversed: xof nworb kciuq ehT
'''

# importing for punctuation
import string  

# taking user input (a sentence)
sentence = input("\nEnter a sentence: ").strip()

# strip punctuation around word and split the sentence
split_sentence = [word.strip(string.punctuation) for word in sentence.split()]
total_words = len(split_sentence) # length of split_sentence


# Count only alphabetic letters(not ' or -)
def letter_count(word):
    return sum(1 for ch in word if ch.isalpha())

# Get the word with the most alphabet letters
longest_word = max(split_sentence, key=letter_count) # max calls letter_count on each word
longest_count = letter_count(longest_word) # function call

# uppercase, lowercase, title case
upper_case = sentence.upper()
lower_case = sentence.lower()
title_case = sentence.title()

# reversed
reversed_sentence = sentence[::-1]

"""
desired outputs:
note: gives the first longest word as in the example of the question(instructed)
        - example: A quick brown fox. (both quick and brown has 5 letters, but output is quick)
"""
print(f'Total words: {total_words}')
print(f'Longest word: {longest_word} ({longest_count} letters)')
print(f'Uppercase: {upper_case}')
print(f'Lowercase: {lower_case}')
print(f'Title case: {title_case}')
print(f'Reversed: {reversed_sentence}')
