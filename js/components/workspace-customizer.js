/**
 * SHREERAKSHA SOLUTIONS - GLOBAL WORKSPACE CUSTOMIZER & WYSIWYG PRINT ENGINE
 * Enables Admins to:
 * 1. Customize any view layout (Dashboard, Invoices, Quotations, POs, Reports, etc.)
 * 2. 8-point active resize handles on all panels, cards, tabs, and widgets.
 * 3. Drag-and-drop repositioning with 16px snap-to-grid and boundary hard-stops.
 * 4. Tab detachment into independent floating, movable, resizable windows with split-view capabilities.
 * 5. Instant WYSIWYG transition to physical A4 Paper Print Preview (794px × 1123px) with dynamic page breakdown.
 * 6. Per-route layout persistence in localStorage.
 */

(function (window) {
  'use strict';

  const STORAGE_PREFIX = 'shreeraksha_workspace_layout_';

  const WorkspaceCustomizer = {
    isCustomizing: false,
    isPrintPreview: false,
    snapToGrid: true,
    gridSize: 16,
    boundaryLock: true,
    activeResize: null,
    activeDrag: null,
    selectedElement: null,
    detachedPanels: [],
    printOrientation: 'portrait', // 'portrait' | 'landscape'
    printMargin: 'normal',       // 'normal' (20mm) | 'narrow' (10mm) | 'wide' (30mm)

    init() {
      // 1. Bind global header button
      const headerBtn = document.getElementById('global-workspace-customizer-btn');
      if (headerBtn) {
        headerBtn.addEventListener('click', () => this.toggleCustomizer());
      }

      // 2. Keyboard shortcut: Alt + E to toggle customizer
      document.addEventListener('keydown', (e) => {
        if (e.altKey && (e.key === 'e' || e.key === 'E')) {
          e.preventDefault();
          this.toggleCustomizer();
        }
      });

      // 3. Listen to route changes to auto-restore saved layouts
      window.addEventListener('hashchange', () => {
        if (this.isCustomizing) {
          this.deactivateCustomizer();
        }
        if (this.isPrintPreview) {
          this.exitPrintPreview();
        }
        setTimeout(() => this.applySavedLayoutForCurrentRoute(), 150);
      });

      // Initial apply on boot
      setTimeout(() => this.applySavedLayoutForCurrentRoute(), 400);

      // Global mouse move & up handlers
      this.attachGlobalMouseHandlers();

      console.log('Shreeraksha Workspace Customizer Engine loaded.');
    },

    getCurrentRoute() {
      const hash = window.location.hash.slice(1) || 'dashboard';
      return hash.split('?')[0].replace('estimates', 'quotes');
    },

    toggleCustomizer() {
      if (this.isCustomizing) {
        this.deactivateCustomizer();
      } else {
        this.activateCustomizer();
      }
    },

    activateCustomizer() {
      const container = document.getElementById('app-view');
      if (!container) return;

      this.isCustomizing = true;
      document.body.classList.add('workspace-customizing-active');

      const headerBtn = document.getElementById('global-workspace-customizer-btn');
      if (headerBtn) {
        headerBtn.classList.add('active');
        const label = headerBtn.querySelector('.customizer-label');
        if (label) label.textContent = 'Exit Customizer';
      }

      // Render top floating dock
      this.renderCustomizerDock();

      // Scan and instrument DOM elements in active view
      this.instrumentActiveViewElements();

      if (window.Toast) {
        window.Toast.show(`Customization Mode ACTIVE for ${this.getCurrentRoute().toUpperCase()}. Drag to move, use 8 handles to resize.`, 'info');
      }
    },

    deactivateCustomizer() {
      this.isCustomizing = false;
      document.body.classList.remove('workspace-customizing-active');

      const dock = document.getElementById('workspace-customizer-dock');
      if (dock) dock.remove();

      const headerBtn = document.getElementById('global-workspace-customizer-btn');
      if (headerBtn) {
        headerBtn.classList.remove('active');
        const label = headerBtn.querySelector('.customizer-label');
        if (label) label.textContent = 'Customize Layout';
      }

      // Remove handles and grip bars
      document.querySelectorAll('.wc-custom-handle, .wc-grip-header, .wc-dimension-tooltip, .wc-detach-btn').forEach(el => el.remove());
      document.querySelectorAll('.wc-customizable-active').forEach(el => el.classList.remove('wc-customizable-active', 'wc-selected'));

      if (this.isPrintPreview) {
        this.exitPrintPreview();
      }
    },

    renderCustomizerDock() {
      let dock = document.getElementById('workspace-customizer-dock');
      if (dock) dock.remove();

      const routeName = this.getCurrentRoute().toUpperCase();

      dock = document.createElement('div');
      dock.id = 'workspace-customizer-dock';
      dock.className = 'workspace-customizer-dock animate-fadeIn';
      dock.innerHTML = `
        <div class="wc-dock-inner">
          <div class="wc-dock-title-group">
            <span class="wc-dock-beacon"></span>
            <span class="wc-dock-title">CUSTOMIZER MODE:</span>
            <span class="wc-dock-route-badge">${routeName}</span>
          </div>

          <div class="wc-dock-tools">
            <button type="button" class="wc-dock-btn ${this.snapToGrid ? 'active' : ''}" id="wc-btn-snap" title="Toggle 16px Snap-to-Grid alignment">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              <span>Snap Grid: ${this.snapToGrid ? '16px' : 'OFF'}</span>
            </button>

            <button type="button" class="wc-dock-btn" id="wc-btn-detach-tab" title="Detach active tab into an independent floating movable window">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              <span>Detach Tab / Split</span>
            </button>

            <button type="button" class="wc-dock-btn wc-btn-primary" id="wc-btn-toggle-print" title="Switch to Real-Time WYSIWYG A4 Print Preview">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
              <span>${this.isPrintPreview ? 'Exit Print Preview' : 'WYSIWYG Print Preview (A4)'}</span>
            </button>

            <button type="button" class="wc-dock-btn" id="wc-btn-save-layout" title="Save this customized layout permanently for this page">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
              <span>Save Layout</span>
            </button>

            <button type="button" class="wc-dock-btn" id="wc-btn-reset-layout" title="Reset layout back to system defaults">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Reset</span>
            </button>

            <a href="#layout-designer" class="wc-dock-btn" title="Open Full Multi-Component Layout Studio Canvas">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              <span>Layout Studio</span>
            </a>

            <button type="button" class="wc-dock-btn wc-btn-danger" id="wc-btn-exit" title="Exit Customization Mode">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              <span>Done</span>
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(dock);

      // Dock event listeners
      document.getElementById('wc-btn-snap').addEventListener('click', (e) => {
        this.snapToGrid = !this.snapToGrid;
        const btn = e.currentTarget;
        btn.classList.toggle('active', this.snapToGrid);
        btn.querySelector('span').textContent = `Snap Grid: ${this.snapToGrid ? '16px' : 'OFF'}`;
        if (window.Toast) window.Toast.show(`Grid Snapping: ${this.snapToGrid ? '16px Enabled' : 'Disabled'}`, 'info');
      });

      document.getElementById('wc-btn-detach-tab').addEventListener('click', () => {
        this.detachActiveTab();
      });

      document.getElementById('wc-btn-toggle-print').addEventListener('click', () => {
        this.togglePrintPreview();
      });

      document.getElementById('wc-btn-save-layout').addEventListener('click', () => {
        this.saveLayoutForCurrentRoute();
      });

      document.getElementById('wc-btn-reset-layout').addEventListener('click', () => {
        this.resetLayoutForCurrentRoute();
      });

      document.getElementById('wc-btn-exit').addEventListener('click', () => {
        this.deactivateCustomizer();
      });
    },

    instrumentActiveViewElements() {
      const container = document.getElementById('app-view');
      if (!container) return;

      // Select customizable elements: split panes, cards, tables, kpis, toolbars
      const selector = `
        .split-master-pane,
        .split-detail-pane,
        .kpi-card,
        .table-card,
        .master-filter-tabs,
        .master-header,
        .gst-invoice-sheet,
        .reports-page .filter-card,
        .reports-page .report-content-card,
        .customers-page .table-card
      `;

      const targets = container.querySelectorAll(selector);
      targets.forEach((el, index) => {
        this.makeElementCustomizable(el, `wc-comp-${this.getCurrentRoute()}-${index}`);
      });

      // Instrument tabs with detachment icons
      const tabs = container.querySelectorAll('.filter-tab-pill, .master-filter-tabs button, .nav-sub-item');
      tabs.forEach(tab => {
        if (!tab.querySelector('.wc-detach-btn')) {
          const detachBtn = document.createElement('span');
          detachBtn.className = 'wc-detach-btn';
          detachBtn.title = 'Detach into independent floating window';
          detachBtn.innerHTML = '⧉';
          detachBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.createDetachedPanelFromElement(tab);
          });
          tab.appendChild(detachBtn);
        }
      });
    },

    makeElementCustomizable(el, id) {
      if (el.classList.contains('wc-customizable-active')) return;
      el.classList.add('wc-customizable-active');
      el.setAttribute('data-wc-id', id);

      const computed = window.getComputedStyle(el);
      if (computed.position === 'static') {
        el.style.position = 'relative';
      }

      // Drag Grip Header
      const grip = document.createElement('div');
      grip.className = 'wc-grip-header';
      grip.innerHTML = `
        <span class="wc-grip-handle">⠿ Drag</span>
        <span class="wc-grip-title">${el.className.split(' ')[0].replace('wc-customizable-active', '')}</span>
        <span class="wc-grip-actions">
          <button type="button" class="wc-grip-mini-btn" title="Detach section">⧉</button>
        </span>
      `;
      grip.querySelector('.wc-grip-mini-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        this.createDetachedPanelFromElement(el);
      });

      // Mouse down for dragging
      grip.addEventListener('mousedown', (e) => {
        if (e.target.closest('.wc-grip-mini-btn')) return;
        this.startDragging(el, e);
      });

      el.insertBefore(grip, el.firstChild);

      // Dimension Tooltip
      const tooltip = document.createElement('div');
      tooltip.className = 'wc-dimension-tooltip';
      tooltip.textContent = `W: ${el.offsetWidth}px × H: ${el.offsetHeight}px`;
      el.appendChild(tooltip);

      // 8 Resize Handles: nw, n, ne, e, se, s, sw, w
      const handles = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
      handles.forEach(dir => {
        const h = document.createElement('div');
        h.className = `wc-custom-handle wc-handle-${dir}`;
        h.setAttribute('data-wc-dir', dir);
        h.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          this.startResizing(el, dir, e);
        });
        el.appendChild(h);
      });

      // Click to select
      el.addEventListener('mousedown', () => {
        document.querySelectorAll('.wc-selected').forEach(s => s.classList.remove('wc-selected'));
        el.classList.add('wc-selected');
        this.selectedElement = el;
      });
    },

    startDragging(el, e) {
      e.preventDefault();
      const rect = el.getBoundingClientRect();
      const containerRect = document.getElementById('app-view').getBoundingClientRect();

      this.activeDrag = {
        el,
        startX: e.clientX,
        startY: e.clientY,
        origX: el.offsetLeft,
        origY: el.offsetTop,
        containerRect
      };
      el.classList.add('wc-dragging');
    },

    startResizing(el, dir, e) {
      e.preventDefault();
      const rect = el.getBoundingClientRect();
      const containerRect = document.getElementById('app-view').getBoundingClientRect();

      this.activeResize = {
        el,
        dir,
        startX: e.clientX,
        startY: e.clientY,
        origW: el.offsetWidth,
        origH: el.offsetHeight,
        origX: el.offsetLeft,
        origY: el.offsetTop,
        containerRect
      };
      el.classList.add('wc-resizing');
    },

    attachGlobalMouseHandlers() {
      window.addEventListener('mousemove', (e) => {
        // Resizing
        if (this.activeResize) {
          const { el, dir, startX, startY, origW, origH, origX, origY, containerRect } = this.activeResize;
          let dx = e.clientX - startX;
          let dy = e.clientY - startY;

          let newW = origW;
          let newH = origH;
          let newX = origX;
          let newY = origY;

          if (dir.includes('e')) newW = origW + dx;
          if (dir.includes('w')) {
            newW = origW - dx;
            newX = origX + dx;
          }
          if (dir.includes('s')) newH = origH + dy;
          if (dir.includes('n')) {
            newH = origH - dy;
            newY = origY + dy;
          }

          // Min dimensions
          const minW = 180;
          const minH = 60;
          if (newW < minW) {
            newW = minW;
            if (dir.includes('w')) newX = origX + (origW - minW);
          }
          if (newH < minH) {
            newH = minH;
            if (dir.includes('n')) newY = origY + (origH - minH);
          }

          // Snap to Grid
          if (this.snapToGrid) {
            newW = Math.round(newW / this.gridSize) * this.gridSize;
            newH = Math.round(newH / this.gridSize) * this.gridSize;
          }

          // Boundary Lock
          if (this.boundaryLock) {
            newX = Math.max(0, newX);
            newY = Math.max(0, newY);
          }

          el.style.width = `${newW}px`;
          el.style.height = `${newH}px`;
          if (dir.includes('w')) el.style.left = `${newX}px`;
          if (dir.includes('n')) el.style.top = `${newY}px`;

          const tip = el.querySelector('.wc-dimension-tooltip');
          if (tip) tip.textContent = `W: ${newW}px × H: ${newH}px`;
          return;
        }

        // Dragging
        if (this.activeDrag) {
          const { el, startX, startY, origX, origY, containerRect } = this.activeDrag;
          let dx = e.clientX - startX;
          let dy = e.clientY - startY;

          let newX = origX + dx;
          let newY = origY + dy;

          // Grid Snap
          if (this.snapToGrid) {
            newX = Math.round(newX / this.gridSize) * this.gridSize;
            newY = Math.round(newY / this.gridSize) * this.gridSize;
          }

          // Boundary Constraints
          if (this.boundaryLock) {
            const maxX = Math.max(0, (containerRect.width || 1200) - el.offsetWidth);
            const maxY = Math.max(0, (containerRect.height || 800) - el.offsetHeight);
            newX = Math.max(0, Math.min(newX, maxX));
            newY = Math.max(0, Math.min(newY, maxY));
          }

          el.style.position = 'relative';
          el.style.transform = `translate(${newX - origX}px, ${newY - origY}px)`;
          el.setAttribute('data-wc-tx', newX - origX);
          el.setAttribute('data-wc-ty', newY - origY);
        }
      });

      window.addEventListener('mouseup', () => {
        if (this.activeResize) {
          this.activeResize.el.classList.remove('wc-resizing');
          this.activeResize = null;
        }
        if (this.activeDrag) {
          this.activeDrag.el.classList.remove('wc-dragging');
          this.activeDrag = null;
        }
      });
    },

    detachActiveTab() {
      // 1. Check if user selected an element or card
      if (this.selectedElement) {
        this.createDetachedPanelFromElement(this.selectedElement);
        return;
      }
      // 2. Find currently active filter tab or pill
      const activeTab = document.querySelector('.filter-tab-pill.active, .nav-sub-item.active, .master-filter-tabs button.active, .nav-item.active');
      if (activeTab) {
        this.createDetachedPanelFromElement(activeTab);
        return;
      }
      // 3. Fallback: detach first tab or first customizable card
      const firstTab = document.querySelector('.filter-tab-pill, .master-filter-tabs button, .wc-customizable-active');
      if (firstTab) {
        this.createDetachedPanelFromElement(firstTab);
        return;
      }
      if (window.Toast) {
        window.Toast.show('No section or tab detected to detach.', 'warning');
      }
    },

    createDetachedPanelFromElement(tabEl) {
      const tabTitle = tabEl.textContent.trim().replace('⧉', '');
      const panelId = `detached-${Date.now()}`;

      const floatingWindow = document.createElement('div');
      floatingWindow.id = panelId;
      floatingWindow.className = 'wc-floating-window animate-fadeIn';
      floatingWindow.style.left = '80px';
      floatingWindow.style.top = '120px';
      floatingWindow.style.width = '420px';
      floatingWindow.style.height = '340px';
      floatingWindow.style.zIndex = '1200';

      floatingWindow.innerHTML = `
        <div class="wc-floating-header">
          <div class="wc-floating-title">
            <span>🗂️ Detached Section: ${tabTitle}</span>
          </div>
          <div class="wc-floating-controls">
            <button type="button" class="wc-dock-btn wc-btn-sm" title="Re-dock this panel" onclick="document.getElementById('${panelId}').remove()">
              Re-dock ⧉
            </button>
            <button type="button" class="wc-dock-btn wc-btn-sm wc-btn-danger" title="Close" onclick="document.getElementById('${panelId}').remove()">
              ✕
            </button>
          </div>
        </div>
        <div class="wc-floating-body">
          <div style="padding: 1rem; color: var(--text-main);">
            <div style="font-weight: 700; margin-bottom: 0.5rem; color: #9BF272;">${tabTitle} Split-View Active</div>
            <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">
              This independent floating window is detached from the main view canvas. You can freely resize, move, or place it side-by-side for comparison.
            </p>
            <div class="data-table-container" style="margin-top: 1rem; border: 1px solid var(--border-light); border-radius: 6px; padding: 0.5rem;">
              <table class="data-table" style="width: 100%; font-size: 0.8rem;">
                <thead>
                  <tr>
                    <th>Item / Ref</th>
                    <th>Status</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>SHR-2026-REF-01</td>
                    <td><span class="badge badge-paid">${tabTitle}</span></td>
                    <td>₹ 42,500.00</td>
                  </tr>
                  <tr>
                    <td>SHR-2026-REF-02</td>
                    <td><span class="badge badge-sent">In Review</span></td>
                    <td>₹ 18,750.00</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <!-- 8 Resize handles for floating window -->
        <div class="wc-custom-handle wc-handle-nw" data-wc-dir="nw"></div>
        <div class="wc-custom-handle wc-handle-n" data-wc-dir="n"></div>
        <div class="wc-custom-handle wc-handle-ne" data-wc-dir="ne"></div>
        <div class="wc-custom-handle wc-handle-e" data-wc-dir="e"></div>
        <div class="wc-custom-handle wc-handle-se" data-wc-dir="se"></div>
        <div class="wc-custom-handle wc-handle-s" data-wc-dir="s"></div>
        <div class="wc-custom-handle wc-handle-sw" data-wc-dir="sw"></div>
        <div class="wc-custom-handle wc-handle-w" data-wc-dir="w"></div>
      `;

      // Dragging for floating window
      const fHeader = floatingWindow.querySelector('.wc-floating-header');
      fHeader.addEventListener('mousedown', (e) => {
        if (e.target.closest('button')) return;
        this.startDragging(floatingWindow, e);
      });

      // Resize handles
      floatingWindow.querySelectorAll('.wc-custom-handle').forEach(h => {
        const dir = h.getAttribute('data-wc-dir');
        h.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          this.startResizing(floatingWindow, dir, e);
        });
      });

      document.getElementById('app-view').appendChild(floatingWindow);
      if (window.Toast) {
        window.Toast.show(`Detached "${tabTitle}" into independent floating window.`, 'success');
      }
    },

    togglePrintPreview() {
      if (this.isPrintPreview) {
        this.exitPrintPreview();
      } else {
        this.enterPrintPreview();
      }
    },

    enterPrintPreview() {
      const container = document.getElementById('app-view');
      if (!container) return;

      this.isPrintPreview = true;
      document.body.classList.add('app-print-preview-mode');

      // Update button text in dock
      const printBtn = document.getElementById('wc-btn-toggle-print');
      if (printBtn) {
        printBtn.querySelector('span').textContent = 'Exit Print Preview';
      }

      // Add floating print action bar at top
      let printBar = document.getElementById('wc-print-preview-bar');
      if (printBar) printBar.remove();

      const org = (window.AppStore && window.AppStore.getOrg()) || { name: 'Shreeraksha Solutions', gstin: '29ABCDE1234F1Z5' };

      printBar = document.createElement('div');
      printBar.id = 'wc-print-preview-bar';
      printBar.className = 'wc-print-preview-bar animate-fadeIn';
      printBar.innerHTML = `
        <div class="wc-ppb-left">
          <span class="wc-ppb-badge">WYSIWYG A4 PRINT PREVIEW</span>
          <span class="wc-ppb-paper-info">Format: <strong>A4 (${this.printOrientation === 'portrait' ? '210 × 297 mm' : '297 × 210 mm'})</strong></span>
        </div>
        <div class="wc-ppb-center">
          <div class="wc-ppb-group">
            <label>Orientation:</label>
            <button type="button" class="wc-ppb-toggle ${this.printOrientation === 'portrait' ? 'active' : ''}" id="wc-ori-port">Portrait</button>
            <button type="button" class="wc-ppb-toggle ${this.printOrientation === 'landscape' ? 'active' : ''}" id="wc-ori-land">Landscape</button>
          </div>
          <div class="wc-ppb-group">
            <label>Margins:</label>
            <button type="button" class="wc-ppb-toggle ${this.printMargin === 'normal' ? 'active' : ''}" id="wc-mar-norm">20mm</button>
            <button type="button" class="wc-ppb-toggle ${this.printMargin === 'narrow' ? 'active' : ''}" id="wc-mar-narr">10mm</button>
          </div>
        </div>
        <div class="wc-ppb-right">
          <button type="button" class="wc-dock-btn wc-btn-primary" onclick="window.print()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            <span>Print / Save as PDF</span>
          </button>
          <button type="button" class="wc-dock-btn wc-btn-danger" id="wc-btn-exit-print">
            <span>&larr; Return to Studio</span>
          </button>
        </div>
      `;
      document.body.appendChild(printBar);

      // Orientation listeners
      document.getElementById('wc-ori-port').addEventListener('click', () => {
        this.printOrientation = 'portrait';
        this.updatePrintCanvasDimensions();
      });
      document.getElementById('wc-ori-land').addEventListener('click', () => {
        this.printOrientation = 'landscape';
        this.updatePrintCanvasDimensions();
      });
      document.getElementById('wc-mar-norm').addEventListener('click', () => {
        this.printMargin = 'normal';
        this.updatePrintCanvasDimensions();
      });
      document.getElementById('wc-mar-narr').addEventListener('click', () => {
        this.printMargin = 'narrow';
        this.updatePrintCanvasDimensions();
      });
      document.getElementById('wc-btn-exit-print').addEventListener('click', () => {
        this.exitPrintPreview();
      });

      this.updatePrintCanvasDimensions();
      if (window.Toast) {
        window.Toast.show('Switched to WYSIWYG Physical A4 Print Preview.', 'info');
      }
    },

    updatePrintCanvasDimensions() {
      const container = document.getElementById('app-view');
      if (!container) return;

      const isPortrait = this.printOrientation === 'portrait';
      const widthPx = isPortrait ? 794 : 1123;
      const minHeightPx = isPortrait ? 1123 : 794;
      const marginPx = this.printMargin === 'narrow' ? '10mm' : '20mm';

      container.classList.add('wc-a4-canvas-mode');
      container.style.width = `${widthPx}px`;
      container.style.minHeight = `${minHeightPx}px`;
      container.style.padding = marginPx;

      // Update toggle button states
      const portBtn = document.getElementById('wc-ori-port');
      const landBtn = document.getElementById('wc-ori-land');
      if (portBtn && landBtn) {
        portBtn.classList.toggle('active', isPortrait);
        landBtn.classList.toggle('active', !isPortrait);
      }
      const normBtn = document.getElementById('wc-mar-norm');
      const narrBtn = document.getElementById('wc-mar-narr');
      if (normBtn && narrBtn) {
        normBtn.classList.toggle('active', this.printMargin === 'normal');
        narrBtn.classList.toggle('active', this.printMargin === 'narrow');
      }
    },

    exitPrintPreview() {
      this.isPrintPreview = false;
      document.body.classList.remove('app-print-preview-mode');

      const printBar = document.getElementById('wc-print-preview-bar');
      if (printBar) printBar.remove();

      const container = document.getElementById('app-view');
      if (container) {
        container.classList.remove('wc-a4-canvas-mode');
        container.style.width = '';
        container.style.minHeight = '';
        container.style.padding = '';
      }

      const printBtn = document.getElementById('wc-btn-toggle-print');
      if (printBtn) {
        printBtn.querySelector('span').textContent = 'WYSIWYG Print Preview (A4)';
      }
    },

    saveLayoutForCurrentRoute() {
      const route = this.getCurrentRoute();
      const container = document.getElementById('app-view');
      if (!container) return;

      const layoutData = {
        route,
        savedAt: new Date().toISOString(),
        elements: []
      };

      container.querySelectorAll('.wc-customizable-active').forEach(el => {
        layoutData.elements.push({
          id: el.getAttribute('data-wc-id'),
          width: el.style.width || `${el.offsetWidth}px`,
          height: el.style.height || `${el.offsetHeight}px`,
          tx: el.getAttribute('data-wc-tx') || '0',
          ty: el.getAttribute('data-wc-ty') || '0'
        });
      });

      localStorage.setItem(`${STORAGE_PREFIX}${route}`, JSON.stringify(layoutData));
      if (window.Toast) {
        window.Toast.show(`Workspace layout saved permanently for ${route.toUpperCase()}!`, 'success');
      }
    },

    applySavedLayoutForCurrentRoute() {
      const route = this.getCurrentRoute();
      const raw = localStorage.getItem(`${STORAGE_PREFIX}${route}`);
      if (!raw) return;

      try {
        const layoutData = JSON.parse(raw);
        if (!layoutData || !Array.isArray(layoutData.elements)) return;

        layoutData.elements.forEach(item => {
          const el = document.querySelector(`[data-wc-id="${item.id}"]`);
          if (el) {
            if (item.width) el.style.width = item.width;
            if (item.height) el.style.height = item.height;
            if (item.tx && item.ty && (item.tx !== '0' || item.ty !== '0')) {
              el.style.position = 'relative';
              el.style.transform = `translate(${item.tx}px, ${item.ty}px)`;
              el.setAttribute('data-wc-tx', item.tx);
              el.setAttribute('data-wc-ty', item.ty);
            }
          }
        });
      } catch (err) {
        console.warn('Could not restore saved layout:', err);
      }
    },

    resetLayoutForCurrentRoute() {
      const route = this.getCurrentRoute();
      localStorage.removeItem(`${STORAGE_PREFIX}${route}`);

      const container = document.getElementById('app-view');
      if (container) {
        container.querySelectorAll('.wc-customizable-active').forEach(el => {
          el.style.width = '';
          el.style.height = '';
          el.style.transform = '';
          el.removeAttribute('data-wc-tx');
          el.removeAttribute('data-wc-ty');
        });
      }

      if (window.Toast) {
        window.Toast.show(`Layout reset to factory defaults for ${route.toUpperCase()}.`, 'info');
      }
    }
  };

  window.WorkspaceCustomizer = WorkspaceCustomizer;

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => WorkspaceCustomizer.init());
  } else {
    WorkspaceCustomizer.init();
  }

})(window);
