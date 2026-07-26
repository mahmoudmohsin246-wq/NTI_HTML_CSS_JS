/**
 * Courses Management UI Controller
 */
import { API } from './api.js';
import { UI } from './ui.js';

export const CoursesUI = {
  coursesList: [],

  async init() {
    this.bindEvents();
    await this.loadCourses();
  },

  bindEvents() {
    // Add Course Form Submit
    const addForm = document.getElementById('add-course-form');
    if (addForm) {
      addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleAddCourse();
      });
    }

    // Edit Course Form Submit
    const editForm = document.getElementById('edit-course-form');
    if (editForm) {
      editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleEditCourse();
      });
    }

    // Search input listener
    const searchInput = document.getElementById('course-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.filterCourses(e.target.value);
      });
    }
  },

  async loadCourses() {
    UI.showLoading('courses-table-container');
    try {
      const res = await API.getCourses();
      this.coursesList = res.data || [];
      this.renderTable(this.coursesList);
    } catch (err) {
      UI.showToast(`Failed to load courses: ${err.message}`, 'error');
      UI.renderEmpty('courses-table-container', 'Failed to load courses.');
    }
  },

  renderTable(coursesList) {
    const container = document.getElementById('courses-table-container');
    if (!container) return;

    if (!coursesList || coursesList.length === 0) {
      UI.renderEmpty('courses-table-container', 'No courses added yet.');
      return;
    }

    let rows = coursesList.map(c => {
      const gradedStudentsCount = c.students ? Object.keys(c.students).length : 0;
      return `
        <tr>
          <td><strong>${c.id}</strong></td>
          <td>${c.name}</td>
          <td><span class="badge badge-cyan">${c.credit_hours} Credit Hours</span></td>
          <td><span class="badge badge-indigo">${gradedStudentsCount} Graded</span></td>
          <td>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
              <button class="btn btn-secondary btn-sm" onclick="window.CoursesUI.openReport('${c.id}')">Report</button>
              <button class="btn btn-accent btn-sm" onclick="window.CoursesUI.openAverage('${c.id}')">Average</button>
              <button class="btn btn-secondary btn-sm" onclick="window.CoursesUI.openEdit('${c.id}')">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="window.CoursesUI.deleteCourse('${c.id}')">Delete</button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    container.innerHTML = `
      <table class="custom-table">
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Credit Hours</th>
            <th>Grades Recorded</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    `;
  },

  filterCourses(query) {
    if (!query) {
      this.renderTable(this.coursesList);
      return;
    }
    const q = query.toLowerCase();
    const filtered = this.coursesList.filter(c =>
      c.id.toLowerCase().includes(q) || c.name.toLowerCase().includes(q)
    );
    this.renderTable(filtered);
  },

  async handleAddCourse() {
    const id_course = document.getElementById('course-id-input').value.trim();
    const name_course = document.getElementById('course-name-input').value.trim();
    const credit_hours = document.getElementById('course-hours-input').value.trim();

    try {
      const res = await API.addCourse({ id_course, name_course, credit_hours });
      UI.showToast(res.message, 'success');
      UI.hideModal('add-course-modal');
      document.getElementById('add-course-form').reset();
      await this.loadCourses();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  openEdit(id) {
    const course = this.coursesList.find(c => c.id === id);
    if (!course) return;

    document.getElementById('edit-course-id').value = course.id;
    document.getElementById('edit-course-name').value = course.name;
    document.getElementById('edit-course-hours').value = course.credit_hours;
    UI.showModal('edit-course-modal');
  },

  async handleEditCourse() {
    const id = document.getElementById('edit-course-id').value;
    const name_course = document.getElementById('edit-course-name').value.trim();
    const credit_hours = document.getElementById('edit-course-hours').value.trim();

    try {
      const res = await API.updateCourse(id, { name_course, credit_hours });
      UI.showToast(res.message, 'success');
      UI.hideModal('edit-course-modal');
      await this.loadCourses();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  async deleteCourse(id) {
    if (!confirm(`Are you sure you want to delete course ID ${id}?`)) return;

    try {
      const res = await API.deleteCourse(id);
      UI.showToast(res.message, 'success');
      await this.loadCourses();
    } catch (err) {
      UI.showToast(err.message, 'error');
    }
  },

  async openAverage(id) {
    try {
      const res = await API.getCourseAverage(id);
      const data = res.data;

      const avgText = data.average !== null ? `${data.average}%` : 'N/A';
      document.getElementById('average-course-info').innerHTML = `
        <h3>Course: ${data.course_name} (ID: ${data.course_id})</h3>
        <p style="margin-top: 10px; font-size: 1.1rem;">
          Average Grade: <strong style="color: #06b6d4; font-size: 1.6rem;">${avgText}</strong>
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 14px; text-align: center;">
          <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: var(--text-muted);">TOTAL GRADED</div>
            <div style="font-weight: bold; font-size: 1.2rem; margin-top: 4px;">${data.total_students}</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: var(--text-muted);">HIGHEST</div>
            <div style="font-weight: bold; font-size: 1.2rem; color: #10b981; margin-top: 4px;">${data.highest_grade !== null ? data.highest_grade : '-'}</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: var(--text-muted);">LOWEST</div>
            <div style="font-weight: bold; font-size: 1.2rem; color: #ef4444; margin-top: 4px;">${data.lowest_grade !== null ? data.lowest_grade : '-'}</div>
          </div>
        </div>
      `;

      UI.showModal('average-modal');
    } catch (err) {
      UI.showToast(`Failed to compute average: ${err.message}`, 'error');
    }
  },

  async openReport(id) {
    try {
      const res = await API.getCourseReport(id);
      const data = res.data;
      const c = data.course;
      const stats = data.stats;

      let gradesTableRows = '';
      if (c.students && Object.keys(c.students).length > 0) {
        gradesTableRows = Object.entries(c.students).map(([student, grade]) => `
          <tr>
            <td>${student}</td>
            <td><strong>${grade}%</strong></td>
          </tr>
        `).join('');
      } else {
        gradesTableRows = `<tr><td colspan="2" style="text-align: center; color: var(--text-muted);">No grades recorded yet.</td></tr>`;
      }

      document.getElementById('course-report-body').innerHTML = `
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 12px; border: 1px solid var(--border-glass);">
          <h2 style="color: #67e8f9; font-family: Outfit; font-size: 1.4rem;">Course Report: ${c.name}</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; font-size: 0.92rem;">
            <div><strong>Course ID:</strong> ${c.id}</div>
            <div><strong>Credit Hours:</strong> ${c.credit_hours} hrs</div>
            <div><strong>Average Grade:</strong> <span style="color: #06b6d4; font-weight: bold;">${stats.average !== null ? stats.average + '%' : 'N/A'}</span></div>
            <div><strong>Total Enrolled Graded:</strong> ${stats.total_students || 0}</div>
          </div>
          <hr style="border-color: var(--border-glass); margin: 16px 0;">
          <h4 style="color: var(--text-muted); margin-bottom: 10px;">Student Grade Ledger:</h4>
          <table class="custom-table">
            <thead>
              <tr>
                <th>Student ID / Name</th>
                <th>Grade Score</th>
              </tr>
            </thead>
            <tbody>
              ${gradesTableRows}
            </tbody>
          </table>
        </div>
      `;

      UI.showModal('course-report-modal');
    } catch (err) {
      UI.showToast(`Failed to generate course report: ${err.message}`, 'error');
    }
  }
};
