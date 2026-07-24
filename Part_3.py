from Part_1 import students
from part_2 import courses
def search_student_name():
    name = input("Enter Student Name: ")
    found = False
    for student in students:
        if student.name.lower() == name.lower():
            print(f"Name: {student.name} ")
            print(f"ID: {student.id}")
            print(f"Academic year: {student.year}")
            print(f"Courses: {student.courses}")
            found = True
            break
    if not found:
        print("Student Not Found")
def search_student_id():
    student_id = input("Enter Student ID: ")
    found = False
    for student in students:
        if student.id == student_id:
            print(f"Name: {student.name} ")
            print(f"ID: {student.id}")
            print(f"Academic year: {student.year}")
            print(f"Courses: {student.courses}")
            found = True
            break
    if not found:
        print("Student Not Found")
def print_courses(course):
    print(f"course name:{course.name_course}")
    print(f"course Id:{course.id_course}")
    print(f"credit hours:{course.credit_hours}")
    print("students grades:")
    if course.students:
        for student, grade in course.students.items():
            print(f"{student}:{grade}")
    else:
        print("no grades recorded yet.")
def search_course_name():
    course_name = input("Enter Course Name: ")
    found = False
    for course in courses:
        if course.name_course.lower() == course_name.lower():
            print_courses(course)
            found = true
    if not found:
        print("Course Not Found")
def search_course_id():
    course_id = input("Enter Course ID: ")
    found = False
    for course in courses:
        if course.id_course == course_id:
            print_courses(course)
            found = True
    if not found:
        print("Course Not Found")
def convert_to_gpa(grade):
    if grade >= 90:
        return 4.0
    elif grade >= 80:
        return 3.0
    elif grade >= 70:
        return 2.0
    elif grade >= 60:
        return 1.0
    else:
        return 0.0
def calculate_gpa():
    student_id = input("Enter Student ID: ")
    found_student = None
    for student in students:
        if student.id == student_id:
            found_student = student.name
            break
    if not found_student:
        print("Student Not Found")
        return
    total_points = 0
    total_hours = 0
    found_grades = False
    for course in courses:
        if student_id in course.students:
            found_grades = True
            raw_grade = course.students[student_id]
            gpa_value = convert_to_gpa(raw_grade)
            hours = course.credit_hours
            total_points += gpa_value * hours
            total_hours += hours
    if not found_grades:
        print(f"No grades recorded yet for student {found_student} (ID: {student_id})")
    elif total_hours == 0:
        print("GPA = 0")
    else:
        gpa = total_points / total_hours
        print(f"Student: {found_student} (ID: {student_id})")
        print(f"Weighted GPA = {round(gpa,2)}")

