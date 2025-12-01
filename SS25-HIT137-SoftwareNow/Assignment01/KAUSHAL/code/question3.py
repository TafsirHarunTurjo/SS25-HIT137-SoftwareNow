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

#Do using dict

number_of_student = int(input('How many students?'))
name_of_students = []
score_of_students = []
sum = 0
for s in range(1,number_of_student+1):
    name = input(f'Enter the name of student-{s}')
    name_of_students.append(name)
    score = int(input(f'Enter the score(0-100) of student-{s}'))
    score_of_students.append(score)
    sum = sum + score

average_score = sum / number_of_student
highest_score = max(score_of_students)
idx_highest_score = score_of_students.index(highest_score)
lowest_score = min(score_of_students)
idx_lowest_score = score_of_students.index(lowest_score)

for i in range(number_of_student):
    print(f'Student {i+1} name: {name_of_students[i]}')
    print(f"{name_of_students[i]}'s score: {score_of_students[i]}")

print('Results:')

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

print(f'Average score: {average_score:.3f}')
print(f'Highest: {name_of_students[idx_highest_score]} ({highest_score})')
print(f'Lowest: {name_of_students[idx_lowest_score]} ({lowest_score})')



    
    





