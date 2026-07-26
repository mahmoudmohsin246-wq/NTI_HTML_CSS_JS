/**
 * Enrollment & Grade Recording UI Controller
 */
import { API } from './api.js';
import { UI } from './ui.js';

export const EnrollmentUI = {
  async init() {
    this.bindEvents();
    await this.populateDropdowns();
  },

  bindEvents() {
    // Enroll Form Submit
    const enrollForm = document.getElementById('enroll-form');
    if (enrollForm) {
      enrollForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleEnrollment();
      });
    }

    // Grade Form Submit
    const gradeForm = document.getElementById('grade-form');
    if (gradeForm) {
      gradeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleRegisterGrade();
      });
    }
  },

  async populateDropdowns() {
    try {
      const [studentsRes, coursesRes] = await Promise.all([
        API.getStudents(),
        API.getCourses()
      ]);

      const students = studentsRes.data || [];
      const courses = coursesRes.data || [];

      // Enroll Student Dropdown
      const enrollStudentSelect = document.getElementById('enroll-student-select');
      if (enrollStudentSelect) {
        enrollStudentSelect.innerHTML = '<option value="">-- Select Student --</option>' +
          students.map(s => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`).join('');
      }

      // Enroll Course Select
      const enrollCourseSelect = document.getElementById('enroll-course-select');
      if (enrollCourseSelect) {
        enrollCourseSelect.innerHTML = '<option value="">-- Select Course --</option>' +
          courses.map(c => `<option value="${c.id}">${c.name} (${c.id}) - ${c.credit_hours} Credits</option>`).join('');
      }

      // Grade Course Select
      const gradeCourseSelect = document.getElementById('grade-course-select');
      if (gradeCourseSelect) {
        gradeCourseSelect.innerHTML = '<option value="">-- Select Course --</option>' +
          courses.map(c => `<option value="${c.id}">${c.name} (${c.id})</option>`).join('');
      }

      // Grade Student Select
      const gradeStudentSelect = document.getElementById('grade-student-select');
      if (gradeStudentSelect) {
        gradeStudentSelect.innerHTML = '<option value="">-- Select Student --</option>' +
          students.map(s => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`).join('');
      }
    } catch (err) {
      console.error('Failed to populate dropdowns:', err);
    }
  },

  async handleEnrollment() {
    const studentId = document.getElementById('enroll-student-select').value;
    const courseId = document.getElementById('enroll-course-select').value;

    if (!studentId || !courseId) {
      UI.showToast('Please select both a student and a course.', 'error');
      return;
    }

    try {
      const res = await API.enrollStudent(studentId, [courseId]);
      UI.showToast(res.message, 'success');
      document.getElementById('enroll-form').reset();
      if (window.StudentsUI) window.StudentsUI.loadStudents();
      if (window.CoursesUI) window.CoursesUI.loadCourses();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  async handleRegisterGrade() {
    const courseId = document.getElementById('grade-course-select').value;
    const studentId = document.getElementById('grade-student-select').value;
    const grade = document.getElementById('grade-input').value;

    if (!courseId || !studentId || grade === '') {
      UI.showToast('Please fill out all fields in the grade form.', 'error');
      return;
    }

    try {
      const res = await API.registerGrade(courseId, studentId, grade);
      UI.showToast(res.message, 'success');
      document.getElementById('grade-form').reset();
      if (window.CoursesUI) window.CoursesUI.loadCourses();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  }
};
