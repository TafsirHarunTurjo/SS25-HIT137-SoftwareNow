# Question 3
# Write a program that asks the user how many students are in the class (minimum 3,
# maximum 10). For each student, input their name and score (0-100). Calculate and
# display:
# • Each student's grade (HD: 85-100, D: 75-84, C: 65-74, P: 50-64, F: 0-49).
# • Class average
# • Highest and lowest score and student name
# • Lowest score and student name
# Example:
# How many students? 3
# Student 1 name: Alice
# Alice's score: 78
# Student 2 name: Bob
# Bob's score: 92
# Student 3 name: Carol
# Carol's score: 45
# Results:
# Alice: 78 (D)
# Bob: 92 (HD)
# Carol: 45 (F)
# Average score: 71.677
# Highest: Bob (92)
# Lowest: Carol (45)

# taking input(number of students) from user
number_of_student = int(input('\tHow many students?(3-10)'))

# retake input if number of students is greater than 10 or less than 3
while number_of_student < 3 or number_of_student > 10:
    number_of_student = int(input('Enter value within the range 3 to 10(included) '))

# initiate list for name of students and their corrosponding scores
name_of_students = [] 
score_of_students = []

sum = 0 
for s in range(1,number_of_student+1):
    # Loop to take only valid names (letters only)
    while True:
        name = input(f'Enter the name of student-{s}\t')
        # strip() removes all leading and trailing spaces. 
        # It takes valid name(eg. Hari or Hari Thapa, but not Hari123 or " ")
        if all(char.isalpha() or char.isspace() for char in name) and name.strip():  # all() checks for every char
            break
        else:
            print("Invalid input! Please enter letters only (no numbers or symbols).")

    name_of_students.append(name) # put each name in the list
    score = int(input(f'Enter the score(0-100) of student-{s}\t'))

    # retake score if the value is negative or greater than 100
    while score < 0 or score > 100:
        score = int(input("Enter again.Score must be between 0 and 100(included)\t"))
    score_of_students.append(score) # put each score in the list

    # used to calculate the sum of score of all student to get average value
    sum = sum + score 

average_score = sum / number_of_student
highest_score = max(score_of_students)
lowest_score = min(score_of_students)

# get indices of all students with highest and lowest scores
# list comprehension using enumerate function(to get both value and index)
idx_highest_scores = [i for i, score in enumerate(score_of_students) if score == highest_score]
idx_lowest_scores = [i for i, score in enumerate(score_of_students) if score == lowest_score]


# name and score of each student
print("\n")
for i in range(number_of_student):
    print(f'Student {i+1} name: {name_of_students[i]}')
    print(f"{name_of_students[i]}'s score: {score_of_students[i]}")

print('Results:')

# Results of student as per grade criteria
for i in range(number_of_student):
    if 100 >= score_of_students[i] >= 85:
        print(f'{name_of_students[i]}: {score_of_students[i]} (HD)')

    elif 84 >= score_of_students[i] >= 75:
        print(f'{name_of_students[i]}: {score_of_students[i]} (D)')

    elif 74 >= score_of_students[i] >= 65:
        print(f'{name_of_students[i]}: {score_of_students[i]} (C)')

    elif 64 >= score_of_students[i] >= 50:
        print(f'{name_of_students[i]}: {score_of_students[i]} (P)')

    elif 49 >= score_of_students[i] >= 0:
        print(f'{name_of_students[i]}: {score_of_students[i]} (F)')

print(f'Average score: {average_score:.3f}') # average score (upto 3 decimal place)

# get the name(s) and corresponding highest & lowest scores using indices found earlier
highest_names = [name_of_students[i] for i in idx_highest_scores]
lowest_names = [name_of_students[i] for i in idx_lowest_scores]

print(f'Highest: {",".join(highest_names)} ({highest_score})')
print(f'Lowest: {",".join(lowest_names)} ({lowest_score})')




    
    





