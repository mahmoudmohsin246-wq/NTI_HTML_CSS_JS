/**
 * Database Backup, Restore, and CSV Export Controller
 */
import { API } from './api.js';
import { UI } from './ui.js';

export const ReportsUI = {
  init() {
    this.bindEvents();
  },

  bindEvents() {
    const saveBtn = document.getElementById('save-db-btn');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => this.handleSaveDatabase());
    }

    const loadBtn = document.getElementById('load-db-btn');
    if (loadBtn) {
      loadBtn.addEventListener('click', () => this.handleLoadDatabase());
    }

    const exportCsvBtn = document.getElementById('export-csv-btn');
    if (exportCsvBtn) {
      exportCsvBtn.addEventListener('click', () => this.handleExportCSV());
    }

    const downloadCsvBtn = document.getElementById('download-csv-btn');
    if (downloadCsvBtn) {
      downloadCsvBtn.addEventListener('click', () => this.handleDownloadCSV());
    }
  },

  async handleSaveDatabase() {
    try {
      const res = await API.saveDatabase();
      UI.showToast(res.message, 'success');
    } catch (err) {
      UI.showToast(`Save failed: ${err.message}`, 'error');
    }
  },

  async handleLoadDatabase() {
    try {
      const res = await API.loadDatabase();
      UI.showToast(res.message, 'success');
      // Refresh views
      if (window.StudentsUI) window.StudentsUI.loadStudents();
      if (window.CoursesUI) window.CoursesUI.loadCourses();
      if (window.EnrollmentUI) window.EnrollmentUI.populateDropdowns();
      if (window.App) window.App.updateStats();
    } catch (err) {
      UI.showToast(`Load failed: ${err.message}`, 'error');
    }
  },

  async handleExportCSV() {
    try {
      const res = await API.exportCSV();
      UI.showToast(res.message, 'success');
    } catch (err) {
      UI.showToast(`CSV Export failed: ${err.message}`, 'error');
    }
  },

  handleDownloadCSV() {
    const downloadUrl = API.getDownloadCSVUrl();
    window.open(downloadUrl, '_blank');
    UI.showToast('CSV Report download initiated...', 'info');
  }
};
