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

sentence = input("Enter a sentence")
split_sentence = sentence.split(" ")
total_words = len(split_sentence)

temp = 0
for word in split_sentence:
    count_letter = len(word)
    if count_letter > temp:
        longest_count = count_letter
    else:
        longest_count = temp
    temp = longest_count

longest_word = [w for w in split_sentence if len(w) == longest_count][0]
longest_word = "".join(longest_word) #note: it returns first longest word, need to exclude ,.(now included)
upper_case = sentence.upper()
lower_case = sentence.lower()
title_case = sentence.title()
reversed_sentence = "".join(reversed(sentence))

print(f'Total words: {total_words}')
print(f'Longest word: {longest_word} ({longest_count}) letters')
print(f'Uppercase: {upper_case}')
print(f'Lowercase: {lower_case}')
print(f'Title case: {title_case}')
print(f'Reversed: {reversed_sentence}')
