# Student & Course Management System (EduPortal) - Front-End & REST API

A modern, responsive Single Page Application (SPA) built for the **Anti-Graffiti / Student & Course Management System**. The application features a glassmorphism dark theme UI connected to an unchanged Python backend via a lightweight Flask REST API bridge.

---

## 📁 Project Architecture & Folder Structure

```
nti project/
│
├── app.py                      # Flask REST API Server & SPA host
├── Part_1.py                   # Backend: Student class & student registry logic
├── part_2.py                   # Backend: Course class & grading logic
├── Part_3.py                   # Backend: Search algorithms & 4.0 GPA converter
├── part_4.py                   # Backend: JSON file persistence & CSV export logic
├── main.py                     # Legacy CLI interface
├── student.json                # JSON Database persistence store
├── report.csv                  # Generated CSV report output
│
└── frontend/                   # Complete Front-End Web Application
    ├── index.html              # Main Single Page Application HTML shell
    ├── css/
    │   └── styles.css          # Glassmorphism dark mode CSS design system
    └── js/
        ├── api.js              # Fetch API client module
        ├── ui.js               # Toast alerts, loading states & modal utilities
        ├── students.js         # Student registry controller & GPA/Report modals
        ├── courses.js          # Course catalog controller & average calculator
        ├── enrollment.js       # Course registration & grade entry controller
        ├── reports.js          # Database save/load & CSV download manager
        └── app.js              # Application entry point & tab navigator
```

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3.8+ is installed on your machine.

### 2. Install Dependencies
Install Flask and Flask-CORS using `pip`:
```bash
pip install flask flask-cors
```

### 3. Start the Application Server
Run `app.py` from the project directory:
```bash
python app.py
```

### 4. Open in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```
*(The Flask server automatically hosts the SPA frontend at the root URL).*

---

## 🗺️ Frontend Pages to Backend Mapping

| Frontend Page / Component | User Action | Mapped Backend Function / API Endpoint |
| :--- | :--- | :--- |
| **Dashboard** | View system overview stats | `GET /api/stats` (Aggregates `students`, `courses`, and `students.courses`) |
| **Students Directory** | View all students | `GET /api/students` (Iterates over `Part_1.students`) |
| **Students Directory** | Add new student | `POST /api/students` -> `Part_1.Student(name, id, year)` |
| **Students Directory** | Edit student name/year | `PUT /api/students/<id>` -> `Student.update_student()` |
| **Students Directory** | Delete student | `DELETE /api/students/<id>` -> `Student.del_update()` |
| **Students Directory** | Calculate Student GPA | `GET /api/students/<id>/gpa` -> `Part_3.calculate_gpa()` & `convert_to_gpa()` |
| **Students Directory** | View Student Report | `GET /api/students/<id>/report` -> `Student.display()` |
| **Course Catalog** | View all courses | `GET /api/courses` (Iterates over `part_2.courses`) |
| **Course Catalog** | Create new course | `POST /api/courses` -> `part_2.add_new_course()` |
| **Course Catalog** | Edit course details | `PUT /api/courses/<id>` -> `Course.update_course()` |
| **Course Catalog** | Delete course | `DELETE /api/courses/<id>` -> `Course.delete_course()` |
| **Course Catalog** | Compute Class Average | `GET /api/courses/<id>/average` -> `part_2.average_course()` |
| **Course Catalog** | View Course Report | `GET /api/courses/<id>/report` -> `Course.course_report()` |
| **Enrollment & Grades** | Sign up student for course | `POST /api/students/<id>/enroll` -> `Student.student_course()` |
| **Enrollment & Grades** | Record student grade | `POST /api/courses/<id>/grade` -> `Course.add_grade()` |
| **Global Search Bar** | Search students/courses | `GET /api/search?query=...` -> `Part_3.search_student_*` & `search_course_*` |
| **Database & Reports** | Save JSON database | `POST /api/database/save` -> `part_4.save_students()` |
| **Database & Reports** | Load JSON database | `POST /api/database/load` -> `part_4.load_students()` |
| **Database & Reports** | Export CSV | `POST /api/database/export-csv` -> `part_4.export_to_csv()` |
| **Database & Reports** | Download CSV File | `GET /api/database/download-csv` -> Downloads `report.csv` |

---

## 📡 REST API Documentation

### 1. Stats
- **`GET /api/stats`**
  - **Description**: Returns overall system metrics (total students, courses, enrollments, recorded grades).
  - **Response**:
    ```json
    {
      "status": "success",
      "total_students": 5,
      "total_courses": 3,
      "total_enrollments": 8,
      "total_grades_recorded": 6
    }
    ```

### 2. Students API
- **`GET /api/students`**: Retrieve all registered students.
- **`POST /api/students`**: Add a new student.
  - **Payload**: `{ "id": "101", "name": "Alice Smith", "year": "2nd Year" }`
- **`GET /api/students/<id>`**: Retrieve single student details.
- **`PUT /api/students/<id>`**: Update student name or academic year.
- **`DELETE /api/students/<id>`**: Delete a student.
- **`POST /api/students/<id>/enroll`**: Enroll student in course(s).
  - **Payload**: `{ "course_ids": ["CS101", "MATH201"] }`
- **`GET /api/students/<id>/gpa`**: Calculate 4.0 weighted GPA for a student.
- **`GET /api/students/<id>/report`**: Retrieve comprehensive student report.

### 3. Courses API
- **`GET /api/courses`**: Retrieve all courses in catalog.
- **`POST /api/courses`**: Add a new course.
  - **Payload**: `{ "id_course": "CS101", "name_course": "Computer Science I", "credit_hours": 3 }`
- **`GET /api/courses/<id>`**: Retrieve single course details.
- **`PUT /api/courses/<id>`**: Update course name or credit hours.
- **`DELETE /api/courses/<id>`**: Delete a course.
- **`POST /api/courses/<id>/grade`**: Record a student grade for a course.
  - **Payload**: `{ "student_id": "101", "grade": 92.5 }`
- **`GET /api/courses/<id>/average`**: Compute grade average, highest, and lowest score.
- **`GET /api/courses/<id>/report`**: Retrieve full course report and grade ledger.

### 4. Search API
- **`GET /api/search?query=cs101&type=all`**: Search students and courses by ID or Name.

### 5. Database & CSV Reports API
- **`POST /api/database/save`**: Save database state to `student.json`.
- **`POST /api/database/load`**: Load database state from `student.json`.
- **`POST /api/database/export-csv`**: Generate `report.csv` spreadsheet.
- **`GET /api/database/download-csv`**: Download `report.csv` file directly.

---

## 🎨 Design Features
- **Modern Glassmorphism Theme**: Dark slate palette (`#0b0f19`) with glowing indigo, cyan, and emerald badges.
- **Micro-Animations**: Smooth tab switching, card hover elevations, and animated toast alerts.
- **Real-Time Validation**: Field checks, error handling, loading spinners, and empty state fallbacks.
