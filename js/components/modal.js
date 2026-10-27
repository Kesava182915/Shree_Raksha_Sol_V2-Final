/**
 * ZOHO INVOICE - DYNAMIC MULTI-MODULE MODAL & DRAFT MINIMIZATION ENGINE
 * Supports per-window drafts (Quotations, Tax Invoices, Customers, Vendors / POs).
 * Clicking outside the popup or clicking minimize preserves all DOM data without saving.
 */

(function (window) {
  'use strict';

  const Modal = {
    activeModal: null,
    minimizedDrafts: {}, // { quotes: modalObj, invoices: modalObj, customers: modalObj, vendors: modalObj, general: modalObj }

    detectCurrentViewModule() {
      const h = (window.location.hash || '').toLowerCase();
      if (h.includes('quotes') || h.includes('estimate')) return 'quotes';
      if (h.includes('invoices')) return 'invoices';
      if (h.includes('customers')) return 'customers';
      if (h.includes('purchase-orders')) return 'vendors';
      return 'general';
    },

    detectModule(title = '', explicitModule = null) {
      if (explicitModule) return explicitModule;
      const t = (title || '').toLowerCase();
      const h = (window.location.hash || '').toLowerCase();
      if (t.includes('quotation') || t.includes('estimate') || h.includes('quotes')) return 'quotes';
      if (t.includes('invoice') || h.includes('invoices')) return 'invoices';
      if (t.includes('customer') || h.includes('customers')) return 'customers';
      if (t.includes('vendor') || t.includes('purchase order') || h.includes('purchase-orders')) return 'vendors';
      return 'general';
    },

    open({
      title = '',
      module = null,
      contentHtml = '',
      size = 'md', // 'sm', 'md', 'lg', 'xl', '2xl'
      onRender = null,
      onConfirm = null,
      confirmText = 'Save',
      cancelText = 'Cancel',
      confirmClass = 'btn-primary',
      showFooter = true,
      allowMinimize = true
    }) {
      const mod = this.detectModule(title, module);

      // If there is already a minimized draft for this module, resume it!
      if (this.minimizedDrafts[mod] && this.minimizedDrafts[mod].isMinimized) {
        this.restore(mod);
        if (window.Toast) {
          window.Toast.show(`Resumed your in-progress ${this.minimizedDrafts[mod].title} draft!`, 'info');
        }
        return;
      }

      // If an active modal is currently open on screen, minimize it
      if (this.activeModal && !this.activeModal.isMinimized) {
        if (this.activeModal.allowMinimize) {
          this.minimize();
        } else {
          this.forceClose();
        }
      }

      const mount = document.getElementById('modal-container');
      if (!mount) return;

      const backdrop = document.createElement('div');
      backdrop.className = 'modal-backdrop';
      backdrop.setAttribute('data-module', mod);

      backdrop.innerHTML = `
        <div class="modal-dialog modal-${size}" role="dialog" aria-modal="true">
          <div class="modal-header">
            <h3 class="modal-title">${title}</h3>
            <div class="modal-header-actions">
              ${allowMinimize ? `
              <button type="button" class="icon-btn-ghost btn-sm modal-minimize-btn" title="Minimize entry form (click outside or click here)" aria-label="Minimize modal">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
              ` : ''}
              <button type="button" class="icon-btn-ghost btn-sm modal-close-btn" title="Close" aria-label="Close modal">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
          </div>
          <div class="modal-body">
            ${contentHtml}
          </div>
          ${showFooter ? `
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary modal-cancel-btn">${cancelText}</button>
            <button type="button" class="btn ${confirmClass} modal-confirm-btn">${confirmText}</button>
          </div>
          ` : ''}
        </div>
      `;

      // Stop any click inside .modal-dialog from propagating to the backdrop
      const dialog = backdrop.querySelector('.modal-dialog');
      if (dialog) {
        dialog.addEventListener('click', (e) => {
          e.stopPropagation();
        });
      }

      // Event handlers
      const minimizeBtn = backdrop.querySelector('.modal-minimize-btn');
      if (minimizeBtn) {
        minimizeBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.minimize();
        });
      }

      const closeBtn = backdrop.querySelector('.modal-close-btn');
      if (closeBtn) {
        closeBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if (allowMinimize) {
            this.minimize();
          } else {
            this.forceClose();
          }
        });
      }

      const cancelBtn = backdrop.querySelector('.modal-cancel-btn');
      if (cancelBtn) {
        cancelBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if (allowMinimize) {
            this.minimize();
          } else {
            this.forceClose();
          }
        });
      }

      const confirmBtn = backdrop.querySelector('.modal-confirm-btn');
      if (confirmBtn && onConfirm) {
        confirmBtn.addEventListener('click', async (e) => {
          const shouldClose = await onConfirm(e, backdrop);
          if (shouldClose !== false) {
            this.forceClose(mod);
          }
        });
      }

      // CRITICAL REQUIREMENT: Clicking outside the popup entry form on backdrop
      // MUST NOT close/destroy it, and MUST NOT save it to database!
      // It MUST MINIMIZE IT TO THE BOTTOM, with all data preserved in the DOM!
      backdrop.addEventListener('click', (e) => {
        if (allowMinimize) {
          this.minimize();
        } else {
          this.forceClose();
        }
      });

      const keyHandler = (e) => {
        if (e.key === 'Escape') {
          if (this.activeModal && !this.activeModal.isMinimized) {
            if (allowMinimize) {
              this.minimize();
            } else {
              this.forceClose();
            }
          }
        }
      };
      document.addEventListener('keydown', keyHandler);

      mount.appendChild(backdrop);
      document.body.classList.add('modal-open');

      const modalObj = {
        backdrop,
        title,
        module: mod,
        size,
        allowMinimize,
        options: { title, module: mod, contentHtml, size, onRender, onConfirm, confirmText, cancelText, confirmClass, showFooter, allowMinimize },
        keyHandler,
        isMinimized: false
      };

      this.activeModal = modalObj;

      if (typeof onRender === 'function') {
        onRender(backdrop);
      }
    },

    /**
     * Minimizes the active modal to the bottom dock, preserving all data in the DOM
     */
    minimize() {
      if (!this.activeModal || this.activeModal.isMinimized) return;

      const modal = this.activeModal;
      modal.isMinimized = true;
      modal.backdrop.classList.add('modal-is-minimized');
      document.body.classList.remove('modal-open');

      this.minimizedDrafts[modal.module] = modal;
      this.activeModal = null;

      this.renderMinimizedDock();
      if (window.Toast) {
        window.Toast.show('Form minimized to bottom dock. Data is preserved (not saved yet).', 'info');
      }
    },

    /**
     * Restores the minimized modal to full view with all data intact
     */
    restore(targetModule = null) {
      let draft = null;
      if (targetModule && this.minimizedDrafts[targetModule]) {
        draft = this.minimizedDrafts[targetModule];
      } else {
        const curMod = this.detectCurrentViewModule();
        draft = this.minimizedDrafts[curMod] || Object.values(this.minimizedDrafts).find(d => d && d.isMinimized);
      }

      if (!draft || !draft.isMinimized) return;

      draft.isMinimized = false;
      draft.backdrop.classList.remove('modal-is-minimized');
      document.body.classList.add('modal-open');

      this.activeModal = draft;
      this.renderMinimizedDock();

      // Focus first input or active element
      const firstInput = draft.backdrop.querySelector('input:not([type="hidden"]), select, textarea');
      if (firstInput) {
        firstInput.focus();
      }
    },

    /**
     * Renders the floating dock at the bottom of the screen.
     * Shows the draft relevant to the active window/module (Quotation, Invoice, Customer, Vendor).
     */
    renderMinimizedDock() {
      this.removeMinimizedDock();

      const activeDrafts = Object.values(this.minimizedDrafts).filter(d => d && d.isMinimized);
      if (activeDrafts.length === 0) return;

      const curMod = this.detectCurrentViewModule();
      // Per user specification:
      // If draft was left in Quotation, Quotation draft minimized window should be visible in Quotations.
      // Same way Vendor, Customer, Tax Invoices should be visible in their respective windows.
      let currentDraft = this.minimizedDrafts[curMod];
      if (!currentDraft || !currentDraft.isMinimized) {
        if (curMod === 'quotes' || curMod === 'invoices' || curMod === 'customers' || curMod === 'vendors') {
          return; // No draft for this respective window
        }
        currentDraft = activeDrafts[0];
      }

      const modIcons = {
        quotes: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        invoices: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
        customers: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        vendors: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        general: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
      };

      const iconSvg = modIcons[currentDraft.module] || modIcons.general;
      const title = currentDraft.title || 'Entry Form';

      // Check if multiple drafts exist
      const multiDraftTabs = activeDrafts.length > 1 ? `
        <div class="minimized-dock-tabs">
          ${activeDrafts.map(d => `
            <button type="button" class="minimized-tab-pill ${d.module === currentDraft.module ? 'active' : ''}" data-mod="${d.module}">
              ${d.module === 'quotes' ? 'Quotation' : d.module === 'invoices' ? 'Tax Invoice' : d.module === 'customers' ? 'Customer' : d.module === 'vendors' ? 'Vendor/PO' : 'Draft'}
            </button>
          `).join('')}
        </div>
      ` : '';

      const dock = document.createElement('div');
      dock.id = 'modal-minimized-dock';
      dock.className = 'modal-minimized-dock animate-slideUp';

      dock.innerHTML = `
        <div class="minimized-dock-card" id="minimized-dock-card" title="Click anywhere to resume entry">
          <div class="minimized-dock-left">
            <div class="minimized-dock-icon">
              ${iconSvg}
            </div>
            <div class="minimized-dock-info">
              <div class="minimized-dock-title">${title}</div>
              <div class="minimized-dock-sub">
                <span class="minimized-live-pulse"></span>
                <span>Draft in progress &bull; Data preserved (not saved yet)</span>
              </div>
              ${multiDraftTabs}
            </div>
          </div>
          <div class="minimized-dock-actions">
            <button type="button" class="btn btn-primary btn-sm minimized-restore-btn" id="minimized-restore-btn" title="Expand and resume form">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
              <span>Resume</span>
            </button>
            <button type="button" class="minimized-discard-btn" id="minimized-discard-btn" title="Discard this entry" aria-label="Discard entry">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>
      `;

      dock.querySelector('.minimized-dock-left').addEventListener('click', (e) => {
        const tabBtn = e.target.closest('.minimized-tab-pill');
        if (tabBtn) {
          e.stopPropagation();
          const targetMod = tabBtn.getAttribute('data-mod');
          const modRouteMap = {
            quotes: '#quotes',
            invoices: '#invoices',
            customers: '#customers',
            vendors: '#purchase-orders'
          };
          if (modRouteMap[targetMod] && window.location.hash !== modRouteMap[targetMod]) {
            window.location.hash = modRouteMap[targetMod];
          }
          this.restore(targetMod);
          return;
        }
        this.restore(currentDraft.module);
      });

      dock.querySelector('#minimized-restore-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        this.restore(currentDraft.module);
      });

      dock.querySelector('#minimized-discard-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        if (confirm(`Discard this in-progress "${title}" and clear unsaved data?`)) {
          this.forceClose(currentDraft.module);
          if (window.Toast) {
            window.Toast.show('Draft discarded.', 'info');
          }
        }
      });

      document.body.appendChild(dock);
    },

    removeMinimizedDock() {
      const dock = document.getElementById('modal-minimized-dock');
      if (dock && dock.parentNode) {
        dock.remove();
      }
    },

    close() {
      this.forceClose();
    },

    forceClose(targetModule = null) {
      let mod = targetModule;
      if (!mod && this.activeModal) {
        mod = this.activeModal.module;
      }
      if (!mod) {
        mod = this.detectCurrentViewModule();
      }

      const modalToClose = (mod && this.minimizedDrafts[mod]) || this.activeModal;
      if (modalToClose) {
        if (modalToClose.keyHandler) {
          document.removeEventListener('keydown', modalToClose.keyHandler);
        }
        if (modalToClose.backdrop && modalToClose.backdrop.parentNode) {
          modalToClose.backdrop.remove();
        }
      }

      if (mod && this.minimizedDrafts[mod]) {
        delete this.minimizedDrafts[mod];
      }
      if (this.activeModal === modalToClose) {
        this.activeModal = null;
      }

      document.body.classList.remove('modal-open');
      this.renderMinimizedDock();
    },

    confirm({
      title = 'Are you sure?',
      message = 'This action cannot be undone.',
      confirmText = 'Yes, Proceed',
      cancelText = 'Cancel',
      danger = false,
      onConfirm
    }) {
      this.open({
        title,
        contentHtml: `<p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.5;">${message}</p>`,
        size: 'sm',
        confirmText,
        cancelText,
        confirmClass: danger ? 'btn-danger' : 'btn-primary',
        allowMinimize: false,
        onConfirm: async () => {
          if (typeof onConfirm === 'function') {
            await onConfirm();
          }
          return true;
        }
      });
    }
  };

  // Re-render minimized dock when user switches windows/hashes
  window.addEventListener('hashchange', () => {
    Modal.renderMinimizedDock();
  });

  window.Modal = Modal;

})(window);
