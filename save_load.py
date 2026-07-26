from student_function import students, Student
from course_function import Course, courses
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_JSON = os.path.join(BASE_DIR, "student.json")
COURSE_JSON = os.path.join(BASE_DIR, "course.json")
REPORT_CSV = os.path.join(BASE_DIR, "report.csv")

def serialize_student_ref(s):
    if hasattr(s, 'id'):
        return str(s.id)
    elif hasattr(s, 'id_course'):
        return str(s.id_course)
    elif isinstance(s, dict):
        return str(s.get('id') or s.get('ID') or s.get('name') or s)
    return str(s)

def serialize_value(v):
    if hasattr(v, 'id'):
        return str(v.id)
    elif hasattr(v, 'id_course'):
        return str(v.id_course)
    elif isinstance(v, dict):
        return {str(k): serialize_value(val) for k, val in v.items()}
    elif isinstance(v, (int, float, str, bool, type(None))):
        return v
    try:
        return float(v)
    except (ValueError, TypeError):
        return str(v)

def save_students():
    students_json = []
    for student in students:
        courses_list = []
        for c in student.courses:
            if hasattr(c, 'id_course'):
                courses_list.append({
                    "id": str(c.id_course),
                    "name": str(c.name_course),
                    "credit_hours": c.credit_hours
                })
            elif isinstance(c, dict):
                courses_list.append(c)
            else:
                courses_list.append({"id": str(c), "name": str(c)})
        st_dict = {
            "Name": student.name,
            "ID": student.id,
            "Academic Year": student.year,
            "Courses": courses_list
        }
        students_json.append(st_dict)
    with open(STUDENT_JSON, "w", encoding="utf-8") as file:
        json.dump(students_json, file, indent=4)

def save_courses():
    courses_json = []
    for course in courses:
        safe_students = {}
        if isinstance(course.students, dict):
            for k, v in course.students.items():
                safe_key = serialize_student_ref(k)
                safe_val = serialize_value(v)
                safe_students[safe_key] = safe_val
        elif isinstance(course.students, (list, tuple, set)):
            safe_students = [serialize_student_ref(s) for s in course.students]
        else:
            safe_students = str(course.students)

        courses_json.append({
            "course name": course.name_course,
            "course id": course.id_course,
            "credit hours": course.credit_hours,
            "students": safe_students
        })
    with open(COURSE_JSON, "w", encoding="utf-8") as file:
        json.dump(courses_json, file, indent=4)

def load_courses():
    if not os.path.exists(COURSE_JSON):
        return
    try:
        with open(COURSE_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
        courses.clear()
        for course_data in data:
            c = Course(
                course_data["course name"],
                course_data["course id"],
                course_data["credit hours"]
            )
            loaded_students = course_data.get("students", {})
            if isinstance(loaded_students, dict):
                c.students = loaded_students
            else:
                c.students = {}
            courses.append(c)
    except Exception as e:
        print(f"[save_load] Error loading course.json: {e}")

def load_students():
    if not os.path.exists(STUDENT_JSON):
        return
    try:
        with open(STUDENT_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
        students.clear()
        for student_data in data:
            s = Student(
                student_data["Name"],
                student_data["ID"],
                student_data["Academic Year"]
            )
            raw_courses = student_data.get("Courses", [])
            resolved_courses = []
            for rc in raw_courses:
                if isinstance(rc, dict):
                    cid = rc.get("id") or rc.get("id_course") or rc.get("name")
                else:
                    cid = str(rc)

                found_course = None
                for c in courses:
                    if str(c.id_course).lower() == str(cid).lower() or c.name_course.lower() == str(cid).lower():
                        found_course = c
                        break
                if found_course:
                    resolved_courses.append(found_course)
                else:
                    resolved_courses.append(rc)
            s.courses = resolved_courses
    except Exception as e:
        print(f"[save_load] Error loading student.json: {e}")

def load_students_to_csv():
    if not os.path.exists(STUDENT_JSON):
        return []
    try:
        with open(STUDENT_JSON, "r", encoding="utf-8") as file:
            students_to_upload = json.load(file)
            return students_to_upload
    except Exception:
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

