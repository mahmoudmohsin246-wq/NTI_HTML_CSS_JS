from Part_1 import students,Student
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_JSON = os.path.join(BASE_DIR, "student.json")
REPORT_CSV = os.path.join(BASE_DIR, "report.csv")

def save_students():
    students_json = []
    for student in students:
        c_list = []
        for c in student.courses:
            if hasattr(c, 'name_course'):
                c_list.append({"id": c.id_course, "name": c.name_course, "credit_hours": c.credit_hours})
            elif isinstance(c, dict):
                c_list.append(c)
            else:
                c_list.append({"name": str(c)})
        st_dict = {
            "Name": student.name,
            "ID": student.id,
            "Academic Year": student.year,
            "Courses": c_list
        }
        students_json.append(st_dict)
    with open(STUDENT_JSON, "w", encoding="utf-8") as file:
        json.dump(students_json, file, indent=4)

        
def load_students():
    if not os.path.exists(STUDENT_JSON):
        return
    try:
        with open(STUDENT_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, dict):
            data = data.get("Student", [])
        if not isinstance(data, list):
            data = []

        students.clear()
        for student in data:
            if not isinstance(student, dict):
                continue
            s = Student(
                student.get("Name", "Unknown"),
                student.get("ID", "0"),
                student.get("Academic Year", "1")
            )
            s.courses = student.get("Courses", [])
    except Exception as e:
        print(f"[part_4] Error loading student.json: {e}")

def load_students_to_csv():
    if not os.path.exists(STUDENT_JSON):
        return []
    try:
        with open(STUDENT_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, dict):
            data = data.get("Student", [])
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def export_to_csv():
    students_to_csv = load_students_to_csv()
    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as file:
        data = csv.writer(file)
        data.writerow(["Name", "ID", "Academic Year", "Courses"])
        for student in students_to_csv:
            data.writerow([
                student.get("Name", ""),
                student.get("ID", ""),
                student.get("Academic Year", ""),
                student.get("Courses", [])
            ])

