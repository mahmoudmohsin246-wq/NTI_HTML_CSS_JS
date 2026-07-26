/**
 * Students Management UI Controller
 */
import { API } from './api.js';
import { UI } from './ui.js';

export const StudentsUI = {
  studentsList: [],

  async init() {
    this.bindEvents();
    await this.loadStudents();
  },

  bindEvents() {
    // Add Student Form Submit
    const addForm = document.getElementById('add-student-form');
    if (addForm) {
      addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleAddStudent();
      });
    }

    // Edit Student Form Submit
    const editForm = document.getElementById('edit-student-form');
    if (editForm) {
      editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleEditStudent();
      });
    }

    // Search input listener
    const searchInput = document.getElementById('student-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.filterStudents(e.target.value);
      });
    }
  },

  async loadStudents() {
    UI.showLoading('students-table-container');
    try {
      const res = await API.getStudents();
      this.studentsList = res.data || [];
      this.renderTable(this.studentsList);
    } catch (err) {
      UI.showToast(`Failed to load students: ${err.message}`, 'error');
      UI.renderEmpty('students-table-container', 'Failed to load students.');
    }
  },

  renderTable(students) {
    const container = document.getElementById('students-table-container');
    if (!container) return;

    if (!students || students.length === 0) {
      UI.renderEmpty('students-table-container', 'No students registered yet.');
      return;
    }

    let rows = students.map(s => {
      const coursesCount = s.courses ? s.courses.length : 0;
      const coursesTags = s.courses && s.courses.length > 0
        ? s.courses.map(c => `<span class="badge badge-cyan">${c.name || c}</span>`).join(' ')
        : '<span class="badge badge-amber">None</span>';

      return `
        <tr>
          <td><strong>${s.id}</strong></td>
          <td>${s.name}</td>
          <td><span class="badge badge-indigo">Year ${s.year}</span></td>
          <td>${coursesTags}</td>
          <td>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
              <button class="btn btn-secondary btn-sm" onclick="window.StudentsUI.openReport('${s.id}')">Report</button>
              <button class="btn btn-accent btn-sm" onclick="window.StudentsUI.openGPA('${s.id}')">GPA</button>
              <button class="btn btn-secondary btn-sm" onclick="window.StudentsUI.openEdit('${s.id}')">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="window.StudentsUI.deleteStudent('${s.id}')">Delete</button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    container.innerHTML = `
      <table class="custom-table">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Full Name</th>
            <th>Academic Year</th>
            <th>Enrolled Courses (${students.length})</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    `;
  },

  filterStudents(query) {
    if (!query) {
      this.renderTable(this.studentsList);
      return;
    }
    const q = query.toLowerCase();
    const filtered = this.studentsList.filter(s =>
      s.id.toLowerCase().includes(q) || s.name.toLowerCase().includes(q) || s.year.toLowerCase().includes(q)
    );
    this.renderTable(filtered);
  },

  async handleAddStudent() {
    const name = document.getElementById('student-name-input').value.trim();
    const id = document.getElementById('student-id-input').value.trim();
    const year = document.getElementById('student-year-input').value.trim();

    try {
      const res = await API.addStudent({ name, id, year });
      UI.showToast(res.message, 'success');
      UI.hideModal('add-student-modal');
      document.getElementById('add-student-form').reset();
      await this.loadStudents();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  openEdit(id) {
    const student = this.studentsList.find(s => s.id === id);
    if (!student) return;

    document.getElementById('edit-student-id').value = student.id;
    document.getElementById('edit-student-name').value = student.name;
    document.getElementById('edit-student-year').value = student.year;
    UI.showModal('edit-student-modal');
  },

  async handleEditStudent() {
    const id = document.getElementById('edit-student-id').value;
    const name = document.getElementById('edit-student-name').value.trim();
    const year = document.getElementById('edit-student-year').value.trim();

    try {
      const res = await API.updateStudent(id, { name, year });
      UI.showToast(res.message, 'success');
      UI.hideModal('edit-student-modal');
      await this.loadStudents();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  async deleteStudent(id) {
    if (!confirm(`Are you sure you want to delete student ID ${id}?`)) return;

    try {
      const res = await API.deleteStudent(id);
      UI.showToast(res.message, 'success');
      await this.loadStudents();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  async openGPA(id) {
    try {
      const res = await API.getStudentGPA(id);
      const data = res.data;

      document.getElementById('gpa-student-info').innerHTML = `
        <h3>${data.student_name} (ID: ${data.student_id})</h3>
        <p style="margin-top: 6px; font-size: 1.1rem;">
          Weighted GPA: <strong style="color: #6366f1; font-size: 1.6rem;">${data.gpa} / 4.0</strong>
        </p>
        <p style="color: var(--text-muted); font-size: 0.85rem;">Total Evaluated Credit Hours: ${data.total_credit_hours}</p>
      `;

      const coursesTable = document.getElementById('gpa-courses-list');
      if (data.evaluated_courses && data.evaluated_courses.length > 0) {
        let rows = data.evaluated_courses.map(c => `
          <tr>
            <td>${c.course_name} (${c.course_id})</td>
            <td>${c.credit_hours} hrs</td>
            <td>${c.numeric_grade}%</td>
            <td><strong style="color: #10b981;">${c.gpa_point.toFixed(1)}</strong></td>
          </tr>
        `).join('');

        coursesTable.innerHTML = `
          <table class="custom-table" style="margin-top: 16px;">
            <thead>
              <tr>
                <th>Course</th>
                <th>Credits</th>
                <th>Score</th>
                <th>GPA Points</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        `;
      } else {
        coursesTable.innerHTML = `<p style="margin-top: 16px; color: var(--text-muted);">No graded courses evaluated yet for this student.</p>`;
      }

      UI.showModal('gpa-modal');
    } catch (err) {
      UI.showToast(`Failed to calculate GPA: ${err.message}`, 'error');
    }
  },

  async openReport(id) {
    try {
      const res = await API.getStudentReport(id);
      const data = res.data;
      const s = data.student;
      const gpa = data.gpa_summary;

      const coursesListHtml = s.courses && s.courses.length > 0
        ? s.courses.map(c => `<li style="margin-bottom: 6px;"><strong>${c.name || c}</strong> (ID: ${c.id || 'N/A'}, ${c.credit_hours || '?'} Credit Hours)</li>`).join('')
        : '<li>No courses registered.</li>';

      document.getElementById('report-body').innerHTML = `
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 12px; border: 1px solid var(--border-glass);">
          <h2 style="color: #a5b4fc; font-family: Outfit; font-size: 1.4rem;">Student Report: ${s.name}</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; font-size: 0.92rem;">
            <div><strong>Student ID:</strong> ${s.id}</div>
            <div><strong>Academic Year:</strong> Year ${s.year}</div>
            <div><strong>Calculated GPA:</strong> <span style="color: #10b981; font-weight: bold;">${gpa.gpa || 0.0}</span></div>
            <div><strong>Evaluated Credits:</strong> ${gpa.total_credit_hours || 0} hrs</div>
          </div>
          <hr style="border-color: var(--border-glass); margin: 16px 0;">
          <h4 style="color: var(--text-muted); margin-bottom: 8px;">Registered Courses:</h4>
          <ul style="padding-left: 20px; color: var(--text-main);">
            ${coursesListHtml}
          </ul>
        </div>
      `;

      UI.showModal('student-report-modal');
    } catch (err) {
      UI.showToast(`Failed to generate report: ${err.message}`, 'error');
    }
  }
};
