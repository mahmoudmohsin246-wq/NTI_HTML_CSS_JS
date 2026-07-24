import os
import json
import msvcrt
blue   = "\033[94m"
yellow = "\033[93m"
cyan   = "\033[96m"
red    = "\033[91m"
green  = "\033[92m"
c_reset = "\033[0m"
from Part_1 import Student, Input, students
from part_2 import courses,Course,add_new_course,add_grade_course,average_course
from Part_3 import search_student_name,search_student_id,search_course_name,search_course_id,calculate_gpa
from part_4 import save_students,export_to_csv,load_students
options = [
    "Add Course",#الفانكشان بضيف و شغاله
    "Add Student",#بيضيف الطالب و شغاله
    "Sign up for a course",#شغال
    "Register Grade",#شغال
    "Print Student GPA",#شغال
    "Print Course Report",#شغال
    "Save Database",#شغاله
    "Load Database",#لا====================
    "Export Course CSV",#شغاله
    "Edit in the student",#شغاله
    "Print Student Report",#شغاله
    "Delete Student",#شغاله
    "Delete Course",#شغاله
    "Edit Course",#شغاله
    "display all courses",#شغاله
    "Search Student",#شغاله
    "search course",#شغاله
    "Course Average",#شغاله
    "Exit"
]
def showMenu(selected):
    os.system("cls")
    print("\n--- Student & Course Management System ---")
    for i, opt in enumerate(options):
        optionId = 0 if i == 19 else i + 1
        if optionId == selected:
            print(" -> " + opt)
        else:
            print("    " + opt)
    print(blue + "------------------------------------------" + c_reset)
    print(yellow + "Use numbers and press Enter" + c_reset)
def main():
    currentSelection = 1
    choice = None
    while True:
        showMenu(currentSelection)
        try:
            key = msvcrt.getch()
            if key == b'H':  # سهم لفوق
                currentSelection = max(1, currentSelection - 1)
            elif key == b'P':  # سهم لتحت
                currentSelection = min(len(options), currentSelection + 1)
            elif key == b'\r':  # Enter
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
                print(blue + "Save Database" + c_reset)
                save_students()
                print(green + "Data saved successfully!" + c_reset)
            elif choice == 8:
                os.system("cls")
                print(blue + "Load Database" + c_reset)
                load_students()
                print(green + "Data loaded successfully!" + c_reset)
            elif choice == 9:
                os.system("cls")
                os.system("cls")
                print(blue + "Export Course CSV" + c_reset)
                export_to_csv()
                print(green + "Course exported successfully!" + c_reset)
            elif choice == 10:
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
            elif choice == 11:
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
            elif choice == 12:
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
            elif choice == 13:
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
            elif choice == 14:
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
            elif choice == 15:
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
            elif choice == 16:
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
            elif choice == 17:
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
            elif choice == 18:
                os.system("cls")
                print(blue + "Course Average" + c_reset)
                average_course()
            elif choice == 0:
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
if __name__ == "__main__":
    main()