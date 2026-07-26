/**
 * Main Front-End Application Orchestrator
 */
import { API } from './api.js';
import { UI } from './ui.js';
import { StudentsUI } from './students.js';
import { CoursesUI } from './courses.js';
import { EnrollmentUI } from './enrollment.js';
import { ReportsUI } from './reports.js';

// Expose modules to window scope for inline onclick handlers
window.StudentsUI = StudentsUI;
window.CoursesUI = CoursesUI;
window.EnrollmentUI = EnrollmentUI;
window.ReportsUI = ReportsUI;
window.UI = UI;

export const App = {
  async init() {
    console.log('[SPA] Initializing Student and Course System UI');
    this.setupTabNavigation();
    this.setupGlobalSearch();
    this.setupModalDismissal();

    // Initialize sub-controllers
    await StudentsUI.init();
    await CoursesUI.init();
    await EnrollmentUI.init();
    ReportsUI.init();

    await this.updateStats();
  },

  setupTabNavigation() {
    const navLinks = document.querySelectorAll('.nav-link[data-tab]');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const tabId = link.getAttribute('data-tab');
        this.switchTab(tabId);
      });
    });
  },

  switchTab(tabId) {
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
      if (link.getAttribute('data-tab') === tabId) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // Update active section view
    document.querySelectorAll('.view-section').forEach(section => {
      if (section.id === `${tabId}-section`) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });

    // Refresh specific section data when navigated to
    if (tabId === 'students') StudentsUI.loadStudents();
    if (tabId === 'courses') CoursesUI.loadCourses();
    if (tabId === 'enrollment') EnrollmentUI.populateDropdowns();

    this.updateStats();
  },

  async updateStats() {
    try {
      const res = await API.getStats();
      const data = res;

      const totalStudentsEl = document.getElementById('stat-total-students');
      if (totalStudentsEl) totalStudentsEl.textContent = data.total_students || 0;

      const totalCoursesEl = document.getElementById('stat-total-courses');
      if (totalCoursesEl) totalCoursesEl.textContent = data.total_courses || 0;

      const totalEnrollmentsEl = document.getElementById('stat-total-enrollments');
      if (totalEnrollmentsEl) totalEnrollmentsEl.textContent = data.total_enrollments || 0;

      const totalGradesEl = document.getElementById('stat-total-grades');
      if (totalGradesEl) totalGradesEl.textContent = data.total_grades_recorded || 0;
    } catch (err) {
      console.warn('Failed to fetch system stats:', err);
    }
  },

  setupGlobalSearch() {
    const globalSearchInput = document.getElementById('global-search-input');
    if (globalSearchInput) {
      let timeout = null;
      globalSearchInput.addEventListener('input', (e) => {
        clearTimeout(timeout);
        const query = e.target.value.trim();
        timeout = setTimeout(() => this.handleGlobalSearch(query), 300);
      });
    }
  },

  async handleGlobalSearch(query) {
    if (!query) return;

    try {
      const res = await API.search(query, 'all');
      console.log('Global Search Results:', res);
      // Automatically switch to Students or Courses tab if results match
      if (res.students && res.students.length > 0) {
        this.switchTab('students');
        StudentsUI.renderTable(res.students);
        UI.showToast(`Found ${res.students.length} matching student(s)`, 'info');
      } else if (res.courses && res.courses.length > 0) {
        this.switchTab('courses');
        CoursesUI.renderTable(res.courses);
        UI.showToast(`Found ${res.courses.length} matching course(s)`, 'info');
      } else {
        UI.showToast(`No records matching '${query}'`, 'info');
      }
    } catch (err) {
      console.error('Global search error:', err);
    }
  },

  setupModalDismissal() {
    // Click outside modal or close button click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
          backdrop.classList.remove('show');
        }
      });
    });

    document.querySelectorAll('.modal-close, [data-dismiss="modal"]').forEach(btn => {
      btn.addEventListener('click', () => {
        const backdrop = btn.closest('.modal-backdrop');
        if (backdrop) backdrop.classList.remove('show');
      });
    });
  }
};

window.App = App;

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
