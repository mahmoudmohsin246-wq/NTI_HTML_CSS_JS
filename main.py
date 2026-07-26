import os
import msvcrt
blue   = "\033[94m"
yellow = "\033[93m"
cyan   = "\033[96m"
red    = "\033[91m"
green  = "\033[92m"
c_reset = "\033[0m"
from student_function import Student, Input, students
from course_function import courses,Course,add_new_course,add_grade_course,average_course
from search_GPA import search_student_name,search_student_id,search_course_name,search_course_id,calculate_gpa
from save_load import save_students,export_to_csv,load_students,save_courses,load_courses
options = [
    "Add Course",
    "Add Student",
    "Sign up for a course",
    "Register Grade",
    "Print Student GPA",
    "Print Course Report",
    "Print Student Report",
    "Edit in the student",
    "Edit Course",
    "display all courses",
    "Search Student",
    "search course",
    "Course Average",
    "Delete Student",
    "Delete Course",
    "Save Database",
    "Export Course CSV",
    "Exit",
]
def showMenu(selected):
    os.system("cls")
    print(blue+"\n--- Student & Course Management System ---"+c_reset)
    for i, opt in enumerate(options):
        optionId = 0 if i == len(options) else i + 1
        if optionId == selected:
            print(yellow+" -> " + opt+c_reset)
        else:
            print("    " + opt)
    print(blue + "------------------------------------------" + c_reset)
    print(yellow + "Use numbers and press Enter" + c_reset)
def main():
    currentSelection = 1
    choice = None
    try:
        load_students()
        load_courses()
    except Exception as e:
        print(red + "System Error:", e, c_reset)
    while True:
        showMenu(currentSelection)
        try:
            key = msvcrt.getch()
            if key == b'H':
                if currentSelection == 1:
                    currentSelection = len(options)
                else:
                    currentSelection -=1
            elif key == b'P':
                if currentSelection == len(options):
                    currentSelection = 1
                else:
                    currentSelection += 1
            elif key == b'\r':
                choice = currentSelection
        except ValueError:
            continue
        try:
            if choice is None:
                continue
            if choice == 1:
                os.system("cls")
                print(blue + "Add Course" + c_reset)
                add_new_course()
            elif choice == 2:
                os.system("cls")
                print(blue + "Add Student" + c_reset)
                info = Input()
                Student(*info)
            elif choice == 3:
                os.system("cls")
                print(blue + "Sign up for a course" + c_reset)
                id_input = input("Enter the ID of student: ")
                found = False
                for student in students:
                    if student.id == id_input:
                        found = True
                        student.student_course()
                        break
                if not found:
                    print(red + "Student not found!" + c_reset)
            elif choice == 4:
                os.system("cls")
                print(blue + "Register Grade" + c_reset)
                add_grade_course()
            elif choice == 5:
                os.system("cls")
                print(blue + "Print Student GPA" + c_reset)
                calculate_gpa()
            elif choice == 6:
                os.system("cls")
                print(blue + "Print Course Report" + c_reset)
                found=False
                id_course = (input("enter id of course:"))
                for course in courses:
                    if course.id_course == id_course:
                        found = True
                        Course.course_report(course)
                        break
                if not found:
                    print(red + "Course not found!" + c_reset)
            elif choice == 7:
                os.system("cls")
                print(blue + "Print Student Report" + c_reset)
                id =input("Enter the id of student you want to print:")
                found=False
                for student in students:
                    if student.id==id:
                        found=True
                        Student.display(student)
                        break
                if not found:
                    print(red + "No students available!" + c_reset)
            elif choice == 8:
                os.system("cls")
                print(blue + "Edit in student" + c_reset)
                id = input("Enter the id of student you want to print:")
                found = False
                for student in students:
                    if student.id == id:
                        found = True
                        Student.update_student(student)
                        break
                if not found:
                    print(red + "No students available!" + c_reset)
            elif choice == 9:
                os.system("cls")
                print(blue + "Edit Course" + c_reset)
                if not courses:
                    print("not found courses")
                    continue
                id = input("enter the id of course you edit:")
                found = False
                for course in courses:
                    if course.id_course == id:
                        found = True
                        course.update_course()
                        break
                if not found:
                    print("course id not found")
                print(blue + "Edit Course" + c_reset)

            elif choice == 10:
                os.system("cls")
                print(blue + "Print all Courses" + c_reset)
                if not courses:
                    print("no courses found")
                else:
                    for course in courses:
                        print("==================Course=======================")
                        print(f"course_ID:{course.id_course}")
                        print(f"course_name:{course.name_course}")
                        print(f"credit_hours:{course.credit_hours}")
                        print("====================================================")
            elif choice == 11:
                os.system("cls")
                print(blue + "Search Student" + c_reset)
                print("1 search by id")
                print("2 search by name")
                print("3 exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    search_student_id()
                elif choice == "2":
                    search_student_name()
                elif choice == "3":
                    break
                else:
                    print(red + "Invalid choice!" + c_reset)
            elif choice == 12:
                os.system("cls")
                print(blue + "Search Course" + c_reset)
                print("1 search by id")
                print("2 search by name")
                print("3 exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    search_course_id()
                elif choice == "2":
                    search_course_name()
                elif choice == "3":
                    print("Exit")
                else:
                    print(red + "Invalid choice!" + c_reset)
            elif choice == 13:
                os.system("cls")
                print(blue + "Course Average" + c_reset)
                average_course()
            elif choice == 14:
                os.system("cls")
                print(blue + "Delete Student" + c_reset)
                id =input("enter the id of student you want to delete:")
                found=False
                for student in students:
                    if student.id==id:
                        found=True
                        Student.del_update(student)
                        break
                if not found:
                    print("No student found")
            elif choice == 15:
                os.system("cls")
                print(blue + "Delete Course" + c_reset)
                id = input("enter id of course: ")
                found = False
                for course in courses:
                    if course.id_course == id:
                        found=True
                        Course.delete_course(course)
                if not found:
                    print(red + "Course not found!" + c_reset)
            elif choice == 16:
                os.system("cls")
                print(blue + "Save Database" + c_reset)
                save_students()
                save_courses()
                print(green + "Data saved successfully!" + c_reset)
            elif choice == 17:
                os.system("cls")
                print(blue + "Export Course CSV" + c_reset)
                export_to_csv()
                print(green + "Course exported successfully!" + c_reset)
            elif choice == 18:
                os.system("cls")
                print(blue + "Saving before exit..." + c_reset)
                save_students()
                export_to_csv()
                print(yellow + "Data saved. Exiting program..." + c_reset)
                break
            else:
                print(red + "Invalid selection!" + c_reset)
        except Exception as e:
            print(red + "System Error:", e, c_reset)
        input(cyan + "\nPress Enter to return to menu..." + c_reset)
        choice = None
main()