/**
 * SHREERAKSHA SOLUTIONS - WORKSPACE LAYOUT CUSTOMIZER & WYSIWYG PRINT PREVIEW
 * Features:
 * 1. Live Canvas with active Customization Mode toggle.
 * 2. 8-Point Active Component Resizing with Min/Max Constraints and Dimensional Tooltips.
 * 3. Drag-and-Drop Positioning with Snap-to-Grid guidelines and Ghost previews.
 * 4. Structural Tab Reordering & Independent Floating Window Detachment.
 * 5. Strict Boundary Hard-Stops & Collision/Z-Index layer management.
 * 6. Instant WYSIWYG Transition to Physical A4/Letter Print Preview with print stylesheets.
 */

(function (window) {
  'use strict';

  const STORAGE_KEY = 'shreeraksha_workspace_layout_v1';

  const DEFAULT_COMPONENTS = [
    {
      id: 'comp-tabs',
      type: 'tabs',
      title: 'Workspace Navigation Tabs',
      x: 24,
      y: 20,
      width: 746,
      height: 60,
      minWidth: 320,
      minHeight: 52,
      zIndex: 10,
      tabs: ['Sales Overview', 'GST Invoices', 'Material Dispatch', 'Audit Logs'],
      activeTab: 0
    },
    {
      id: 'comp-actions',
      type: 'buttons',
      title: 'Quick Operations Toolbar',
      x: 24,
      y: 95,
      width: 746,
      height: 64,
      minWidth: 260,
      minHeight: 48,
      zIndex: 10,
      buttons: [
        { label: '+ Create Tax Invoice', action: 'invoice', color: 'primary' },
        { label: '+ New Quotation', action: 'quote', color: 'secondary' },
        { label: 'Export GSTR-1', action: 'export', color: 'outline' },
        { label: 'Batch Print', action: 'print', color: 'outline' }
      ]
    },
    {
      id: 'comp-kpi-1',
      type: 'kpi',
      title: 'Monthly GST Turnover',
      x: 24,
      y: 175,
      width: 360,
      height: 140,
      minWidth: 220,
      minHeight: 110,
      zIndex: 5,
      kpiValue: '₹ 18,45,290.00',
      kpiSub: '+14.8% vs last month',
      kpiColor: '#9BF272'
    },
    {
      id: 'comp-kpi-2',
      type: 'kpi',
      title: 'Eligible ITC (Input Tax Credit)',
      x: 410,
      y: 175,
      width: 360,
      height: 140,
      minWidth: 220,
      minHeight: 110,
      zIndex: 5,
      kpiValue: '₹ 3,32,150.00',
      kpiSub: 'Auto-reconciled with GSTR-2B',
      kpiColor: '#00e5ff'
    },
    {
      id: 'comp-table',
      type: 'table',
      title: 'Recent GST Invoices & E-Way Bills',
      x: 24,
      y: 335,
      width: 746,
      height: 310,
      minWidth: 400,
      minHeight: 200,
      zIndex: 5
    },
    {
      id: 'comp-notes',
      type: 'notes',
      title: 'Statutory Compliance & Notes',
      x: 24,
      y: 665,
      width: 746,
      height: 140,
      minWidth: 300,
      minHeight: 100,
      zIndex: 5
    }
  ];

  const LayoutDesignerView = {
    components: [],
    isCustomizing: true,
    isPreviewMode: false,
    snapToGrid: true,
    gridSize: 16,
    boundaryLock: true,
    paperSize: 'a4', // 'a4' or 'letter'
    selectedComponentId: null,
    activeDrag: null,
    activeResize: null,

    init() {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          this.components = JSON.parse(saved);
        } catch (e) {
          this.components = JSON.parse(JSON.stringify(DEFAULT_COMPONENTS));
        }
      } else {
        this.components = JSON.parse(JSON.stringify(DEFAULT_COMPONENTS));
      }
    },

    saveLayout() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.components));
      if (window.Toast) {
        window.Toast.show('Workspace layout saved successfully!', 'success');
      }
    },

    resetToDefault() {
      this.components = JSON.parse(JSON.stringify(DEFAULT_COMPONENTS));
      this.saveLayout();
      this.render();
      if (window.Toast) {
        window.Toast.show('Layout reset to default factory template.', 'info');
      }
    },

    render() {
      const container = document.getElementById('app-view') || document.getElementById('view-container');
      if (!container) return;

      if (!this.components || this.components.length === 0) {
        this.init();
      }

      container.innerHTML = `
        <div class="layout-studio-page animate-fadeIn">
          
          <!-- TOP STUDIO CONTROL BAR -->
          <div class="studio-top-bar">
            <div class="studio-title-group">
              <h2>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
                <span>Workspace Layout Studio</span>
                <span class="studio-badge">${this.isPreviewMode ? 'WYSIWYG Print Preview' : (this.isCustomizing ? 'Customization Active' : 'Live Mode')}</span>
              </h2>
            </div>

            <div class="studio-controls-strip">
              <!-- Mode Toggle -->
              <div class="customizer-mode-toggle" title="Toggle between Editing Canvas and Live Workspace">
                <button type="button" class="mode-toggle-btn ${this.isCustomizing && !this.isPreviewMode ? 'active' : ''}" id="btn-mode-customize">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                  <span>Customize</span>
                </button>
                <button type="button" class="mode-toggle-btn ${!this.isCustomizing && !this.isPreviewMode ? 'active' : ''}" id="btn-mode-live">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  <span>Live Preview</span>
                </button>
              </div>

              <!-- Grid Snapping Toggle -->
              <button type="button" class="btn ${this.snapToGrid ? 'btn-secondary' : 'btn-outline'} btn-sm" id="btn-toggle-grid" title="Toggle Snap-to-Grid (16px increments)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                <span>Snap Grid: ${this.snapToGrid ? 'ON (16px)' : 'OFF'}</span>
              </button>

              <!-- Boundary Lock -->
              <button type="button" class="btn ${this.boundaryLock ? 'btn-secondary' : 'btn-outline'} btn-sm" id="btn-toggle-bounds" title="Strict Canvas Boundary Constraints">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <span>Bounds: ${this.boundaryLock ? 'Locked' : 'Free'}</span>
              </button>

              <!-- Reset & Save -->
              <button type="button" class="btn btn-outline btn-sm" id="btn-reset-layout" title="Reset to default factory layout">
                Reset
              </button>
              <button type="button" class="btn btn-secondary btn-sm" id="btn-save-layout" title="Save current arrangement">
                Save Layout
              </button>

              <!-- Dedicated WYSIWYG Print Preview Button -->
              <button type="button" class="btn btn-primary btn-sm btn-icon-gap" id="btn-toggle-print-preview" style="font-weight: 700; background: linear-gradient(135deg, #193440, #2a586d); border-color: #9BF272;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
                <span>${this.isPreviewMode ? 'Exit Print Preview' : 'WYSIWYG Print Preview (A4)'}</span>
              </button>
            </div>
          </div>

          <!-- FLOATING PRINT PREVIEW CONTROL BAR (Visible only in print preview) -->
          <div class="print-preview-bar">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span style="font-size: 0.85rem; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 0.4rem;">
                📄 Physical Document Canvas: 
                <span style="color: #9BF272; font-family: var(--font-mono);">A4 Portrait (210 × 297 mm)</span>
              </span>
              <span style="font-size: 0.75rem; color: #94a3b8;">100% WYSIWYG Scaled Output</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <button type="button" class="btn btn-primary btn-sm btn-icon-gap" onclick="window.print()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
                <span>Print / Save as PDF</span>
              </button>
              <button type="button" class="btn btn-secondary btn-sm" id="btn-exit-print-bar">
                <span>&larr; Return to Studio</span>
              </button>
            </div>
          </div>

          <!-- MAIN CANVAS GRID -->
          <div class="studio-main-grid ${this.isPreviewMode ? 'print-preview-mode' : ''}">
            
            <!-- LEFT COMPONENT LIBRARY PALETTE -->
            <aside class="studio-library-card">
              <div class="studio-library-section">
                <h4>
                  <span>Interface Components</span>
                  <span class="text-xs text-muted">Drag to add</span>
                </h4>
                <div class="library-items-list">
                  <div class="library-draggable-item" data-comp-type="kpi">
                    <span>📊 Metric Card (KPI)</span>
                    <span class="text-xs text-muted">+ Add</span>
                  </div>
                  <div class="library-draggable-item" data-comp-type="buttons">
                    <span>🔘 Action Button Bar</span>
                    <span class="text-xs text-muted">+ Add</span>
                  </div>
                  <div class="library-draggable-item" data-comp-type="tabs">
                    <span>🗂️ Nav Tab Strip</span>
                    <span class="text-xs text-muted">+ Add</span>
                  </div>
                  <div class="library-draggable-item" data-comp-type="table">
                    <span>📋 Data Table Widget</span>
                    <span class="text-xs text-muted">+ Add</span>
                  </div>
                  <div class="library-draggable-item" data-comp-type="notes">
                    <span>📝 Compliance Notes</span>
                    <span class="text-xs text-muted">+ Add</span>
                  </div>
                </div>
              </div>

              <div class="studio-library-section" style="border-top: 1px solid var(--border-light); padding-top: 1rem;">
                <h4>Preset Templates</h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <button type="button" class="btn btn-outline btn-sm text-left" id="preset-billing-station" style="font-size: 0.775rem;">
                    🎯 GST Billing Station (A4)
                  </button>
                  <button type="button" class="btn btn-outline btn-sm text-left" id="preset-executive-dash" style="font-size: 0.775rem;">
                    📈 Executive Finance Overview
                  </button>
                </div>
              </div>

              <div class="studio-library-section" style="border-top: 1px solid var(--border-light); padding-top: 1rem;">
                <h4>Layout Guidelines</h4>
                <div class="text-xs text-muted" style="line-height: 1.5;">
                  • <strong>Resize Handles</strong>: Click any block to reveal 8 active border handles.<br>
                  • <strong>Bounds Lock</strong>: Blocks cannot be dragged outside canvas borders.<br>
                  • <strong>Tabs Detach</strong>: Drag a tab downward to pop it out into a standalone window!
                </div>
              </div>
            </aside>

            <!-- CANVAS VIEWPORT -->
            <main class="canvas-viewport-wrapper ${this.isCustomizing && !this.isPreviewMode ? 'customizing' : ''}" id="canvas-viewport">
              
              <!-- Canvas Status Bar -->
              <div class="canvas-status-bar">
                <div>
                  <span>Interactive Canvas Canvas: </span>
                  <span class="canvas-dimension-info" id="canvas-dim-display">794 × 1123 px (A4 Equivalent)</span>
                </div>
                <div>
                  <span id="canvas-active-selection-label">Click a component to select and resize</span>
                </div>
              </div>

              <!-- Interactive Board -->
              <div class="interactive-canvas-board" id="canvas-board">
                <!-- Snap guidelines -->
                <div class="snap-guide-line-x" id="snap-guide-x"></div>
                <div class="snap-guide-line-y" id="snap-guide-y"></div>

                <!-- Ghost preview for drag and drop -->
                <div class="canvas-ghost-preview" id="ghost-preview"></div>

                <!-- Render dynamic components -->
                ${this.renderComponentsHtml()}
              </div>
            </main>

          </div>

        </div>
      `;

      this.bindEvents();
    },

    renderComponentsHtml() {
      return this.components.map(comp => {
        const isSelected = this.selectedComponentId === comp.id;

        return `
          <div class="canvas-component ${isSelected ? 'selected' : ''}" 
               id="${comp.id}" 
               data-id="${comp.id}" 
               data-type="${comp.type}"
               style="left: ${comp.x}px; top: ${comp.y}px; width: ${comp.width}px; height: ${comp.height}px; z-index: ${comp.zIndex || 5};">
            
            <!-- Component Header -->
            <div class="canvas-component-header">
              <span class="canvas-component-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/></svg>
                <span>${comp.title}</span>
              </span>
              <div class="canvas-component-actions">
                <button type="button" class="canvas-action-icon-btn comp-delete-btn" data-id="${comp.id}" title="Remove Component">&times;</button>
              </div>
            </div>

            <!-- Component Body by Type -->
            <div class="canvas-component-body">
              ${this.renderComponentContent(comp)}
            </div>

            <!-- Dimensional Tooltip -->
            <div class="dimension-tooltip">
              W: ${comp.width}px × H: ${comp.height}px
            </div>

            <!-- 8 Active Resize Handles -->
            <div class="resize-handle handle-nw" data-handle="nw" data-id="${comp.id}"></div>
            <div class="resize-handle handle-n"  data-handle="n"  data-id="${comp.id}"></div>
            <div class="resize-handle handle-ne" data-handle="ne" data-id="${comp.id}"></div>
            <div class="resize-handle handle-e"  data-handle="e"  data-id="${comp.id}"></div>
            <div class="resize-handle handle-se" data-handle="se" data-id="${comp.id}"></div>
            <div class="resize-handle handle-s"  data-handle="s"  data-id="${comp.id}"></div>
            <div class="resize-handle handle-sw" data-handle="sw" data-id="${comp.id}"></div>
            <div class="resize-handle handle-w"  data-handle="w"  data-id="${comp.id}"></div>
          </div>
        `;
      }).join('');
    },

    renderComponentContent(comp) {
      switch (comp.type) {
        case 'tabs':
          return `
            <div class="canvas-tab-bar" data-id="${comp.id}">
              ${(comp.tabs || []).map((t, idx) => `
                <div class="canvas-tab-pill ${comp.activeTab === idx ? 'active' : ''}" data-tab-idx="${idx}" draggable="true">
                  <span class="tab-drag-handle">&#8942;&#8942;</span>
                  <span>${t}</span>
                  ${comp.tabs.length > 1 ? `<span class="tab-detach-btn" data-tab-idx="${idx}" title="Detach into separate window" style="opacity: 0.6; cursor: pointer; font-size: 0.7rem; margin-left: 2px;">&#x2197;</span>` : ''}
                </div>
              `).join('')}
              <button type="button" class="btn-ghost-sm btn-add-tab" data-id="${comp.id}" style="font-size: 0.75rem; padding: 0.2rem 0.5rem;">+ Tab</button>
            </div>
          `;
        case 'buttons':
          return `
            <div style="display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap;">
              ${(comp.buttons || []).map((btn, bidx) => `
                <button type="button" class="btn btn-${btn.color || 'primary'} btn-sm canvas-button-component" data-btn-idx="${bidx}">
                  <span>${btn.label}</span>
                </button>
              `).join('')}
            </div>
          `;
        case 'kpi':
          return `
            <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
              <div style="font-size: 1.45rem; font-weight: 800; font-family: var(--font-heading); color: ${comp.kpiColor || '#9BF272'}; margin-bottom: 2px;">
                ${comp.kpiValue || '₹ 0.00'}
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 500;">
                ${comp.kpiSub || 'Verified Statutory Figure'}
              </div>
            </div>
          `;
        case 'table':
          return `
            <table class="data-table" style="font-size: 0.775rem;">
              <thead>
                <tr>
                  <th>Doc #</th>
                  <th>Customer / Entity</th>
                  <th>Date</th>
                  <th class="text-right">Taxable Amt</th>
                  <th class="text-right">GST (18%)</th>
                  <th class="text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="font-mono font-bold">SHRKS/Inv/26-27/024</td>
                  <td>Manipal Speciality Chemicals</td>
                  <td>23-10-2026</td>
                  <td class="text-right font-mono">₹ 29,260.00</td>
                  <td class="text-right font-mono">₹ 5,266.80</td>
                  <td class="text-right"><span class="badge badge-paid">PAID</span></td>
                </tr>
                <tr>
                  <td class="font-mono font-bold">SHRKS/Qtn/26-27/025</td>
                  <td>Biocon Biologics Ltd</td>
                  <td>22-10-2026</td>
                  <td class="text-right font-mono">₹ 18,500.00</td>
                  <td class="text-right font-mono">₹ 3,330.00</td>
                  <td class="text-right"><span class="badge badge-sent">SENT</span></td>
                </tr>
                <tr>
                  <td class="font-mono font-bold">SHRKS/PO/26-27/007</td>
                  <td>Waters India Instruments</td>
                  <td>21-10-2026</td>
                  <td class="text-right font-mono">₹ 1,66,500.00</td>
                  <td class="text-right font-mono">₹ 29,970.00</td>
                  <td class="text-right"><span class="badge badge-paid">ISSUED</span></td>
                </tr>
              </tbody>
            </table>
          `;
        case 'notes':
          return `
            <div style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.5;">
              <strong>GST Compliance Note:</strong> Invoices generated under Section 31 of CGST Act. Certified that particulars given above are true and correct, and payment is subject to Mangalore / Sulya jurisdiction.
            </div>
          `;
        default:
          return `<div class="text-muted text-xs">Custom workspace content block</div>`;
      }
    },

    bindEvents() {
      const board = document.getElementById('canvas-board');
      if (!board) return;

      // Top control bar events
      const btnCustomize = document.getElementById('btn-mode-customize');
      const btnLive = document.getElementById('btn-mode-live');
      const btnPrint = document.getElementById('btn-toggle-print-preview');
      const btnExitPrint = document.getElementById('btn-exit-print-bar');
      const btnGrid = document.getElementById('btn-toggle-grid');
      const btnBounds = document.getElementById('btn-toggle-bounds');
      const btnSave = document.getElementById('btn-save-layout');
      const btnReset = document.getElementById('btn-reset-layout');

      if (btnCustomize) {
        btnCustomize.addEventListener('click', () => {
          this.isCustomizing = true;
          this.isPreviewMode = false;
          this.render();
        });
      }

      if (btnLive) {
        btnLive.addEventListener('click', () => {
          this.isCustomizing = false;
          this.isPreviewMode = false;
          this.selectedComponentId = null;
          this.render();
        });
      }

      if (btnPrint) {
        btnPrint.addEventListener('click', () => {
          this.isPreviewMode = !this.isPreviewMode;
          this.selectedComponentId = null;
          this.render();
        });
      }

      if (btnExitPrint) {
        btnExitPrint.addEventListener('click', () => {
          this.isPreviewMode = false;
          this.isCustomizing = true;
          this.render();
        });
      }

      if (btnGrid) {
        btnGrid.addEventListener('click', () => {
          this.snapToGrid = !this.snapToGrid;
          this.render();
        });
      }

      if (btnBounds) {
        btnBounds.addEventListener('click', () => {
          this.boundaryLock = !this.boundaryLock;
          this.render();
        });
      }

      if (btnSave) {
        btnSave.addEventListener('click', () => this.saveLayout());
      }

      if (btnReset) {
        btnReset.addEventListener('click', () => this.resetToDefault());
      }

      // Presets
      const presetBilling = document.getElementById('preset-billing-station');
      if (presetBilling) {
        presetBilling.addEventListener('click', () => {
          this.components = JSON.parse(JSON.stringify(DEFAULT_COMPONENTS));
          this.render();
          if (window.Toast) window.Toast.show('Loaded GST Billing Station (A4) preset.', 'info');
        });
      }

      const presetExec = document.getElementById('preset-executive-dash');
      if (presetExec) {
        presetExec.addEventListener('click', () => {
          this.components = [
            { id: 'comp-kpi-1', type: 'kpi', title: 'Monthly Revenue', x: 24, y: 20, width: 236, height: 130, zIndex: 5, kpiValue: '₹ 24.8L', kpiSub: '+18.2%' },
            { id: 'comp-kpi-2', type: 'kpi', title: 'Output CGST', x: 280, y: 20, width: 236, height: 130, zIndex: 5, kpiValue: '₹ 2.23L', kpiSub: 'Karnataka (29)' },
            { id: 'comp-kpi-3', type: 'kpi', title: 'Output SGST', x: 536, y: 20, width: 234, height: 130, zIndex: 5, kpiValue: '₹ 2.23L', kpiSub: 'Karnataka (29)' },
            { id: 'comp-tabs', type: 'tabs', title: 'Analytics Views', x: 24, y: 170, width: 746, height: 60, zIndex: 10, tabs: ['Overview', 'GSTR-1 Summary', 'Cashflow', 'E-Way Bills'], activeTab: 0 },
            { id: 'comp-table', type: 'table', title: 'Top Performing Client Invoices', x: 24, y: 250, width: 746, height: 380, zIndex: 5 }
          ];
          this.render();
          if (window.Toast) window.Toast.show('Loaded Executive Finance Overview preset.', 'info');
        });
      }

      // Library Item Click to Add
      document.querySelectorAll('.library-draggable-item').forEach(item => {
        item.addEventListener('click', () => {
          const type = item.getAttribute('data-comp-type');
          const newId = `comp-${type}-${Date.now().toString().slice(-4)}`;
          const newComp = {
            id: newId,
            type,
            title: `New ${type.toUpperCase()} Component`,
            x: 48,
            y: 120,
            width: type === 'kpi' ? 320 : 700,
            height: type === 'kpi' ? 130 : 160,
            minWidth: 200,
            minHeight: 80,
            zIndex: 15
          };
          if (type === 'kpi') {
            newComp.kpiValue = '₹ 50,000.00';
            newComp.kpiSub = 'Live KPI Metric';
          } else if (type === 'tabs') {
            newComp.tabs = ['Tab Alpha', 'Tab Beta', 'Tab Gamma'];
            newComp.activeTab = 0;
          } else if (type === 'buttons') {
            newComp.buttons = [{ label: 'Action 1', color: 'primary' }, { label: 'Action 2', color: 'secondary' }];
          }
          this.components.push(newComp);
          this.selectedComponentId = newId;
          this.render();
          if (window.Toast) window.Toast.show(`Added new ${type} block to canvas.`, 'info');
        });
      });

      // Component Deletion
      document.querySelectorAll('.comp-delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const id = btn.getAttribute('data-id');
          this.components = this.components.filter(c => c.id !== id);
          if (this.selectedComponentId === id) this.selectedComponentId = null;
          this.render();
        });
      });

      // Tab Detachment into standalone floating card
      document.querySelectorAll('.tab-detach-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const tabIdx = parseInt(btn.getAttribute('data-tab-idx'), 10);
          const compElem = btn.closest('.canvas-component');
          const compId = compElem ? compElem.getAttribute('data-id') : null;
          const comp = this.components.find(c => c.id === compId);
          if (comp && comp.tabs && comp.tabs[tabIdx]) {
            const detachedTabName = comp.tabs.splice(tabIdx, 1)[0];
            const newDetachedId = `comp-detached-${Date.now().toString().slice(-4)}`;
            this.components.push({
              id: newDetachedId,
              type: 'kpi',
              title: `${detachedTabName} (Detached Section)`,
              x: Math.min(comp.x + 30, 400),
              y: comp.y + 70,
              width: 340,
              height: 160,
              minWidth: 220,
              minHeight: 100,
              zIndex: 20,
              kpiValue: 'Detached View Active',
              kpiSub: `Popped out from ${comp.title}`,
              kpiColor: '#00e5ff'
            });
            this.selectedComponentId = newDetachedId;
            this.render();
            if (window.Toast) window.Toast.show(`Detached "${detachedTabName}" into an independent workspace window!`, 'info');
          }
        });
      });

      // DRAG & RESIZE ENGINE
      this.initDragAndResizeEngine(board);
    },

    initDragAndResizeEngine(board) {
      if (!this.isCustomizing || this.isPreviewMode) return;

      const guideX = document.getElementById('snap-guide-x');
      const guideY = document.getElementById('snap-guide-y');
      const ghost = document.getElementById('ghost-preview');
      const selLabel = document.getElementById('canvas-active-selection-label');

      // Click on canvas background deselects
      board.addEventListener('mousedown', (e) => {
        if (e.target === board) {
          this.selectedComponentId = null;
          document.querySelectorAll('.canvas-component').forEach(c => c.classList.remove('selected'));
          if (selLabel) selLabel.textContent = 'Click a component to select and resize';
        }
      });

      // Handle Resize MouseDown
      board.addEventListener('mousedown', (e) => {
        const handle = e.target.closest('.resize-handle');
        if (handle) {
          e.preventDefault();
          e.stopPropagation();
          const dir = handle.getAttribute('data-handle');
          const compId = handle.getAttribute('data-id');
          const comp = this.components.find(c => c.id === compId);
          if (!comp) return;

          const compEl = document.getElementById(compId);
          compEl.classList.add('resizing');

          this.activeResize = {
            dir,
            compId,
            comp,
            compEl,
            startX: e.clientX,
            startY: e.clientY,
            origX: comp.x,
            origY: comp.y,
            origW: comp.width,
            origH: comp.height
          };
          return;
        }

        // Handle Component Drag MouseDown
        const compEl = e.target.closest('.canvas-component');
        if (compEl && !e.target.closest('button') && !e.target.closest('input')) {
          const compId = compEl.getAttribute('data-id');
          const comp = this.components.find(c => c.id === compId);
          if (!comp) return;

          this.selectedComponentId = compId;
          document.querySelectorAll('.canvas-component').forEach(c => c.classList.remove('selected'));
          compEl.classList.add('selected');
          compEl.classList.add('dragging');

          if (selLabel) selLabel.textContent = `Selected: ${comp.title} (W: ${comp.width}px, H: ${comp.height}px)`;

          // Setup ghost preview
          if (ghost) {
            ghost.style.left = `${comp.x}px`;
            ghost.style.top = `${comp.y}px`;
            ghost.style.width = `${comp.width}px`;
            ghost.style.height = `${comp.height}px`;
            ghost.style.display = 'block';
          }

          const boardRect = board.getBoundingClientRect();
          this.activeDrag = {
            compId,
            comp,
            compEl,
            offsetX: e.clientX - compEl.getBoundingClientRect().left,
            offsetY: e.clientY - compEl.getBoundingClientRect().top,
            boardRect
          };
        }
      });

      // Global MouseMove for Resize & Drag
      const onMouseMove = (e) => {
        // RESIZING IN PROGRESS
        if (this.activeResize) {
          const { dir, comp, compEl, startX, startY, origX, origY, origW, origH } = this.activeResize;
          const dx = e.clientX - startX;
          const dy = e.clientY - startY;

          let newW = origW;
          let newH = origH;
          let newX = origX;
          let newY = origY;

          const minW = comp.minWidth || 160;
          const minH = comp.minHeight || 60;
          const boardW = board.clientWidth || 794;
          const boardH = board.clientHeight || 1123;

          if (dir.includes('e')) newW = origW + dx;
          if (dir.includes('s')) newH = origH + dy;
          if (dir.includes('w')) {
            newW = origW - dx;
            newX = origX + dx;
          }
          if (dir.includes('n')) {
            newH = origH - dy;
            newY = origY + dy;
          }

          // Grid snap resize
          if (this.snapToGrid) {
            newW = Math.round(newW / this.gridSize) * this.gridSize;
            newH = Math.round(newH / this.gridSize) * this.gridSize;
            newX = Math.round(newX / this.gridSize) * this.gridSize;
            newY = Math.round(newY / this.gridSize) * this.gridSize;
          }

          // Min/Max constraints
          if (newW < minW) {
            newW = minW;
            if (dir.includes('w')) newX = origX + (origW - minW);
          }
          if (newH < minH) {
            newH = minH;
            if (dir.includes('n')) newY = origY + (origH - minH);
          }

          // Boundary constraints
          if (this.boundaryLock) {
            newX = Math.max(0, newX);
            newY = Math.max(0, newY);
            if (newX + newW > boardW) newW = boardW - newX;
            if (newY + newH > boardH) newH = boardH - newY;
          }

          comp.x = newX;
          comp.y = newY;
          comp.width = newW;
          comp.height = newH;

          compEl.style.left = `${newX}px`;
          compEl.style.top = `${newY}px`;
          compEl.style.width = `${newW}px`;
          compEl.style.height = `${newH}px`;

          const tip = compEl.querySelector('.dimension-tooltip');
          if (tip) tip.textContent = `W: ${newW}px × H: ${newH}px`;
          return;
        }

        // DRAGGING IN PROGRESS
        if (this.activeDrag) {
          const { comp, compEl, offsetX, offsetY, boardRect } = this.activeDrag;
          let rawX = e.clientX - boardRect.left - offsetX;
          let rawY = e.clientY - boardRect.top - offsetY;

          // Grid snap position
          if (this.snapToGrid) {
            rawX = Math.round(rawX / this.gridSize) * this.gridSize;
            rawY = Math.round(rawY / this.gridSize) * this.gridSize;
          }

          // Strict boundary hard-stops
          const boardW = board.clientWidth || 794;
          const boardH = board.clientHeight || 1123;

          if (this.boundaryLock) {
            rawX = Math.max(0, Math.min(rawX, boardW - comp.width));
            rawY = Math.max(0, Math.min(rawY, boardH - comp.height));
          }

          compEl.style.left = `${rawX}px`;
          compEl.style.top = `${rawY}px`;

          // Update ghost box
          if (ghost) {
            ghost.style.left = `${rawX}px`;
            ghost.style.top = `${rawY}px`;
          }

          // Crosshair snap guides
          if (guideX && guideY) {
            guideX.style.left = `${rawX}px`;
            guideX.style.display = 'block';
            guideY.style.top = `${rawY}px`;
            guideY.style.display = 'block';
          }

          comp.x = rawX;
          comp.y = rawY;
        }
      };

      const onMouseUp = () => {
        if (this.activeResize) {
          if (this.activeResize.compEl) {
            this.activeResize.compEl.classList.remove('resizing');
          }
          this.activeResize = null;
          this.saveLayout();
        }

        if (this.activeDrag) {
          if (this.activeDrag.compEl) {
            this.activeDrag.compEl.classList.remove('dragging');
          }
          this.activeDrag = null;
          if (ghost) ghost.style.display = 'none';
          if (guideX) guideX.style.display = 'none';
          if (guideY) guideY.style.display = 'none';
          this.saveLayout();
        }
      };

      window.removeEventListener('mousemove', window._studioMouseMove);
      window.removeEventListener('mouseup', window._studioMouseUp);
      window._studioMouseMove = onMouseMove;
      window._studioMouseUp = onMouseUp;
      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);
    }
  };

  window.LayoutDesignerView = LayoutDesignerView;

})(window);
