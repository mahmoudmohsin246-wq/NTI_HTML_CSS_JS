/**
 * UI Utilities and Notification Helpers
 */

export const UI = {
  showToast(message, type = 'info', duration = 3500) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';

    toast.innerHTML = `
      <span>${icon}</span>
      <div style="flex: 1;">${message}</div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  showModal(modalId) {
    const backdrop = document.getElementById(modalId);
    if (backdrop) {
      backdrop.classList.add('show');
    }
  },

  hideModal(modalId) {
    const backdrop = document.getElementById(modalId);
    if (backdrop) {
      backdrop.classList.remove('show');
    }
  },

  showLoading(elementId, text = 'Loading data...') {
    const el = document.getElementById(elementId);
    if (el) {
      el.innerHTML = `
        <div class="loading-state">
          <div class="spinner"></div>
          <p>${text}</p>
        </div>
      `;
    }
  },

  renderEmpty(elementId, message = 'No records found.') {
    const el = document.getElementById(elementId);
    if (el) {
      el.innerHTML = `
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
          <p>${message}</p>
        </div>
      `;
    }
  }
};
