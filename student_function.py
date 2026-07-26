from course_function import courses
students=[]
class Student:
    def __init__(self,name,id,year):
        self.courses = []
        self.name= name
        self.id = id
        self.year = year
        self.student = {"Name": self.name, "ID": self.id, "Academic Year": self.year,"Courses": self.courses}
        found = False
        for student in students:
            if student.id == self.id:
                found = True
                break
        if found :
            print("The ID is used before.")
        else:
            students.append(self)
    def del_update(self):
        students.remove(self)
        print("The student has been deleted!")

    def student_course(self):
        print(f"The number of courses is {len(courses)} ")
        num = int(input("Enter the number of courses you want: "))
        if num + len(self.courses) > len(courses):
            print("The Number of courses you entered is greater than the available")
        else:
            while num > 0:
                course_name = input("Enter the name of the course: ")
                found = False
                for course in courses:
                    if course.name_course.lower() == course_name.lower():
                        found = True
                        if course in self.courses:
                            print("You have already registered for this course")
                        else:
                            self.courses.append(course)
                            print("The Course has been added successfully!")
                        num -= 1
                        break
                if not found:
                    print("This course isn't available")
    def display(self):
        print("Here is your Report")
        print(f"Name: {self.name} " )
        print(f"ID: {self.id}")
        print(f"Academic year: {self.year}")
        print(f"Courses: {self.courses}")
    def update_student(self):
        update = input("What do you want to update (Name/ID/Year): ").lower()
        if update == "name":
            id1=input("Enter the id: ")
            for student in students:
                if student.id == id1:
                    student.name = input("Enter the new name: ")
                    self.name = student.name
                    break
        elif update == "id":
            name1 = input("Enter the name: ")
            for student in students:
                if student.name == name1:
                    self.id = input("Enter the new ID: ")
                    student.id=self.id
                    break
        elif update == "year":
            id1 = input("Enter the id: ")
            for student in students:
                if student.id == id1:
                    self.year=input("Enter the new Academic Year: ")
                    student.year=self.year
                    break
def Input():
    Name = input("Enter the Name:")
    ID = input("Enter the ID: ")
    year = input("Enter the Academic Year: ")
    info=[Name,ID,year]
    return info