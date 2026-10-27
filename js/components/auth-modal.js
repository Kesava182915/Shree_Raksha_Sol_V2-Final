/**
 * SHREERAKSHA SOLUTIONS - ENTERPRISE USER PROFILE & ACCESS MODULE
 * Login features and admin icon removed per user requirement.
 * Application operates directly in authenticated Administrator mode with 100% full access.
 */

(function (window) {
  'use strict';

  const TOKEN_KEY = 'shreeraksha_auth_token';
  const USER_KEY = 'shreeraksha_auth_user';

  const DEFAULT_USER = {
    id: 'usr-admin-1',
    name: 'Shreeraksha Solutions',
    role: 'admin',
    email: 'connect@shreeraksha.in',
    phone: '+91 9880 54 99 55'
  };

  const AuthManager = {
    currentUser: Object.assign({}, DEFAULT_USER),
    currentRole: 'admin',
    selectedRole: 'admin',
    token: 'permanent_enterprise_admin_token',

    init() {
      // Ensure local storage has default admin user and permanent token
      try {
        localStorage.setItem(TOKEN_KEY, this.token);
        localStorage.setItem(USER_KEY, JSON.stringify(this.currentUser));
      } catch (e) {}

      // Remove any leftover login overlay backdrops from DOM
      this.closeModal();

      // Admin icon removed from top header per user request
      this.renderHeaderProfile();
      this.syncSidebar();

      // Ensure active route renders immediately
      if (window.App && typeof window.App.handleRoute === 'function') {
        window.App.handleRoute();
      }
    },

    renderAuthOverlay() {
      // Login feature removed: No login overlay rendered
      const existing = document.getElementById('auth-overlay-backdrop');
      if (existing) existing.remove();
    },

    renderHeaderProfile() {
      // Admin icon completely removed from top header per user request
      const existing = document.getElementById('header-user-profile-wrap');
      if (existing) existing.remove();
    },

    bindHeaderEvents() {
      // Header profile widget removed
    },

    syncSidebar() {
      const sbName = document.querySelector('.sidebar-footer .user-name');
      const sbRole = document.querySelector('.sidebar-footer .user-role');
      const sbAvatar = document.querySelector('.sidebar-footer .user-avatar');

      if (sbName) sbName.textContent = this.currentUser.name;
      if (sbRole) sbRole.textContent = 'GST Compliance Admin';
      if (sbAvatar) sbAvatar.textContent = 'SR';
    },

    // Safe compatibility methods for zero functional defects
    openModal() {
      // Login feature removed: No modal opened
    },

    closeModal() {
      const overlay = document.getElementById('auth-overlay-backdrop');
      if (overlay) overlay.remove();
    },

    checkSession() {
      return true;
    },

    isAuthenticated() {
      return true;
    },

    setRole(role) {
      this.selectedRole = role || 'admin';
      this.currentRole = this.selectedRole;
      if (this.currentUser) this.currentUser.role = this.selectedRole;
    },

    applyUserSession(user) {
      if (user) {
        this.currentUser = Object.assign({}, DEFAULT_USER, user);
        this.selectedRole = this.currentUser.role || 'admin';
        this.currentRole = this.selectedRole;
      }
      this.syncSidebar();
    },

    toggleUserRole(nextRole) {
      const targetRole = nextRole || (this.selectedRole === 'admin' ? 'customer' : 'admin');
      this.setRole(targetRole);
      if (window.Toast) {
        window.Toast.show(`Viewing suite with ${targetRole.toUpperCase()} permissions`, 'info');
      }
    },

    logout() {
      if (window.Toast) {
        window.Toast.show('Direct access mode: Login is disabled. Full suite access remains active.', 'info');
      }
    },

    // Mock API methods resolving immediately with success
    async submitSignIn(identifier, password, role) {
      this.setRole(role || 'admin');
      return { success: true, user: this.currentUser, token: this.token };
    },

    async submitSignUp(payload) {
      return { success: true, user: this.currentUser, token: this.token };
    },

    async submitSendOtp(identifier, purpose) {
      return { success: true, otp: '123456' };
    },

    async submitVerifyOtp(identifier, code, role) {
      this.setRole(role || 'admin');
      return { success: true, user: this.currentUser, token: this.token };
    },

    async submitForgotPasswordOtp(identifier) {
      return { success: true, otp: '123456' };
    },

    async submitResetPassword(identifier, code, newPassword) {
      return { success: true, message: 'Password reset' };
    }
  };

  window.AuthManager = AuthManager;
  window.Auth = AuthManager;

})(window);
