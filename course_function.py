courses=[]
class Course:
    def __init__(self,name_course,id_course,credit_hours):
        self.name_course=name_course
        self.id_course=id_course
        self.credit_hours=int(credit_hours)
        self.students={}
    def update_course(self):
        print("1.update name")
        print("2.update credit hours")
        print("3.update both")
        choice=(input("enter choice:1/2/3:"))
        if choice=="1" or choice=="3":
            new_name_course=(input("enter new course name:"))
            self.name_course=new_name_course
        if choice=="2" or choice=="3":
            new_credit_hours=int(input("enter new credit hours:"))
            self.credit_hours=new_credit_hours
        print("course update successfully")
    def delete_course(self):
        courses.remove(self)
        print("course deleted successfully")
    def add_grade(self):
        student_name=(input("enter student name:"))
        grade=float(input(f"enter grade for {student_name} "))
        self.students[student_name]=grade
        print(f"grade add successfully for {student_name} in {self.name_course}")
    def course_report(self):
        print("=========================COURSE REPORT================================")
        print(f"course name:{self.name_course}")
        print(f"course Id:{self.id_course}")
        print(f"credit hours:{self.credit_hours}")
        print("students grades:")
        if self.students:
            for student,grade in self.students.items():
                print(f"{student}:{grade}")
        else:
            print("no grades recorded yet.")
def add_new_course():
    id_course=(input("enter id of course:"))
    for course in courses:
        if course.id_course==id_course:
            print("course is exists!")
            return
    name_course=(input("enter name of course:"))
    credit_hours=int(input("enter credit hours of course:"))
    new_course=Course(name_course,id_course,credit_hours)
    courses.append(new_course)
    print("course add successfully")
def add_grade_course():
    id_course=(input("enter the ID of the course you want to add grade to:"))
    for course in courses:
        if course.id_course==id_course:
            course.add_grade()
            return
    print("course not found")
def average_course():
    id_course = input("Enter ID of course: ")
    for course in courses:
        if course.id_course == id_course:
            if course.students:
                total = sum(course.students.values())
                avg = total / len(course.students)
                print(f"Average grade for {course.name_course} is {avg:.2f}")
            else:
                print("No grades recorded yet for this course.")
            return
    print("Course not found")
