import os
import json
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS

from student_function import students, Student
from course_function import courses, Course
from search_GPA import convert_to_gpa
import save_load

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# Helper serialization functions
def student_to_dict(s):
    courses_list = []
    for c in s.courses:
        if isinstance(c, Course):
            courses_list.append({"id": c.id_course, "name": c.name_course, "credit_hours": c.credit_hours})
        elif isinstance(c, dict):
            courses_list.append(c)
        else:
            courses_list.append({"id": str(c), "name": str(c)})
    return {
        "id": str(s.id),
        "name": s.name,
        "year": str(s.year),
        "courses": courses_list
    }

def course_to_dict(c):
    return {
        "id": str(c.id_course),
        "name": c.name_course,
        "credit_hours": c.credit_hours,
        "students": c.students  # dict of student_id/name -> grade
    }

def find_student_by_id(student_id):
    for s in students:
        if str(s.id).lower() == str(student_id).lower():
            return s
    return None

def find_course_by_id(course_id):
    for c in courses:
        if str(c.id_course).lower() == str(course_id).lower():
            return c
    return None

# Serve Frontend SPA
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# System Stats Endpoint
@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_enrollments = sum(len(s.courses) for s in students)
    total_grades = sum(len(c.students) for c in courses)
    return jsonify({
        "status": "success",
        "total_students": len(students),
        "total_courses": len(courses),
        "total_enrollments": total_enrollments,
        "total_grades_recorded": total_grades
    })

# Students API
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify({
        "status": "success",
        "data": [student_to_dict(s) for s in students]
    })

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    student_id = str(data.get("id", "")).strip()
    year = str(data.get("year", "")).strip()

    if not name or not student_id or not year:
        return jsonify({"status": "error", "message": "Name, ID, and Academic Year are required."}), 400

    if find_student_by_id(student_id):
        return jsonify({"status": "error", "message": f"Student with ID '{student_id}' already exists."}), 400

    new_student = Student(name, student_id, year)
    return jsonify({
        "status": "success",
        "message": f"Student '{name}' added successfully.",
        "data": student_to_dict(new_student)
    }), 201

@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404
    return jsonify({"status": "success", "data": student_to_dict(student)})

@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    data = request.get_json() or {}
    new_name = data.get("name")
    new_year = data.get("year")

    if new_name is not None and str(new_name).strip():
        student.name = str(new_name).strip()
    if new_year is not None and str(new_year).strip():
        student.year = str(new_year).strip()

    student.student["Name"] = student.name
    student.student["Academic Year"] = student.year

    return jsonify({
        "status": "success",
        "message": "Student updated successfully.",
        "data": student_to_dict(student)
    })

@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    for course in courses:
        if student_id in course.students:
            del course.students[student_id]
        if student.name in course.students:
            del course.students[student.name]

    student.del_update()
    return jsonify({"status": "success", "message": f"Student ID '{student_id}' deleted successfully."})

@app.route("/api/students/<student_id>/enroll", methods=["POST"])
def enroll_student_course(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    data = request.get_json() or {}
    course_ids = data.get("course_ids", [])
    if isinstance(course_ids, str):
        course_ids = [course_ids]

    if not course_ids:
        return jsonify({"status": "error", "message": "No courses selected."}), 400

    added = []
    already = []
    not_found = []

    for cid in course_ids:
        course = find_course_by_id(cid)
        if not course:
            for c in courses:
                if c.name_course.lower() == str(cid).lower():
                    course = c
                    break

        if not course:
            not_found.append(str(cid))
            continue

        if course in student.courses:
            already.append(course.name_course)
        else:
            student.courses.append(course)
            added.append(course.name_course)

    msg_parts = []
    if added:
        msg_parts.append(f"Enrolled in: {', '.join(added)}.")
    if already:
        msg_parts.append(f"Already enrolled in: {', '.join(already)}.")
    if not_found:
        msg_parts.append(f"Courses not found: {', '.join(not_found)}.")

    return jsonify({
        "status": "success",
        "message": " ".join(msg_parts),
        "data": student_to_dict(student)
    })

@app.route("/api/students/<student_id>/gpa", methods=["GET"])
def get_student_gpa(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    total_points = 0.0
    total_hours = 0
    evaluated_courses = []

    for course in courses:
        raw_grade = None
        if student_id in course.students:
            raw_grade = course.students[student_id]
        elif student.name in course.students:
            raw_grade = course.students[student.name]

        if raw_grade is not None:
            try:
                numeric_grade = float(raw_grade)
                gpa_val = convert_to_gpa(numeric_grade)
                hours = int(course.credit_hours)
                total_points += gpa_val * hours
                total_hours += hours
                evaluated_courses.append({
                    "course_id": course.id_course,
                    "course_name": course.name_course,
                    "credit_hours": hours,
                    "numeric_grade": numeric_grade,
                    "gpa_point": gpa_val
                })
            except ValueError:
                pass

    if total_hours == 0:
        calculated_gpa = 0.0
    else:
        calculated_gpa = round(total_points / total_hours, 2)

    return jsonify({
        "status": "success",
        "data": {
            "student_id": student.id,
            "student_name": student.name,
            "gpa": calculated_gpa,
            "total_credit_hours": total_hours,
            "evaluated_courses": evaluated_courses
        }
    })

@app.route("/api/students/<student_id>/report", methods=["GET"])
def get_student_report(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    gpa_res = get_student_gpa(student_id).json.get("data", {})
    return jsonify({
        "status": "success",
        "data": {
            "student": student_to_dict(student),
            "gpa_summary": gpa_res
        }
    })

# Courses API
@app.route("/api/courses", methods=["GET"])
def get_courses():
    return jsonify({
        "status": "success",
        "data": [course_to_dict(c) for c in courses]
    })

@app.route("/api/courses", methods=["POST"])
def add_course():
    data = request.get_json() or {}
    id_course = str(data.get("id_course", "")).strip()
    name_course = data.get("name_course", "").strip()
    credit_hours = data.get("credit_hours")

    if not id_course or not name_course or credit_hours is None:
        return jsonify({"status": "error", "message": "Course ID, Course Name, and Credit Hours are required."}), 400

    try:
        credit_hours = int(credit_hours)
    except ValueError:
        return jsonify({"status": "error", "message": "Credit Hours must be a valid integer."}), 400

    if find_course_by_id(id_course):
        return jsonify({"status": "error", "message": f"Course with ID '{id_course}' already exists."}), 400

    new_course = Course(name_course, id_course, credit_hours)
    courses.append(new_course)

    return jsonify({
        "status": "success",
        "message": f"Course '{name_course}' added successfully.",
        "data": course_to_dict(new_course)
    }), 201

@app.route("/api/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404
    return jsonify({"status": "success", "data": course_to_dict(course)})

@app.route("/api/courses/<course_id>", methods=["PUT"])
def update_course(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404

    data = request.get_json() or {}
    new_name = data.get("name_course")
    new_hours = data.get("credit_hours")

    if new_name is not None and str(new_name).strip():
        course.name_course = str(new_name).strip()
    if new_hours is not None:
        try:
            course.credit_hours = int(new_hours)
        except ValueError:
            return jsonify({"status": "error", "message": "Credit Hours must be an integer."}), 400

    return jsonify({
        "status": "success",
        "message": "Course updated successfully.",
        "data": course_to_dict(course)
    })

@app.route("/api/courses/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404

    for s in students:
        if course in s.courses:
            s.courses.remove(course)

    course.delete_course()
    return jsonify({"status": "success", "message": f"Course ID '{course_id}' deleted successfully."})

@app.route("/api/courses/<course_id>/grade", methods=["POST"])
def register_grade(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404

    data = request.get_json() or {}
    student_identifier = str(data.get("student_id", "")).strip()
    grade = data.get("grade")

    if not student_identifier or grade is None:
        return jsonify({"status": "error", "message": "Student ID/Name and Grade are required."}), 400

    try:
        grade = float(grade)
    except ValueError:
        return jsonify({"status": "error", "message": "Grade must be a valid number."}), 400

    if grade < 0 or grade > 100:
        return jsonify({"status": "error", "message": "Grade must be between 0 and 100."}), 400

    course.students[student_identifier] = grade

    return jsonify({
        "status": "success",
        "message": f"Grade {grade} registered for '{student_identifier}' in course '{course.name_course}'.",
        "data": course_to_dict(course)
    })

@app.route("/api/courses/<course_id>/average", methods=["GET"])
def get_course_average(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404

    if not course.students:
        return jsonify({
            "status": "success",
            "data": {
                "course_id": course.id_course,
                "course_name": course.name_course,
                "average": None,
                "total_students": 0,
                "message": "No grades recorded yet for this course."
            }
        })

    numeric_grades = []
    for g in course.students.values():
        try:
            numeric_grades.append(float(g))
        except (ValueError, TypeError):
            pass

    if not numeric_grades:
        avg = None
    else:
        avg = round(sum(numeric_grades) / len(numeric_grades), 2)

    return jsonify({
        "status": "success",
        "data": {
            "course_id": course.id_course,
            "course_name": course.name_course,
            "average": avg,
            "total_students": len(numeric_grades),
            "highest_grade": max(numeric_grades) if numeric_grades else None,
            "lowest_grade": min(numeric_grades) if numeric_grades else None
        }
    })

@app.route("/api/courses/<course_id>/report", methods=["GET"])
def get_course_report(course_id):
    course = find_course_by_id(course_id)
    if not course:
        return jsonify({"status": "error", "message": "Course not found."}), 404

    avg_res = get_course_average(course_id).json.get("data", {})
    return jsonify({
        "status": "success",
        "data": {
            "course": course_to_dict(course),
            "stats": avg_res
        }
    })

# Unified Search API
@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip().lower()
    search_type = request.args.get("type", "all").strip().lower()

    matched_students = []
    matched_courses = []

    if not query:
        return jsonify({
            "status": "success",
            "students": [student_to_dict(s) for s in students],
            "courses": [course_to_dict(c) for c in courses]
        })

    if search_type in ["all", "student", "student_id", "student_name"]:
        for s in students:
            if query in s.id.lower() or query in s.name.lower():
                matched_students.append(student_to_dict(s))

    if search_type in ["all", "course", "course_id", "course_name"]:
        for c in courses:
            if query in c.id_course.lower() or query in c.name_course.lower():
                matched_courses.append(course_to_dict(c))

    return jsonify({
        "status": "success",
        "query": query,
        "students": matched_students,
        "courses": matched_courses
    })

# Database Persistence API
@app.route("/api/database/save", methods=["POST"])
def save_database():
    try:
        save_load.save_students()
        save_load.save_courses()
        return jsonify({"status": "success", "message": "Database saved successfully to student.json and course.json."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to save database: {str(e)}"}), 500

@app.route("/api/database/load", methods=["POST"])
def load_database():
    try:
        save_load.load_students()
        save_load.load_courses()
        return jsonify({
            "status": "success",
            "message": f"Database loaded successfully! Total loaded students: {len(students)}, courses: {len(courses)}.",
            "total_students": len(students)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to load database: {str(e)}"}), 500

@app.route("/api/database/export-csv", methods=["POST"])
def export_csv():
    try:
        save_load.save_students()
        save_load.export_to_csv()
        return jsonify({"status": "success", "message": "Course report exported successfully to report.csv."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to export CSV: {str(e)}"}), 500

@app.route("/api/database/download-csv", methods=["GET"])
def download_csv():
    try:
        save_load.save_students()
        save_load.export_to_csv()
        report_file = save_load.REPORT_CSV
        if os.path.exists(report_file):
            return send_file(report_file, as_attachment=True, download_name="report.csv", mimetype="text/csv")
        else:
            return jsonify({"status": "error", "message": "report.csv file not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"Download failed: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        save_load.load_students()
        save_load.load_courses()
        print(f"[Init] Pre-loaded {len(students)} students and {len(courses)} courses.")
    except Exception as e:
        print(f"[Init] Could not pre-load database: {e}")

    print("[Backend] Starting Flask REST API server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
