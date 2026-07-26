/**
 * API Client Layer for Student and Course System Backend
 */
const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  };

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `HTTP error ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`[API Error] ${endpoint}:`, error);
    throw error;
  }
}

export const API = {
  // Stats
  getStats: () => request('/stats'),

  // Students
  getStudents: () => request('/students'),
  getStudent: (id) => request(`/students/${id}`),
  addStudent: (data) => request('/students', { method: 'POST', body: data }),
  updateStudent: (id, data) => request(`/students/${id}`, { method: 'PUT', body: data }),
  deleteStudent: (id) => request(`/students/${id}`, { method: 'DELETE' }),
  enrollStudent: (id, courseIds) => request(`/students/${id}/enroll`, { method: 'POST', body: { course_ids: courseIds } }),
  getStudentGPA: (id) => request(`/students/${id}/gpa`),
  getStudentReport: (id) => request(`/students/${id}/report`),

  // Courses
  getCourses: () => request('/courses'),
  getCourse: (id) => request(`/courses/${id}`),
  addCourse: (data) => request('/courses', { method: 'POST', body: data }),
  updateCourse: (id, data) => request(`/courses/${id}`, { method: 'PUT', body: data }),
  deleteCourse: (id) => request(`/courses/${id}`, { method: 'DELETE' }),
  registerGrade: (courseId, studentId, grade) => request(`/courses/${courseId}/grade`, { method: 'POST', body: { student_id: studentId, grade: parseFloat(grade) } }),
  getCourseAverage: (id) => request(`/courses/${id}/average`),
  getCourseReport: (id) => request(`/courses/${id}/report`),

  // Search
  search: (query, type = 'all') => request(`/search?query=${encodeURIComponent(query)}&type=${type}`),

  // Database & Export
  saveDatabase: () => request('/database/save', { method: 'POST' }),
  loadDatabase: () => request('/database/load', { method: 'POST' }),
  exportCSV: () => request('/database/export-csv', { method: 'POST' }),
  getDownloadCSVUrl: () => `${API_BASE}/database/download-csv`
};
