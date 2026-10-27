/**
 * SHREERAKSHA SOLUTIONS - GST DOCUMENT TEMPLATE ENGINE
 * Shared by Quotations, Vendor PO, Credit Notes, Debit Notes, and Invoices.
 * 100% exact replica of the official quotation format.
 * Supports multi-page pagination with repeated headers, footers, and dynamic page counts.
 * Page breakdown immediately after subtotal with auto-adjusting rows.
 */

(function (window) {
  'use strict';

  const GSTDocumentTemplate = {
    /**
     * Estimates vertical height in millimeters for a given item row in A4 landscape.
     */
    estimateItemHeight(item) {
      let h = 9.0; // Base height (padding + title + HSN)
      const desc = (item && item.description) ? String(item.description).trim() : '';
      const name = (item && item.name) ? String(item.name).trim() : '';
      const totalLen = name.length + (desc ? desc.length + 5 : 0);
      if (totalLen > 90) {
        h += 7.0;
      } else if (totalLen > 45) {
        h += 3.5;
      }
      return h;
    },

    /**
     * Determines whether items should paginate dynamically based on exact height budget.
     */
    shouldPaginate(items, docType = 'QUOTATION', doc = null) {
      const pages = this.buildPages(items, docType, doc);
      return pages.length > 1;
    },

    /**
     * Builds smart pages with dynamic page breakdown:
     * 1. 1st page is filled 1st before considering breakdown.
     *    If all contents (Items + Sub Total + Total Block + Notes/Terms) fit on Page 1 -> Exactly 1 Page.
     * 2. If Notes & Terms & "For Shreeraksha Solutions" cannot fit on Page 1, but Items + Sub Total + Total Block fit:
     *    Page breakdown happens immediately before "For Shreeraksha Solutions" / Notes & Terms!
     *    Page 1 contains all items, Sub Total, and Total Block with full, uncompromised footer.
     *    Notes & Terms, Banking Details, and "For Shreeraksha Solutions" is the starting point on Page 2!
     * 3. If Total Block cannot fit on Page 1, but Items + Sub Total fit:
     *    Page breakdown is IMMEDIATELY AFTER SUBTOTAL!
     *    Page 2 starts with Total Block, followed by Notes & Terms & Banking & "For Shreeraksha Solutions"!
     * 4. If items exceed Page 1 capacity:
     *    Page 1 fills with as many items as can fit, remaining items continue on Page 2,
     *    and breakdown occurs immediately after Total (or Subtotal).
     */
    buildPages(items, docType = 'QUOTATION', doc = null) {
      const itemList = items || [];
      const n = itemList.length;
      const isQuotation = (docType === 'QUOTATION');
      const isPO = (docType === 'PURCHASE ORDER' || (docType && docType.includes('PURCHASE')));
      const hasBank = !isPO && !isQuotation;

      // Section heights in millimeters (A4 Landscape 210mm height, uncompromised margins)
      // Printable height with 8mm top and bottom padding = 194mm
      const PRINTABLE_PAGE_H = 194.0;
      const HEADER_P1 = 23.0 + (docType === 'TAX INVOICE' || docType.includes('DELIVERY') ? 40.0 : (docType === 'PROFORMA INVOICE' || docType.includes('NOTE') ? 35.0 : 33.0));
      const HEADER_P2 = 23.0 + 8.5;  // Top Header + Title (23.0mm) + Continued Meta Bar (8.5mm) = 31.5mm
      const FOOTER_H = 17.5;         // Footer box with 4 full lines: Address, Phone, Email/GSTIN, Website/MSME (10px, 1.35 line-height)

      const SPACE_P1 = PRINTABLE_PAGE_H - HEADER_P1 - FOOTER_H; // Available for content on Page 1 (~113.5mm)
      const SPACE_P2 = PRINTABLE_PAGE_H - HEADER_P2 - FOOTER_H; // Available for content on Page 2+ (~145.0mm)

      const TBL_HDR = 9.0;
      const SUBTOTAL_H = 6.5;
      const TOTAL_BLK_H = 15.0;

      // Dynamic calculation of terms height based on doc.terms
      const effectiveTerms = (doc && doc.terms) ? String(doc.terms).trim() : '';
      const termsLines = effectiveTerms ? effectiveTerms.split('\n').filter(l => l.trim().length > 0).length : 10;
      const NOTES_TERMS_H = Math.max(34.0, 14.0 + termsLines * 3.2);

      // Bank details box height
      const BANK_H = hasBank ? 26.0 : 0.0;
      // Signature box height with 2X height (96px body + header) = 32mm
      const SIGN_H = 32.0;

      // When Bank is present, right column has Bank + Sign stacked vertically (26 + 32 + 4 = 62mm)
      const FULL_LOWER_H = hasBank ? (BANK_H + SIGN_H + 4.0) : Math.max(NOTES_TERMS_H, SIGN_H);
      // When page breaks after Banking details table (before signature box):
      // Page 1 has Notes/Terms on left and Banking details on right
      const NOTES_TERMS_BANK_H = hasBank ? Math.max(NOTES_TERMS_H, BANK_H) : NOTES_TERMS_H;

      const totalItemsH = itemList.reduce((acc, item) => acc + this.estimateItemHeight(item), 0);

      // Permutation 1: Check if EVERYTHING (Items + Sub Total + Total Block + FULL Lower Block including Sign) fits on Page 1 (Single Page)
      if (totalItemsH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H + FULL_LOWER_H <= SPACE_P1) {
        return [{
          pageIndex: 0,
          items: itemList,
          startIndex: 0,
          showSubTotal: true,
          showTotalBlock: true,
          showNotesTerms: true,
          showBank: hasBank,
          showSign: true
        }];
      }

      // Permutation 2 (User Request): In Tax Invoice and other documents with banking details:
      // If space is not sufficient for the whole lower section, dynamic page break happens AFTER Banking details table,
      // just BEFORE "For Shreeraksha Solutions" signature box!
      if (hasBank && (totalItemsH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H + NOTES_TERMS_BANK_H <= SPACE_P1)) {
        return [
          {
            pageIndex: 0,
            items: itemList,
            startIndex: 0,
            showSubTotal: true,
            showTotalBlock: true,
            showNotesTerms: true,
            showBank: true,
            showSign: false // Page break happens AFTER Banking details table!
          },
          {
            pageIndex: 1,
            items: [], // Signature box is the starting point on Page 2!
            startIndex: n,
            showSubTotal: false,
            showTotalBlock: false,
            showNotesTerms: false,
            showBank: false,
            showSign: true // Just before "For Shreeraksha Solutions"
          }
        ];
      }

      // Permutation 3: Items + Sub Total + Total Block fit on Page 1 (Break after Total Block)
      if (totalItemsH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H <= SPACE_P1) {
        return [
          {
            pageIndex: 0,
            items: itemList,
            startIndex: 0,
            showSubTotal: true,
            showTotalBlock: true,
            showNotesTerms: false,
            showBank: false,
            showSign: false
          },
          {
            pageIndex: 1,
            items: [],
            startIndex: n,
            showSubTotal: false,
            showTotalBlock: false,
            showNotesTerms: true,
            showBank: hasBank,
            showSign: true
          }
        ];
      }

      // Permutation 4: Items + Sub Total fit on Page 1 (Break after Sub Total)
      if (totalItemsH + TBL_HDR + SUBTOTAL_H <= SPACE_P1) {
        return [
          {
            pageIndex: 0,
            items: itemList,
            startIndex: 0,
            showSubTotal: true,
            showTotalBlock: false,
            showNotesTerms: false,
            showBank: false,
            showSign: false
          },
          {
            pageIndex: 1,
            items: [],
            startIndex: n,
            showSubTotal: false,
            showTotalBlock: true,
            showNotesTerms: true,
            showBank: hasBank,
            showSign: true
          }
        ];
      }

      // Permutation 5: Items alone exceed Page 1. Multi-page dynamic distribution.
      const pages = [];
      let rem = [...itemList];
      let startIdx = 0;
      let pIdx = 0;

      // Fill Page 1 first
      const curP1 = [];
      let curH1 = TBL_HDR;
      while (rem.length > 0 && (curH1 + this.estimateItemHeight(rem[0]) <= SPACE_P1 - 6.0)) {
        curH1 += this.estimateItemHeight(rem[0]);
        curP1.push(rem.shift());
      }

      pages.push({
        pageIndex: pIdx++,
        items: curP1,
        startIndex: startIdx,
        showSubTotal: false,
        showTotalBlock: false,
        showNotesTerms: false,
        showBank: false,
        showSign: false
      });
      startIdx += curP1.length;

      // Process continuation pages
      while (rem.length > 0) {
        const remH = rem.reduce((acc, i) => acc + this.estimateItemHeight(i), 0);

        // Check if remaining items + Sub Total + Total Block + FULL Lower Block fit on this continuation page
        if (remH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H + FULL_LOWER_H <= SPACE_P2) {
          pages.push({
            pageIndex: pIdx++,
            items: rem,
            startIndex: startIdx,
            showSubTotal: true,
            showTotalBlock: true,
            showNotesTerms: true,
            showBank: hasBank,
            showSign: true
          });
          startIdx += rem.length;
          rem = [];
          break;
        }

        // Check if remaining items + Sub Total + Total Block + Notes/Terms/Bank fit on this continuation page
        if (hasBank && (remH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H + NOTES_TERMS_BANK_H <= SPACE_P2)) {
          pages.push({
            pageIndex: pIdx++,
            items: rem,
            startIndex: startIdx,
            showSubTotal: true,
            showTotalBlock: true,
            showNotesTerms: true,
            showBank: true,
            showSign: false
          });
          startIdx += rem.length;
          rem = [];
          pages.push({
            pageIndex: pIdx++,
            items: [],
            startIndex: startIdx,
            showSubTotal: false,
            showTotalBlock: false,
            showNotesTerms: false,
            showBank: false,
            showSign: true
          });
          break;
        }

        // Check if remaining items + Sub Total + Total Block fit on this continuation page (Break after Total)
        if (remH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H <= SPACE_P2) {
          pages.push({
            pageIndex: pIdx++,
            items: rem,
            startIndex: startIdx,
            showSubTotal: true,
            showTotalBlock: true,
            showNotesTerms: false,
            showBank: false,
            showSign: false
          });
          startIdx += rem.length;
          rem = [];
          pages.push({
            pageIndex: pIdx++,
            items: [],
            startIndex: startIdx,
            showSubTotal: false,
            showTotalBlock: false,
            showNotesTerms: true,
            showBank: hasBank,
            showSign: true
          });
          break;
        }

        // Check if remaining items + Sub Total fit on this continuation page (Break after Subtotal)
        if (remH + TBL_HDR + SUBTOTAL_H <= SPACE_P2) {
          pages.push({
            pageIndex: pIdx++,
            items: rem,
            startIndex: startIdx,
            showSubTotal: true,
            showTotalBlock: false,
            showNotesTerms: false,
            showBank: false,
            showSign: false
          });
          startIdx += rem.length;
          rem = [];
          pages.push({
            pageIndex: pIdx++,
            items: [],
            startIndex: startIdx,
            showSubTotal: false,
            showTotalBlock: true,
            showNotesTerms: true,
            showBank: hasBank,
            showSign: true
          });
          break;
        }

        // Chunk remaining items for this continuation page
        const chunk = [];
        let curChunkH = TBL_HDR;
        while (rem.length > 0 && (curChunkH + this.estimateItemHeight(rem[0]) <= SPACE_P2 - 8.0)) {
          curChunkH += this.estimateItemHeight(rem[0]);
          chunk.push(rem.shift());
        }

        pages.push({
          pageIndex: pIdx++,
          items: chunk,
          startIndex: startIdx,
          showSubTotal: false,
          showTotalBlock: false,
          showNotesTerms: false,
          showBank: false,
          showSign: false
        });
        startIdx += chunk.length;
      }

      return pages;
    },

    /**
     * Renders table rows for a specific page with continuous SL numbering
     */
    renderItemRows(items, startIndex, isInterState, isQuotation = false) {
      return items.map((item, localIndex) => {
        const globalIndex = startIndex + localIndex;
        const hsnSacCode = item.hsnCode || item.sacCode || item.hsn || '90279090';
        const discDisplay = item.discountType === 'amount' 
          ? window.Calculator.formatNumber(item.discountVal)
          : `${(parseFloat(item.discountVal) || 0).toFixed(2)}%`;

        // 2-Digit Serial Number: 01, 02, ..., 10, 99
        const slNumber = String(globalIndex + 1).padStart(2, '0');

        // Quantity with Unit of Measurement: e.g. 6 No's, 1 Pcs
        const qtyVal = parseFloat(item.quantity) || 0;
        const qtyNumStr = Number.isInteger(qtyVal) ? String(qtyVal) : qtyVal.toFixed(2);
        let uStr = (item.unit || (item.itemId ? (window.AppStore.getById('items', item.itemId) || {}).unit : '') || "No's").trim();
        const uClean = uStr.toLowerCase().replace(/[^a-z]/g, '');
        if (uClean === 'nos' || uClean === 'no' || uClean === '') {
          uStr = "No's";
        } else if (uClean === 'pcs' || uClean === 'pc' || uClean === 'piece' || uClean === 'pieces') {
          uStr = "Pcs";
        } else if (uClean === 'set' || uClean === 'sets') {
          uStr = "Sets";
        } else if (uClean === 'service' || uClean === 'services') {
          uStr = "Service";
        } else if (uClean === 'box' || uClean === 'boxes') {
          uStr = "Box";
        } else if (uClean === 'mtr' || uClean === 'meter' || uClean === 'meters') {
          uStr = "Mtr";
        }
        const formattedQtyWithUnit = `${qtyNumStr} ${uStr}`;

        // Task 4: Material Description and Technical details continued in 1st row itself
        // with separation of Closed brackets and inverted comas.
        // HSN/SAC code at the last line of the row.
        const desc = (item && item.description) ? String(item.description).trim() : '';
        let cleanDesc = desc;
        if (cleanDesc) {
          cleanDesc = cleanDesc.replace(/^[\s\(\["']+|[\s\)\]"']+$/g, '').trim();
        }
        const itemTitle = (item.name || '').trim();
        const technicalDetailsPart = cleanDesc ? ` ("${cleanDesc}")` : '';

        // Task 3: Quotation GST columns - single column % of GST and Amount of GST
        let taxCells = '';
        if (isQuotation) {
          const gstRate = item.taxRate !== undefined && item.taxRate !== null && item.taxRate !== ''
            ? parseFloat(item.taxRate)
            : ((parseFloat(item.cgstRate) || 0) + (parseFloat(item.sgstRate) || 0) || parseFloat(item.igstRate) || 18);
          const gstAmount = ((parseFloat(item.cgstAmount) || 0) + (parseFloat(item.sgstAmount) || 0)) || (parseFloat(item.igstAmount) || 0);

          taxCells = `
            <td class="sr-cell-tax-pct">${gstRate}%</td>
            <td class="sr-cell-tax-amt">${window.Calculator.formatNumber(gstAmount)}</td>
          `;
        } else if (isInterState) {
          taxCells = `
            <td class="sr-cell-tax-pct">${item.igstRate}%</td>
            <td class="sr-cell-tax-amt">${window.Calculator.formatNumber(item.igstAmount)}</td>
          `;
        } else {
          taxCells = `
            <td class="sr-cell-tax-pct">${item.cgstRate}%</td>
            <td class="sr-cell-tax-amt">${window.Calculator.formatNumber(item.cgstAmount)}</td>
            <td class="sr-cell-tax-pct">${item.sgstRate}%</td>
            <td class="sr-cell-tax-amt">${window.Calculator.formatNumber(item.sgstAmount)}</td>
          `;
        }

        return `
          <tr>
            <td class="sr-cell-num">${slNumber}</td>
            <td class="sr-cell-desc">
              <div class="sr-item-desc-main"><span class="sr-item-title">${itemTitle}</span>${technicalDetailsPart ? `<span class="sr-item-specs">${technicalDetailsPart}</span>` : ''}</div>
              <div class="sr-item-hsn">HSN/SAC: ${hsnSacCode}</div>
            </td>
            <td class="sr-cell-qty" style="white-space: nowrap;">${formattedQtyWithUnit}</td>
            <td class="sr-cell-rate">${window.Calculator.formatNumber(item.rate)}</td>
            <td class="sr-cell-amount">${window.Calculator.formatNumber(item.grossAmount)}</td>
            <td class="sr-cell-disc">${discDisplay}</td>
            <td class="sr-cell-taxable">${window.Calculator.formatNumber(item.taxableAmount)}</td>
            ${taxCells}
            <td class="sr-cell-total">${window.Calculator.formatNumber(item.totalLineAmount)}</td>
          </tr>
        `;
      }).join('');
    },

    /**
     * Renders Amount in Words and Rounding & Grand Total Table
     */
    renderTotalBlock(ctx) {
      return `
        <!-- TOTAL BLOCK (WORDS + ROUNDING/TOTAL) -->
        <div class="sr-total-block">
          <div class="sr-words-col">
            <div class="sr-words-label">Amount in Words</div>
            <div class="sr-words-val">${ctx.calc.totalInWords}</div>
          </div>
          <div class="sr-total-col">
            <table class="sr-rounding-table">
              <tbody>
                <tr>
                  <td class="sr-round-label">Rounding</td>
                  <td class="sr-round-val">${ctx.calc.rounding >= 0 ? '+' + ctx.calc.rounding.toFixed(2) : ctx.calc.rounding.toFixed(2)}</td>
                </tr>
                <tr>
                  <td class="sr-total-label">Total</td>
                  <td class="sr-total-val">₹ ${window.Calculator.formatNumber(ctx.calc.roundedTotal)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `;
    },

    /**
     * Parse structured bank details from organization profile
     */
    getBankDetails(org = {}) {
      const details = {
        bankName: org.bankName || 'State Bank of India',
        accountName: org.accountName || 'SHREERAKSHA SOLUTIONS',
        accountNumber: org.accountNumber || '45666081503',
        branch: org.branch || 'PARKALA',
        ifscCode: org.ifscCode || 'SBIN0016869'
      };

      if (org.bankDetails && typeof org.bankDetails === 'string') {
        const lines = org.bankDetails.split('\n');
        for (const line of lines) {
          const parts = line.split(/[:\t]+/);
          if (parts.length >= 2) {
            const key = parts[0].toLowerCase().trim();
            const val = parts.slice(1).join(':').trim();
            if (key.includes('bank name')) details.bankName = val;
            else if (key.includes('account') && key.includes('name')) details.accountName = val;
            else if (key.includes('account') && (key.includes('number') || key.includes('no'))) details.accountNumber = val;
            else if (key.includes('ifsc')) details.ifscCode = val;
            else if (key.includes('branch') && !key.includes('ifsc')) details.branch = val;
          }
        }
      }
      return details;
    },

    /**
     * Renders Terms & Conditions list dynamically from doc.terms or defaults
     */
    renderTermsList(termsStr, paymentTerms, defaultOrgTerms = '') {
      const payTerm = paymentTerms || '30 Days net';
      
      let effectiveTerms = termsStr;
      if (!effectiveTerms || !String(effectiveTerms).trim()) {
        effectiveTerms = defaultOrgTerms || (window.AppStore && window.AppStore.getOrg() && window.AppStore.getOrg().defaultTerms) || '';
      }

      if (!effectiveTerms || !String(effectiveTerms).trim()) {
        effectiveTerms = `• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (${payTerm}).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery.`;
      }

      const rawLines = String(effectiveTerms).split('\n');
      const rendered = [];

      for (let rawLine of rawLines) {
        const trimmed = rawLine.trim();
        if (!trimmed) continue;

        // Check if raw line or trimmed line indicates a sub-bullet: starts with * or - or indented
        const isSubBullet = (/^\s+[\*\-•]/.test(rawLine)) || trimmed.startsWith('*') || (trimmed.startsWith('-') && !trimmed.startsWith('--'));
        
        // Strip leading bullet characters, replacement chars (\ufffd), asterisks, dashes, whitespace
        let cleanText = trimmed.replace(/^[\s\ufffd•\*\-\–\—\>]+/, '').trim();
        
        if (cleanText) {
          if (isSubBullet) {
            rendered.push(`<li class="sr-sub-bullet">${cleanText}</li>`);
          } else {
            rendered.push(`<li>${cleanText}</li>`);
          }
        }
      }

      if (rendered.length === 0) {
        return `<li>Above prices are FOR Destination.</li>
<li>Please mention our Estimate number on all future correspondence.</li>
<li>Please share your valid GSTIN in your Purchase Order.</li>
<li>Payment Terms: As agreed (${payTerm}).</li>
<li>In case of Refurbished requirement</li>
<li class="sr-sub-bullet">The defective part need to be returned - against delivery.</li>
<li>Delivery will be within 3-4 weeks from date of PO.</li>
<li class="sr-sub-bullet">Goods indicated above in stock are accurate as of the quote date.</li>
<li class="sr-sub-bullet">If goods are out of stock at the time of release of PO, standard lead time would apply.</li>
<li>Payment will be 50% advance and balance against delivery.</li>`;
      }

      return rendered.join('\n');
    },

    /**
     * Renders Notes, Terms & Conditions, Bank Details, and Authorized Signature
     * Dynamically supports breaking after Banking Details table before Signature box
     */
    renderNotesAndTermsBlock(doc, ctx, pageCfg = {}) {
      const isQuotation = (ctx.docType === 'QUOTATION');
      const isPO = (ctx.docType === 'PURCHASE ORDER' || (ctx.docType && ctx.docType.includes('PURCHASE')));
      const showBank = pageCfg.showBank !== undefined ? pageCfg.showBank : (!isPO && !isQuotation);
      const showSign = pageCfg.showSign !== undefined ? pageCfg.showSign : true;
      const showNotesTerms = pageCfg.showNotesTerms !== undefined ? pageCfg.showNotesTerms : true;
      const bank = this.getBankDetails(ctx.org || {});

      if (!showNotesTerms && !showBank && !showSign) return '';

      // If only signature box is to be shown (e.g. Page 2 after banking details dynamic break)
      if (!showNotesTerms && !showBank && showSign) {
        return `
          <!-- SIGNATURE BOX ONLY (DYNAMIC BREAK AFTER BANKING DETAILS) -->
          <div class="sr-notes-terms-block sr-sign-only-block" style="justify-content: flex-end; margin-top: 12mm;">
            <div class="sr-bank-sign-col" style="margin-left: auto;">
              <div class="sr-sign-box">
                <div class="sr-sign-header">For ${ctx.org.legalName || 'Shreeraksha Solutions'}</div>
                <div class="sr-sign-body">
                  <div class="sr-sign-line"></div>
                  <div class="sr-sign-label">Authorized Signature</div>
                </div>
              </div>
            </div>
          </div>
        `;
      }

      return `
        <!-- NOTES & TERMS BLOCK (NOTES/TERMS + BANK/SIGN) -->
        <div class="sr-notes-terms-block">
          ${showNotesTerms ? `
          <div class="sr-notes-terms-col">
            <div class="sr-notes-label">Notes</div>
            <div class="sr-notes-val">${doc.notes || 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned'}</div>

            <div class="sr-terms-label">Terms & Conditions</div>
            <ul class="sr-terms-list">
              ${this.renderTermsList(doc.terms, doc.paymentTerms, (ctx.org && ctx.org.defaultTerms) || '')}
            </ul>
          </div>
          ` : '<div class="sr-notes-terms-col"></div>'}

          <div class="sr-bank-sign-col">
            ${showBank ? `
            <div class="sr-bank-box">
              <div class="sr-bank-header">COMPANY BANKING DETAILS (FOR RTGS / NEFT)</div>
              <table class="sr-bank-table">
                <tbody>
                  <tr>
                    <td class="sr-bank-k">Bank Name:</td>
                    <td class="sr-bank-v">${bank.bankName}</td>
                  </tr>
                  <tr>
                    <td class="sr-bank-k">Account Name:</td>
                    <td class="sr-bank-v">${bank.accountName}</td>
                  </tr>
                  <tr>
                    <td class="sr-bank-k">Account No:</td>
                    <td class="sr-bank-v">${bank.accountNumber}</td>
                  </tr>
                  <tr>
                    <td class="sr-bank-k">IFSC Code:</td>
                    <td class="sr-bank-v">${bank.ifscCode}</td>
                  </tr>
                  <tr>
                    <td class="sr-bank-k">Branch:</td>
                    <td class="sr-bank-v">${bank.branch}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            ` : ''}

            ${showSign ? `
            <div class="sr-sign-box">
              <div class="sr-sign-header">For ${ctx.org.legalName || 'Shreeraksha Solutions'}</div>
              <div class="sr-sign-body">
                <div class="sr-sign-line"></div>
                <div class="sr-sign-label">Authorized Signature</div>
              </div>
            </div>
            ` : ''}
          </div>
        </div>
      `;
    },

    /**
     * Renders a single page with repeated header, items table, and bottom-pinned footer
     */
    renderPage(doc, pageCfg, totalPages, ctx) {
      const isFirstPage = (pageCfg.pageIndex === 0);
      const isQuotation = (ctx.docType === 'QUOTATION');
      const isInvoiceOrDeliveryNote = (ctx.docType === 'TAX INVOICE' || ctx.docType === 'DELIVERY CHALLAN' || ctx.docType === 'DELIVERY NOTE');
      const isDNCNOrProforma = (ctx.docType === 'PROFORMA INVOICE' || ctx.docType === 'DEBIT NOTE' || ctx.docType === 'CREDIT NOTE');

      return `
        <div class="shreeraksha-document shreeraksha-document-page ${ctx.docType === 'QUOTATION' ? 'doc-quotation' : ''}" data-doc-type="${ctx.docType}">
          
          <!-- TOP HEADER WITH EXACT UPLOADED LOGO (MAINTAINED AS IT IS, REPEATED ON EVERY PAGE) -->
          <div class="sr-header-top">
            <div class="sr-company-title-wrap">
              <img src="assets/shreeraksha-text-exact.png" alt="SHREERAKSHA SOLUTIONS" class="sr-brand-img">
            </div>

            <div class="sr-ornamental-logo">
              <img src="assets/shreeraksha-emblem-exact.png" alt="Shreeraksha Emblem" class="sr-logo-img">
            </div>
          </div>

          <!-- DOCUMENT TITLE (REPEATED ON EVERY PAGE) -->
          <div class="sr-document-title">
            ${ctx.docType}
          </div>

          ${isFirstPage ? (
            isInvoiceOrDeliveryNote ? `
            <!-- INVOICE & DELIVERY NOTE: BILLING DETAILS TOP, BILL TO & SHIP TO BELOW -->
            <table class="sr-meta-table sr-invoice-dn-meta-table">
              <thead>
                <tr>
                  <th colspan="2" style="background-color: #9BA8AB; color: #000000; font-weight: 800; font-size: 11px; padding: 3px 6px; border: 1.5px solid #000000;">BILLING DETAILS</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="width: 50%; padding: 4px 6px; vertical-align: top;">
                    <div class="sr-meta-kv-grid" style="grid-template-columns: 110px 1fr; row-gap: 2px; font-size: 10px;">
                      <span class="sr-meta-k">Billing Doc No:</span>
                      <span class="sr-meta-v" style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">${doc.number || (ctx.docType.includes('DELIVERY') ? 'SHRKS/DC/26-27/001' : 'SHRKS/Inv/26-27/019')}</span>

                      <span class="sr-meta-k">Payment Terms:</span>
                      <span class="sr-meta-v">${doc.paymentTerms || '30 Days net'}</span>

                      <span class="sr-meta-k">Buyer Po:</span>
                      <span class="sr-meta-v">${doc.poNumber || doc.reference || '-'}</span>
                    </div>
                  </td>
                  <td style="width: 50%; padding: 4px 6px; vertical-align: top;">
                    <div class="sr-meta-kv-grid" style="grid-template-columns: 100px 1fr; row-gap: 2px; font-size: 10px;">
                      <span class="sr-meta-k">Billing Date:</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.date)}</span>

                      <span class="sr-meta-k">Due Date:</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.dueDate || doc.date)}</span>

                      <span class="sr-meta-k">PO Date:</span>
                      <span class="sr-meta-v">${(doc.poDate || doc.referenceDate) ? window.Calculator.formatDate(doc.poDate || doc.referenceDate) : '-'}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
              <thead>
                <tr>
                  <th style="width: 50%; background-color: #9BA8AB; color: #000000; font-weight: 800; font-size: 11px; padding: 3px 6px; border: 1.5px solid #000000;">BILL TO (BUYER)</th>
                  <th style="width: 50%; background-color: #9BA8AB; color: #000000; font-weight: 800; font-size: 11px; padding: 3px 6px; border: 1.5px solid #000000;">SHIP TO (CONSIGNEE / DELIVERY)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    <div class="sr-customer-name" style="font-size: 11.5px; font-weight: 800; margin-bottom: 2px;">
                      ${ctx.party.company || ctx.party.name}
                    </div>
                    <div style="white-space: pre-line; line-height: 1.35; font-size: 9.5px; margin-bottom: 3px;">
                      ${doc.billingAddress || ctx.party.billingAddress || ctx.party.address || 'Address not provided'}
                    </div>
                    <div style="font-size: 9.5px; font-weight: 700;">
                      GSTIN &nbsp;<span style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">${ctx.party.taxId || ctx.party.gstin || '29AATCM4200G1ZD'}</span>
                    </div>
                    <div style="font-size: 9px; margin-top: 1px;">
                      State: <b>${ctx.party.state || ctx.placeOfSupply}</b>
                    </div>
                  </td>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    <div class="sr-customer-name" style="font-size: 11.5px; font-weight: 800; margin-bottom: 2px;">
                      ${doc.shippingPartyName || ctx.party.shippingPartyName || ctx.party.company || ctx.party.name}
                    </div>
                    <div style="white-space: pre-line; line-height: 1.35; font-size: 9.5px; margin-bottom: 3px;">
                      ${doc.shippingAddress || ctx.party.shippingAddress || doc.billingAddress || ctx.party.billingAddress || ctx.party.address || 'Same as billing address'}
                    </div>
                    <div style="font-size: 9.5px; font-weight: 700;">
                      GSTIN &nbsp;<span style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">${doc.shippingGstin || ctx.party.shippingGstin || ctx.party.taxId || ctx.party.gstin || '29AATCM4200G1ZD'}</span>
                    </div>
                    <div style="font-size: 9px; margin-top: 1px;">
                      State: <b>${doc.shippingState || ctx.party.state || ctx.placeOfSupply}</b>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            ` : (isDNCNOrProforma ? `
            <!-- DN/CN & PROFORMA INVOICE: BILL TO LEFT, BILLING DETAILS RIGHT -->
            <table class="sr-meta-table sr-dn-cn-proforma-meta-table">
              <thead>
                <tr>
                  <th style="width: 50%; background-color: #9BA8AB; color: #000000; font-weight: 800; font-size: 11px; padding: 3px 6px; border: 1.5px solid #000000;">BILL TO</th>
                  <th style="width: 50%; background-color: #9BA8AB; color: #000000; font-weight: 800; font-size: 11px; padding: 3px 6px; border: 1.5px solid #000000;">BILLING DETAILS</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    <div class="sr-customer-name" style="font-size: 11.5px; font-weight: 800; margin-bottom: 2px;">
                      ${ctx.party.company || ctx.party.name}
                    </div>
                    <div style="white-space: pre-line; line-height: 1.35; font-size: 9.5px; margin-bottom: 3px;">
                      ${doc.billingAddress || ctx.party.billingAddress || ctx.party.address || 'Address not provided'}
                    </div>
                    <div style="font-size: 9.5px; font-weight: 700;">
                      GSTIN &nbsp;<span style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">${ctx.party.taxId || ctx.party.gstin || '29AATCM4200G1ZD'}</span>
                    </div>
                    <div style="font-size: 9px; margin-top: 1px;">
                      State: <b>${ctx.party.state || ctx.placeOfSupply}</b>
                    </div>
                  </td>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    <div class="sr-meta-kv-grid" style="grid-template-columns: 115px 1fr; row-gap: 2px; font-size: 10px;">
                      <span class="sr-meta-k">Billing Doc No:</span>
                      <span class="sr-meta-v" style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">${doc.number || (ctx.docType === 'PROFORMA INVOICE' ? 'SHRKS/PI/26-27/001' : (ctx.docType === 'DEBIT NOTE' ? 'SHRKS/DN/26-27/001' : 'SHRKS/CN/26-27/001'))}</span>

                      <span class="sr-meta-k">Billing Date:</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.date)}</span>

                      <span class="sr-meta-k">Payment Terms:</span>
                      <span class="sr-meta-v">${doc.paymentTerms || '30 Days net'}</span>

                      <span class="sr-meta-k">Buyer Po:</span>
                      <span class="sr-meta-v">${doc.poNumber || doc.reference || '-'}</span>

                      <span class="sr-meta-k">Due Date:</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.dueDate || doc.date)}</span>

                      <span class="sr-meta-k">PO Date:</span>
                      <span class="sr-meta-v">${(doc.poDate || doc.referenceDate) ? window.Calculator.formatDate(doc.poDate || doc.referenceDate) : '-'}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            ` : `
            <!-- STANDARD TWO COLUMN META BOX (QUOTATION, PURCHASE ORDER) -->
            <table class="sr-meta-table">
              <thead>
                <tr>
                  <th style="width: 50%;">${ctx.partyHeaderLabel}</th>
                  <th style="width: 50%;">${isQuotation ? 'QUOTATION DETAILS' : `${ctx.docType} DETAILS`}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    ${(isQuotation || doc.attention || ctx.party.attention) ? `
                      <div class="sr-kind-attention-block" style="margin-bottom: 4px; padding-bottom: 2px; border-bottom: 1px solid #000000;">
                        <span class="sr-attention-label" style="font-size: 11px; font-weight: 700; color: #000000;">Kind Attention : </span>
                        <span class="sr-attention-name" style="font-size: 11.5px; font-weight: 700; color: #000000;">${doc.attention || ctx.party.attention || 'Mr. Sreekar Nayak'}</span>
                      </div>
                    ` : ''}
                    <div class="sr-customer-name">${ctx.party.company || ctx.party.name}</div>
                    <div style="white-space: pre-line; line-height: 1.35; margin-bottom: 3px;">${ctx.party.billingAddress || ctx.party.address || 'Address not provided'}</div>
                    <div style="font-weight: 700;">GSTIN &nbsp;${ctx.party.taxId || ctx.party.gstin || '29AATCM4200G1ZD'}</div>
                  </td>
                  <td style="vertical-align: top; padding: 4px 6px;">
                    <div class="sr-meta-kv-grid">
                      <span class="sr-meta-k">${ctx.numLabel}</span>
                      <span class="sr-meta-v">${doc.number || 'SHRKS/Qtn/26-27/019'}</span>

                      <span class="sr-meta-k">${ctx.dateLabel}</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.date)}</span>

                      <span class="sr-meta-k">${ctx.expLabel}</span>
                      <span class="sr-meta-v">${window.Calculator.formatDate(doc.expiryDate || doc.dueDate || doc.originalInvoiceNumber)}</span>

                      <span class="sr-meta-k">Reference#</span>
                      <span class="sr-meta-v">${doc.reference ? (doc.reference + (doc.referenceDate ? ` dt. ${window.Calculator.formatDate(doc.referenceDate)}` : '')) : (doc.referenceDate ? window.Calculator.formatDate(doc.referenceDate) : '')}</span>

                      <span class="sr-meta-k">Email</span>
                      <span class="sr-meta-v">${ctx.party.email || ''}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            `)
          ) : `
            <!-- CONTINUATION COMPACT META REFERENCE BAR (PAGE 2+) -->
            <div class="sr-continued-meta-bar">
              <span><strong>${ctx.numLabel}:</strong> ${doc.number || ''}</span>
              <span><strong>${ctx.dateLabel}:</strong> ${window.Calculator.formatDate(doc.date)}</span>
              <span><strong>${ctx.partyHeaderLabel}:</strong> ${ctx.party.company || ctx.party.name}</span>
              <span><strong>Page:</strong> ${pageCfg.pageIndex + 1} of ${totalPages}</span>
            </div>
          `}

          ${pageCfg.items.length > 0 ? `
            <!-- GST ITEMS GRID TABLE (AUTO-ADJUSTING ROWS & COLUMNS) -->
            <table class="sr-items-table">
              <thead>
                ${isQuotation ? `
                  <!-- QUOTATION GST HEADER: SINGLE GST COLUMN (% of GST & Amount of GST) -->
                  <tr>
                    <th rowspan="2" class="sr-th-sl">SL</th>
                    <th rowspan="2" class="sr-th-desc">Item & Description</th>
                    <th rowspan="2" class="sr-th-qty">Qty</th>
                    <th rowspan="2" class="sr-th-rate">Rate</th>
                    <th rowspan="2" class="sr-th-amount">Amount</th>
                    <th rowspan="2" class="sr-th-disc">${ctx.discHeaderLabel}</th>
                    <th rowspan="2" class="sr-th-taxable">Taxable<br>Amount</th>
                    <th colspan="2" class="sr-th-tax">GST</th>
                    <th rowspan="2" class="sr-th-total">Total</th>
                  </tr>
                  <tr>
                    <th class="sr-th-tax-pct">% of GST</th>
                    <th class="sr-th-tax-amt">Amount of GST</th>
                  </tr>
                ` : (ctx.isInterState ? `
                  <!-- INTER-STATE (IGST) HEADER -->
                  <tr>
                    <th rowspan="2" class="sr-th-sl">SL</th>
                    <th rowspan="2" class="sr-th-desc">Item & Description</th>
                    <th rowspan="2" class="sr-th-qty">Qty</th>
                    <th rowspan="2" class="sr-th-rate">Rate</th>
                    <th rowspan="2" class="sr-th-amount">Amount</th>
                    <th rowspan="2" class="sr-th-disc">${ctx.discHeaderLabel}</th>
                    <th rowspan="2" class="sr-th-taxable">Taxable<br>Amount</th>
                    <th colspan="2" class="sr-th-tax">IGST</th>
                    <th rowspan="2" class="sr-th-total">Total</th>
                  </tr>
                  <tr>
                    <th class="sr-th-tax-pct">%</th>
                    <th class="sr-th-tax-amt">Amt</th>
                  </tr>
                ` : `
                  <!-- INTRA-STATE (CGST + SGST) HEADER -->
                  <tr>
                    <th rowspan="2" class="sr-th-sl">SL</th>
                    <th rowspan="2" class="sr-th-desc">Item & Description</th>
                    <th rowspan="2" class="sr-th-qty">Qty</th>
                    <th rowspan="2" class="sr-th-rate">Rate</th>
                    <th rowspan="2" class="sr-th-amount">Amount</th>
                    <th rowspan="2" class="sr-th-disc">${ctx.discHeaderLabel}</th>
                    <th rowspan="2" class="sr-th-taxable">Taxable<br>Amount</th>
                    <th colspan="2" class="sr-th-tax">CGST</th>
                    <th colspan="2" class="sr-th-tax">SGST</th>
                    <th rowspan="2" class="sr-th-total">Total</th>
                  </tr>
                  <tr>
                    <th class="sr-th-tax-pct">%</th>
                    <th class="sr-th-tax-amt">Amt</th>
                    <th class="sr-th-tax-pct">%</th>
                    <th class="sr-th-tax-amt">Amt</th>
                  </tr>
                `)}
              </thead>
              <tbody>
                ${this.renderItemRows(pageCfg.items, pageCfg.startIndex, ctx.isInterState, isQuotation)}

                ${pageCfg.showSubTotal ? `
                  <!-- SUB TOTAL ROW - PAGE BREAKDOWN IMMEDIATELY AFTER THIS -->
                  <tr class="sr-subtotal-row">
                    <td colspan="4" class="sr-subtotal-label">Sub Total</td>
                    <td class="sr-cell-amount">₹ ${window.Calculator.formatNumber(ctx.calc.subTotalGross)}</td>
                    <td class="sr-cell-disc">₹ ${window.Calculator.formatNumber(ctx.calc.totalDiscount)}</td>
                    <td class="sr-cell-taxable">₹ ${window.Calculator.formatNumber(ctx.calc.totalTaxable)}</td>
                    
                    ${isQuotation ? `
                      <td colspan="2" class="sr-cell-tax-amt" style="text-align: right;">₹ ${window.Calculator.formatNumber((ctx.calc.totalCGST || 0) + (ctx.calc.totalSGST || 0) || ctx.calc.totalIGST || 0)}</td>
                    ` : (ctx.isInterState ? `
                      <td colspan="2" class="sr-cell-tax-amt" style="text-align: right;">₹ ${window.Calculator.formatNumber(ctx.calc.totalIGST)}</td>
                    ` : `
                      <td colspan="2" class="sr-cell-tax-amt" style="text-align: right;">₹ ${window.Calculator.formatNumber(ctx.calc.totalCGST)}</td>
                      <td colspan="2" class="sr-cell-tax-amt" style="text-align: right;">₹ ${window.Calculator.formatNumber(ctx.calc.totalSGST)}</td>
                    `)}

                    <td class="sr-cell-total">₹ ${window.Calculator.formatNumber(ctx.calc.subTotalFinal)}</td>
                  </tr>
                ` : ''}
              </tbody>
            </table>
          ` : ''}

          ${pageCfg.showTotalBlock ? this.renderTotalBlock(ctx) : ''}

          ${(pageCfg.showNotesTerms || pageCfg.showBank || pageCfg.showSign) ? this.renderNotesAndTermsBlock(doc, ctx, pageCfg) : ''}

          <!-- BOTTOM FOOTER LINE SEPARATOR (MAINTAINED AS IT IS, REPEATED ON EVERY PAGE) -->
          <div class="sr-footer-box">
            <div class="sr-footer-left">
              <div><span class="sr-footer-strong">Address :</span> 5-68, Mulliya Mata House, Ajjavara Post, Sulya, Dakshina Kannada - 574 239, Karnataka, India</div>
              <div><span class="sr-footer-strong">Phone :</span> +91 9880 54 99 55 &nbsp;&nbsp;+91 96636 91509</div>
              <div><span class="sr-footer-strong">E-Mail :</span> connect@shreeraksha.in &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sr-footer-strong">GSTIN :</span> 29FEAPS4448D1ZA</div>
              <div><span class="sr-footer-strong">Website :</span> www.shreeraksha.in &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sr-footer-strong">MSME Reg. No. :</span> UDYAM-KR-11-0087041</div>
            </div>

            <div class="sr-footer-right">
              <div class="sr-footer-page-pill">Page ${pageCfg.pageIndex + 1} of ${totalPages}</div>
            </div>
          </div>

        </div>
      `;
    },

    /**
     * Main entry point to render document HTML
     */
    render(doc, options = {}) {
      const org = window.AppStore.getOrg();
      let docType = options.docType || doc.docType;
      if (!docType) {
        if (doc.invoiceType === 'delivery_note' || doc.invoiceType === 'dc' || (doc.number && doc.number.includes('/DC/'))) {
          docType = 'DELIVERY CHALLAN';
        } else if (doc.invoiceType === 'proforma' || (doc.number && doc.number.includes('/PI/'))) {
          docType = 'PROFORMA INVOICE';
        } else if (doc.invoiceType === 'tax' || (doc.number && doc.number.includes('/Inv/'))) {
          docType = 'TAX INVOICE';
        } else {
          docType = 'QUOTATION';
        }
      } else if (docType === 'TAX INVOICE') {
        if (doc.invoiceType === 'delivery_note' || doc.invoiceType === 'dc' || (doc.number && doc.number.includes('/DC/'))) {
          docType = 'DELIVERY CHALLAN';
        } else if (doc.invoiceType === 'proforma' || (doc.number && doc.number.includes('/PI/'))) {
          docType = 'PROFORMA INVOICE';
        }
      }

      const partyType = options.partyType || (docType.includes('PURCHASE') || doc.vendorId ? 'vendor' : 'customer');
      
      const party = partyType === 'vendor' 
        ? (window.AppStore.getById('customers', doc.vendorId || doc.customerId) || { name: 'Vendor Name' })
        : (window.AppStore.getById('customers', doc.customerId) || { name: 'Customer Name' });

      const placeOfSupply = doc.placeOfSupply || party.placeOfSupply || 'Karnataka (29)';
      const isInterState = window.Calculator.isInterState(placeOfSupply, org.state || 'Karnataka (29)');

      // Calculate totals using GST calculation engine
      const calc = window.Calculator.computeGSTDocumentTotals(doc.items || [], isInterState, doc.adjustment || 0);

      // Determine labels based on document type
      let numLabel = 'Quote#';
      let dateLabel = 'Quote Date';
      let expLabel = 'Validity date';

      if (docType === 'PURCHASE ORDER') {
        numLabel = 'PO#';
        dateLabel = 'PO Date';
        expLabel = 'Delivery Due';
      } else if (docType === 'CREDIT NOTE') {
        numLabel = 'Credit Note#';
        dateLabel = 'CN Date';
        expLabel = 'Original Inv#';
      } else if (docType === 'DEBIT NOTE') {
        numLabel = 'Debit Note#';
        dateLabel = 'DN Date';
        expLabel = 'Original Inv#';
      } else if (docType === 'TAX INVOICE') {
        numLabel = 'Invoice#';
        dateLabel = 'Invoice Date';
        expLabel = 'Due Date';
      } else if (docType === 'PROFORMA INVOICE') {
        numLabel = 'Proforma#';
        dateLabel = 'Proforma Date';
        expLabel = 'Due Date';
      } else if (docType === 'DELIVERY CHALLAN' || docType === 'DELIVERY NOTE') {
        numLabel = 'Challan#';
        dateLabel = 'Challan Date';
        expLabel = 'Dispatch Date';
      }

      const partyHeaderLabel = partyType === 'vendor' ? 'Vendor' : 'Customer';

      // Check if discount column has amount or percentage
      const hasDiscountAmount = (doc.items || []).some(i => i.discountType === 'amount');
      const discHeaderLabel = hasDiscountAmount ? 'Disc Amt' : 'Disc %';

      // Build smart pages (breakdown immediately after subtotal)
      const pages = this.buildPages(calc.items || [], docType, doc);
      const totalPages = pages.length;

      const ctx = {
        docType,
        partyType,
        party,
        org,
        placeOfSupply,
        isInterState,
        calc,
        numLabel,
        dateLabel,
        expLabel,
        partyHeaderLabel,
        discHeaderLabel
      };

      if (totalPages === 1) {
        return this.renderPage(doc, pages[0], 1, ctx);
      }

      return `
        <div class="shreeraksha-document-wrapper">
          ${pages.map((p, idx) => `
            ${this.renderPage(doc, p, totalPages, ctx)}
            ${idx < totalPages - 1 ? '<div class="page-break"></div>' : ''}
          `).join('')}
        </div>
      `;
    }
  };

  window.GSTDocumentTemplate = GSTDocumentTemplate;

})(window);
