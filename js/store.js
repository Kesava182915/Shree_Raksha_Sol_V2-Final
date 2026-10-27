/**
 * ZOHO INVOICE - REACTIVE LOCAL DATA STORE
 * Handles state management, localStorage persistence, event subscriptions, and seed data.
 * Customized for Shreeraksha Solutions with full Indian GST compliance, Vendor POs, and Credit/Debit Notes.
 */

(function (window) {
  'use strict';

  const STORAGE_KEY = 'zoho_invoice_db_v3_shreeraksha';

  const DEFAULT_DATA = {
    organization: {
      name: 'SHREERAKSHA SOLUTIONS',
      legalName: 'Shreeraksha Solutions',
      taxId: '29FEAPS4448D1ZA', // GSTIN
      msmeRegNo: 'UDYAM-KR-11-0087041',
      email: 'connect@shreeraksha.in',
      phone: '+91 9880 54 99 55 / +91 96636 91509',
      website: 'www.shreeraksha.in',
      address: '5-68, Mulliya Mata House, Ajjavara Post, Sulya\nDakshina Kannada - 574 239, Karnataka, India',
      state: 'Karnataka (29)',
      currency: 'INR',
      currencySymbol: '₹',
      logo: 'assets/shreeraksha-logo.svg',
      themeColor: 'zoho',
      invoicePrefix: 'SHRKS/Inv/26-27/',
      proformaPrefix: 'SHRKS/PI/26-27/',
      dcPrefix: 'SHRKS/DC/26-27/',
      estimatePrefix: 'SHRKS/Qtn/26-27/',
      poPrefix: 'SHRKS/PO/26-27/',
      creditNotePrefix: 'SHRKS/CN/26-27/',
      debitNotePrefix: 'SHRKS/DN/26-27/',
      defaultPaymentTerms: '30 Days net',
      bankName: 'State Bank of India',
      accountName: 'SHREERAKSHA SOLUTIONS',
      accountNumber: '45666081503',
      ifscCode: 'SBIN0016869',
      branch: 'PARKALA',
      defaultNotes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
      defaultTerms: `• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (30 Days net).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery.`
    },
    taxes: [
      { id: 'tax-18', name: 'GST 18%', rate: 18.0 },
      { id: 'tax-12', name: 'GST 12%', rate: 12.0 },
      { id: 'tax-5',  name: 'GST 5%',  rate: 5.0 },
      { id: 'tax-28', name: 'GST 28%', rate: 28.0 },
      { id: 'tax-0',  name: 'Zero Tax 0%', rate: 0.0 }
    ],
    items: [
      {
        id: 'item-1',
        name: 'ZODIAC C18',
        itemType: 'product',
        hsnCode: '90279090',
        sacCode: '',
        sku: 'ZOD-C18-250',
        rate: 39286.00,
        unit: 'nos',
        taxRate: 18.0,
        taxRateId: 'tax-18',
        description: '250mmx4.6mm, 5µm'
      },
      {
        id: 'item-2',
        name: 'ZODIAC C18',
        itemType: 'product',
        hsnCode: '90279090',
        sacCode: '',
        sku: 'ZOD-C18-150',
        rate: 39286.00,
        unit: 'nos',
        taxRate: 18.0,
        taxRateId: 'tax-18',
        description: '150mmx4.6mm, 3.5µm'
      },
      {
        id: 'item-3',
        name: 'Hypersil BDS C18',
        itemType: 'product',
        hsnCode: '90279090',
        sacCode: '',
        sku: 'HYP-BDS-250',
        rate: 67778.00,
        unit: 'nos',
        taxRate: 18.0,
        taxRateId: 'tax-18',
        description: '250mm x 4.6mm, 5µm'
      },
      {
        id: 'item-4',
        name: 'Chromatography Column Annual Calibration & Validation',
        itemType: 'service',
        hsnCode: '',
        sacCode: '998313',
        sku: 'SRV-CALIB-01',
        rate: 25000.00,
        unit: 'service',
        taxRate: 18.0,
        taxRateId: 'tax-18',
        description: 'Onsite HPLC system calibration, resolution verification, and certificate issuance.'
      },
      {
        id: 'item-5',
        name: 'HPLC Method Development & Resolution Optimization',
        itemType: 'service',
        hsnCode: '',
        sacCode: '998319',
        sku: 'SRV-METH-02',
        rate: 45000.00,
        unit: 'service',
        taxRate: 18.0,
        taxRateId: 'tax-18',
        description: 'Custom mobile phase formulation, retention factor analysis, and peak purity report.'
      }
    ],
    customers: [
      {
        id: 'cust-1',
        name: 'Manipal Speciality Chemicals Pvt Ltd',
        company: 'Manipal Speciality Chemicals Pvt Ltd',
        attention: 'Mr. Sreekar Nayak',
        email: 'sreekar.nayak@manipalspeciality.com',
        phone: '+91 820 257 1200',
        taxId: '29AATCM4200G1ZD',
        placeOfSupply: 'Karnataka (29)',
        currency: 'INR',
        billingAddress: '52/1A, Udayavani Building, Tile Factory Road, Manipal\nUdupi, Karnataka, India 576104',
        shippingAddress: 'Plot 18-B, Industrial Area, Shivalli, Manipal\nUdupi, Karnataka, India 576104',
        shippingPartyName: 'Manipal QC Analytical Facility & Receiving Bay',
        paymentTerms: '30 Days net',
        notes: 'Kind Attention: Mr. Sreekar Nayak. Priority pharmaceutical delivery.'
      },
      {
        id: 'cust-2',
        name: 'Sun Pharma Advanced Research Ltd',
        company: 'Sun Pharma Advanced Research Ltd',
        attention: 'Dr. Ananya Sharma',
        email: 'procurement@sunpharma.res.in',
        phone: '+91 22 6645 5600',
        taxId: '27AAACS1234D1Z2',
        placeOfSupply: 'Maharashtra (27)',
        currency: 'INR',
        billingAddress: 'Peninsula Business Park, Tower A, 8th Floor, Senapati Bapat Marg, Lower Parel\nMumbai, Maharashtra, India 400013',
        shippingAddress: 'Plot No 14, MIDC Industrial Area, Taloja\nNavi Mumbai, Maharashtra, India 410208',
        shippingPartyName: 'Sun Pharma R&D Formulation Centre (Consignee Unit)',
        paymentTerms: '30 Days net',
        notes: 'Inter-state client. IGST applies automatically.'
      },
      {
        id: 'cust-3',
        name: 'Biocon Biologics India Ltd',
        company: 'Biocon Biologics India Ltd',
        attention: 'Dr. Vikram Malhotra',
        email: 'procure@biocon.com',
        phone: '+91 80 2808 2808',
        taxId: '29AABCB2623P1ZL',
        placeOfSupply: 'Karnataka (29)',
        currency: 'INR',
        billingAddress: 'Biocon House, Semicon Park, Electronics City Phase II, Hosur Road\nBengaluru, Karnataka, India 560100',
        shippingAddress: 'Plot No 2-4, Bommasandra-Jigani Link Road, Bommasandra Ind. Area\nBengaluru, Karnataka, India 560099',
        shippingPartyName: 'Biocon Special Economic Zone (SEZ) Unit 2 (Consignee)',
        paymentTerms: '30 Days net',
        notes: 'High-purity LC columns for recombinant insulin batch release.'
      },
      {
        id: 'cust-4',
        name: 'Serum Institute of India Pvt Ltd',
        company: 'Serum Institute of India Pvt Ltd',
        attention: 'Mr. Adarsh Deshmukh',
        email: 'commercial@seruminstitute.com',
        phone: '+91 20 2699 3900',
        taxId: '27AAACS2728P1Z8',
        placeOfSupply: 'Maharashtra (27)',
        currency: 'INR',
        billingAddress: '212/2, Hadapsar, Off Soli Poonawalla Road\nPune, Maharashtra, India 411028',
        shippingAddress: 'Gate No. 3, Vaccine Production Complex, Manjari BK\nPune, Maharashtra, India 412307',
        shippingPartyName: 'Serum Institute Quality Control & Analytical Testing Hub',
        paymentTerms: '30 Days net',
        notes: 'Inter-state supply for vaccine validation laboratory.'
      },
      {
        id: 'vend-1',
        name: 'Thermo Fisher Scientific India Pvt Ltd',
        company: 'Thermo Fisher Scientific India Pvt Ltd',
        attention: 'Mr. Rajesh Pillai',
        isVendor: true,
        email: 'orders.india@thermofisher.com',
        phone: '+91 20 6626 7000',
        taxId: '27AAACT9921B1Z9',
        placeOfSupply: 'Maharashtra (27)',
        currency: 'INR',
        billingAddress: 'Godrej Millennium, 9 Koregaon Park Road\nPune, Maharashtra, India 411001',
        shippingAddress: 'Godrej Millennium, 9 Koregaon Park Road\nPune, Maharashtra, India 411001',
        paymentTerms: 'Net 30',
        notes: 'Primary chromatography consumables vendor.'
      }
    ],
    estimates: [
      {
        id: 'est-019',
        number: 'SHRKS/Qtn/26-27/019',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-03',
        expiryDate: '2026-12-31',
        placeOfSupply: 'Karnataka (29)',
        status: 'accepted',
        reference: 'RFQ-MANIPAL-8840',
        referenceDate: '2026-10-02',
        paymentTerms: '30 Days net',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18',
            description: '250mmx4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 6.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-2',
            name: 'ZODIAC C18',
            description: '150mmx4.6mm, 3.5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 3.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18',
            description: '250mm x 4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 1.00,
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        terms: '• Above prices are FOR Destination.\n• Please mention our Estimate number on all future correspondence.\n• Please share your valid GSTIN in your Purchase Order.\n• Payment Terms: As agreed (30 Days net).\n• In case of Refurbished requirement\n  * The defective part need to be returned - against delivery.\n• Delivery will be within 3-4 weeks from date of PO.\n  * Goods indicated above in stock are accurate as of the quote date.\n  * If goods are out of stock at the time of release of PO, standard lead time would apply.\n• Payment will be 50% advance and balance against delivery.'
      },
      {
        id: 'est-020',
        number: 'SHRKS/Qtn/26-27/020',
        customerId: 'cust-2',
        attention: 'Dr. Ananya Sharma',
        date: '2026-10-10',
        expiryDate: '2026-11-30',
        placeOfSupply: 'Maharashtra (27)', // Inter-state demonstration
        status: 'sent',
        reference: 'SUN-RFQ-9921',
        referenceDate: '2026-10-08',
        paymentTerms: '30 Days net',
        items: [
          {
            itemId: 'item-4',
            name: 'Chromatography Column Annual Calibration & Validation',
            description: 'Validation of 4 Waters Alliance HPLC Systems',
            itemType: 'service',
            hsnCode: '',
            sacCode: '998313',
            quantity: 2.00,
            rate: 25000.00,
            discountType: 'amount', // Testing flat amount discount
            discount: 2000.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18',
            description: '250mm x 4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 2.00,
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        notes: 'Inter-State supply to Maharashtra. Full 18% IGST is applicable as per GST regulations.',
        terms: 'Payment 30 Days Net from date of installation.'
      },
      {
        id: 'est-024',
        number: 'SHRKS/Qtn/26-27/024',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-15',
        expiryDate: '2026-12-31',
        placeOfSupply: 'Karnataka (29)',
        status: 'draft',
        reference: 'PUR-RFQ-8840',
        referenceDate: '2026-10-14',
        paymentTerms: '30 Days net',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18 Analytical Column',
            description: '250mm x 4.6mm, 5µm particle size, 120Å pore size',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 6.00,
            unit: "No's",
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-2',
            name: 'ZODIAC C18 Fast LC Column',
            description: '150mm x 4.6mm, 3.5µm high-resolution',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 3.00,
            unit: "No's",
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18 Premium Column',
            description: '250mm x 4.6mm, 5µm base-deactivated silica',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 1.00,
            unit: 'Pcs',
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-1',
            name: 'Waters Symmetry C8 Column',
            description: '150mm x 3.9mm, 5µm pharmaceutical grade',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 2.00,
            unit: "No's",
            rate: 45000.00,
            discountType: 'percent',
            discount: 10.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-2',
            name: 'Kromasil 100-5-C18 Column',
            description: '250mm x 4.6mm, 5µm analytical chemistry column',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 2.00,
            unit: "No's",
            rate: 42500.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-4',
            name: 'HPLC Column Protection Guard Cartridges',
            description: 'Pack of 5 universal 10mm cartridge guards',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 1.00,
            unit: 'Sets',
            rate: 18500.00,
            discountType: 'amount',
            discount: 500.00,
            taxRate: 18.0
          }
        ],
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        terms: '• Above prices are FOR Destination.\n• Please mention our Estimate number on all future correspondence.\n• Please share your valid GSTIN in your Purchase Order.\n• Payment Terms: As agreed (30 Days net).\n• Delivery will be within 3-4 weeks from date of PO.\n• Payment will be 50% advance and balance against delivery.'
      }
    ],
    invoices: [
      {
        id: 'inv-019',
        number: 'SHRKS/Inv/26-27/019',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-04',
        dueDate: '2026-11-03',
        placeOfSupply: 'Karnataka (29)',
        paymentTerms: '30 Days net',
        status: 'partially_paid',
        poNumber: 'PO/MANIPAL/26-27/088',
        billingAddress: '52/1A, Udayavani Building, Tile Factory Road, Manipal\nUdupi, Karnataka, India 576104',
        shippingAddress: 'Plot 18-B, Industrial Area, Shivalli, Manipal\nUdupi, Karnataka, India 576104',
        shippingPartyName: 'Manipal QC Analytical Facility & Receiving Bay',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18',
            description: '250mmx4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 6.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-2',
            name: 'ZODIAC C18',
            description: '150mmx4.6mm, 3.5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 3.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18',
            description: '250mm x 4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 1.00,
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        subtotal: 421394.00,
        discountTotal: 21069.70,
        taxTotal: 72058.38,
        rounding: -0.68,
        total: 472382.00,
        amountPaid: 200000.00,
        balanceDue: 272382.00,
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        terms: 'Payment due within 30 days.',
        history: [
          {
            date: '2026-10-04 10:15',
            action: 'Tax Invoice SHRKS/Inv/26-27/019 generated and issued to Manipal Speciality Chemicals',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-04 14:30',
            action: 'Consignee and Ship To delivery address verified (QC Unit, Manipal)',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-05 16:45',
            action: 'Payment of ₹ 2,00,000.00 recorded (BANK UTR: HDFC-NEFT-992104)',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-18 11:20',
            action: 'Audit verification completed. GST CGST/SGST ledger reconciled',
            user: 'Demo Customer [CUSTOMER]'
          }
        ]
      },
      {
        id: 'inv-020',
        number: 'SHRKS/Inv/26-27/020',
        customerId: 'cust-2',
        attention: 'Dr. Ananya Sharma',
        date: '2026-10-10',
        dueDate: '2026-11-09',
        placeOfSupply: 'Maharashtra (27)',
        paymentTerms: '30 Days net',
        status: 'paid',
        poNumber: 'SUN/PO/2026/0942',
        billingAddress: 'Peninsula Business Park, Tower A, 8th Floor, Senapati Bapat Marg, Lower Parel\nMumbai, Maharashtra, India 400013',
        shippingAddress: 'Plot No 14, MIDC Industrial Area, Taloja\nNavi Mumbai, Maharashtra, India 410208',
        shippingPartyName: 'Sun Pharma R&D Formulation Centre (Consignee Unit)',
        items: [
          {
            itemId: 'item-4',
            name: 'Chromatography Column Annual Calibration & Validation',
            description: 'Validation of 4 Waters Alliance HPLC Systems',
            itemType: 'service',
            hsnCode: '',
            sacCode: '998313',
            quantity: 2.00,
            rate: 25000.00,
            discountType: 'amount',
            discount: 2000.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18',
            description: '250mm x 4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 2.00,
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        subtotal: 185556.00,
        discountTotal: 8777.80,
        taxTotal: 31820.08,
        rounding: -0.28,
        total: 208598.00,
        amountPaid: 208598.00,
        balanceDue: 0.00,
        notes: 'Inter-State supply to Maharashtra. Full 18% IGST is applicable as per GST regulations.',
        terms: 'Payment 30 Days Net from date of installation.',
        history: [
          {
            date: '2026-10-10 11:00',
            action: 'Tax Invoice SHRKS/Inv/26-27/020 generated for Inter-State Supply (IGST 18%)',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-10 15:40',
            action: 'Bill To (Peninsula Business Park, Mumbai) and Ship To (MIDC Taloja) validated',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-12 09:30',
            action: 'E-Way Bill 241920194812 generated & dispatched via Blue Dart AWB 99401201',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-15 14:10',
            action: 'Full payment of ₹ 2,08,598.00 recorded (RTGS UTR: KKBK2610150912)',
            user: 'Demo Customer [CUSTOMER]'
          },
          {
            date: '2026-10-16 17:00',
            action: 'Statutory Tax Invoice audit sign-off completed',
            user: 'Shreeraksha Admin [ADMIN]'
          }
        ]
      },
      {
        id: 'inv-021',
        number: 'SHRKS/Inv/26-27/021',
        customerId: 'cust-3',
        attention: 'Dr. Vikram Malhotra',
        date: '2026-09-01',
        dueDate: '2026-10-01',
        placeOfSupply: 'Karnataka (29)',
        paymentTerms: '30 Days net',
        status: 'overdue',
        poNumber: 'BIO/PO/2026/OCT/041',
        billingAddress: 'Biocon House, Semicon Park, Electronics City Phase II, Hosur Road\nBengaluru, Karnataka, India 560100',
        shippingAddress: 'Plot No 2-4, Bommasandra-Jigani Link Road, Bommasandra Ind. Area\nBengaluru, Karnataka, India 560099',
        shippingPartyName: 'Biocon Special Economic Zone (SEZ) Unit 2 (Consignee)',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18',
            description: '250mm x 4.6mm, 5µm Analytical Column',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 4.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-5',
            name: 'HPLC Method Development & Resolution Optimization',
            description: 'Custom mobile phase formulation, retention factor analysis, and peak purity report',
            itemType: 'service',
            hsnCode: '',
            sacCode: '998319',
            quantity: 1.00,
            rate: 45000.00,
            discountType: 'percent',
            discount: 10.00,
            taxRate: 18.0
          }
        ],
        subtotal: 202144.00,
        discountTotal: 12357.20,
        taxTotal: 34161.62,
        rounding: 0.58,
        total: 223949.00,
        amountPaid: 0.00,
        balanceDue: 223949.00,
        notes: 'Order placed under annual rate contract ARC-2026-BIO.',
        terms: 'Payment due within 30 days of invoice receipt.',
        history: [
          {
            date: '2026-09-01 09:30',
            action: 'Tax Invoice SHRKS/Inv/26-27/021 generated and delivered to Accounts Dept',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-09-01 14:00',
            action: 'Bill to (Electronics City HQ) and Ship to (SEZ Bommasandra) stamped',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-02 10:00',
            action: 'Automatic payment reminder triggered upon 30-day net expiry',
            user: 'System Auditor [AUDIT]'
          },
          {
            date: '2026-10-15 16:30',
            action: 'First overdue escalation letter sent to Finance Directorate',
            user: 'Shreeraksha Admin [ADMIN]'
          }
        ]
      },
      {
        id: 'inv-022',
        number: 'SHRKS/Inv/26-27/022',
        customerId: 'cust-4',
        attention: 'Mr. Adarsh Deshmukh',
        date: '2026-10-18',
        dueDate: '2026-11-17',
        placeOfSupply: 'Maharashtra (27)',
        paymentTerms: '30 Days net',
        status: 'sent',
        poNumber: 'SIIPL/PUR/2026/8831',
        billingAddress: '212/2, Hadapsar, Off Soli Poonawalla Road\nPune, Maharashtra, India 411028',
        shippingAddress: 'Gate No. 3, Vaccine Production Complex, Manjari BK\nPune, Maharashtra, India 412307',
        shippingPartyName: 'Serum Institute Quality Control & Analytical Testing Hub',
        items: [
          {
            itemId: 'item-3',
            name: 'Hypersil BDS C18',
            description: '250mm x 4.6mm, 5µm base-deactivated analytical column',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 3.00,
            rate: 67778.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          },
          {
            itemId: 'item-4',
            name: 'Chromatography Column Annual Calibration & Validation',
            description: 'Onsite HPLC system calibration, resolution verification, and certificate issuance',
            itemType: 'service',
            hsnCode: '',
            sacCode: '998313',
            quantity: 1.00,
            rate: 25000.00,
            discountType: 'amount',
            discount: 0.00,
            taxRate: 18.0
          }
        ],
        subtotal: 228334.00,
        discountTotal: 10166.70,
        taxTotal: 39270.11,
        rounding: 0.59,
        total: 257438.00,
        amountPaid: 0.00,
        balanceDue: 257438.00,
        notes: 'Delivery against PO SIIPL/PUR/2026/8831 with temperature-monitored packaging.',
        terms: 'Payment 30 Days Net from date of delivery.',
        history: [
          {
            date: '2026-10-18 11:30',
            action: 'Tax Invoice SHRKS/Inv/26-27/022 drafted and reviewed by Accounts',
            user: 'Demo Customer [CUSTOMER]'
          },
          {
            date: '2026-10-18 16:00',
            action: 'Tax Invoice approved & sealed with statutory Bill to and Ship to details',
            user: 'Shreeraksha Admin [ADMIN]'
          },
          {
            date: '2026-10-19 10:15',
            action: 'Digitally transmitted to Serum Institute procurement desk',
            user: 'Shreeraksha Admin [ADMIN]'
          }
        ]
      },
      {
        id: 'dc-001',
        number: 'SHRKS/DC/26-27/001',
        invoiceType: 'delivery_note',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-16',
        dueDate: '2026-11-15',
        placeOfSupply: 'Karnataka (29)',
        paymentTerms: '30 Days net',
        status: 'sent',
        poNumber: 'PO/MANIPAL/26-27/095',
        billingAddress: '52/1A, Udayavani Building, Tile Factory Road, Manipal\nUdupi, Karnataka, India 576104',
        shippingAddress: 'Plot 18-B, Industrial Area, Shivalli, Manipal\nUdupi, Karnataka, India 576104',
        shippingPartyName: 'Manipal QC Analytical Facility & Receiving Bay',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18 Analytical Column',
            description: '250mm x 4.6mm, 5µm (Material dispatch under Delivery Challan)',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 2.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        subtotal: 78572.00,
        discountTotal: 3928.60,
        taxTotal: 13435.81,
        rounding: -0.21,
        total: 88079.00,
        amountPaid: 0.00,
        balanceDue: 88079.00,
        notes: 'Goods dispatched under Delivery Challan for job-work / incoming site trial.',
        terms: '• Material dispatched against PO/MANIPAL/26-27/095.\n• To be verified and converted into regular Tax Invoice upon acceptance.',
        history: [
          {
            date: '2026-10-16 11:30',
            action: 'Delivery Challan SHRKS/DC/26-27/001 created and dispatched',
            user: 'Shreeraksha Admin [ADMIN]'
          }
        ]
      },
      {
        id: 'pi-001',
        number: 'SHRKS/PI/26-27/001',
        invoiceType: 'proforma',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-17',
        dueDate: '2026-11-16',
        placeOfSupply: 'Karnataka (29)',
        paymentTerms: '30 Days net',
        status: 'sent',
        poNumber: 'PO/MANIPAL/26-27/098',
        poDate: '2026-10-15',
        billingAddress: '52/1A, Udayavani Building, Tile Factory Road, Manipal\nUdupi, Karnataka, India 576104',
        shippingAddress: 'Plot 18-B, Industrial Area, Shivalli, Manipal\nUdupi, Karnataka, India 576104',
        shippingPartyName: 'Manipal QC Analytical Facility & Receiving Bay',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18 Analytical Column',
            description: '250mm x 4.6mm, 5µm',
            itemType: 'product',
            hsnCode: '90279090',
            quantity: 2.00,
            rate: 39286.00,
            discountType: 'percent',
            discount: 5.00,
            taxRate: 18.0
          }
        ],
        subtotal: 78572.00,
        discountTotal: 3928.60,
        taxTotal: 13435.81,
        rounding: -0.21,
        total: 88079.00,
        amountPaid: 0.00,
        balanceDue: 88079.00,
        notes: 'Proforma Invoice issued for commercial clearance and advance billing.',
        terms: '• 50% advance against Proforma Invoice.\n• Balance against delivery.',
        history: [
          {
            date: '2026-10-17 10:00',
            action: 'Proforma Invoice SHRKS/PI/26-27/001 issued',
            user: 'Shreeraksha Admin [ADMIN]'
          }
        ]
      }
    ],
    purchaseOrders: [
      {
        id: 'po-005',
        number: 'SHRKS/PO/26-27/005',
        vendorId: 'vend-1',
        attention: 'Mr. Rajesh Pillai',
        date: '2026-10-02',
        dueDate: '2026-10-25',
        placeOfSupply: 'Karnataka (29)',
        status: 'issued',
        reference: 'INDENT-OCT-44',
        paymentTerms: 'Net 30',
        items: [
          {
            itemId: 'item-1',
            name: 'ZODIAC C18 Raw Assemblies',
            description: 'Unpacked analytical column blanks (250mm)',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 10.00,
            rate: 18500.00,
            discountType: 'percent',
            discount: 10.00,
            taxRate: 18.0
          }
        ],
        notes: 'Please dispatch via Blue Dart Express to our Sulya address.',
        terms: 'Material subject to QC inspection upon delivery.'
      }
    ],
    debitCreditNotes: [
      {
        id: 'note-001',
        number: 'SHRKS/CN/26-27/001',
        docType: 'CREDIT NOTE',
        partyType: 'customer',
        partyId: 'cust-1',
        customerId: 'cust-1',
        attention: 'Mr. Sreekar Nayak',
        date: '2026-10-06',
        originalInvoiceNumber: 'SHRKS/Inv/26-27/019',
        placeOfSupply: 'Karnataka (29)',
        status: 'approved',
        reason: 'Post-sales volume rebate and calibration discount',
        items: [
          {
            itemId: 'item-1',
            name: 'Volume Rebate on ZODIAC C18 Columns',
            description: 'Credit adjusted for Purchase Order bulk commitment',
            itemType: 'service',
            hsnCode: '',
            sacCode: '998313',
            quantity: 1.00,
            rate: 10000.00,
            discountType: 'amount',
            discount: 0,
            taxRate: 18.0
          }
        ],
        notes: 'Credit note value will be adjusted against Invoice SHRKS/Inv/26-27/019.'
      },
      {
        id: 'note-002',
        number: 'SHRKS/DN/26-27/002',
        docType: 'DEBIT NOTE',
        partyType: 'vendor',
        partyId: 'vend-1',
        vendorId: 'vend-1',
        attention: 'Mr. Rajesh Pillai',
        date: '2026-10-08',
        originalInvoiceNumber: 'TH-INV-8910',
        placeOfSupply: 'Maharashtra (27)',
        status: 'approved',
        reason: 'Transit damage / defective return against PO SHRKS/PO/26-27/005',
        items: [
          {
            itemId: 'item-1',
            name: 'Transit Damaged Column Blank Rejection',
            description: 'Damaged fittings returned via courier airway bill 882910',
            itemType: 'product',
            hsnCode: '90279090',
            sacCode: '',
            quantity: 2.00,
            rate: 18500.00,
            discountType: 'percent',
            discount: 10.00,
            taxRate: 18.0
          }
        ],
        notes: 'Debit Note issued towards damaged goods rejected during incoming QC.'
      }
    ],
    recurring: [],
    payments: [
      {
        id: 'pay-001',
        paymentNumber: 'PAY-000001',
        date: '2026-10-05',
        customerId: 'cust-1',
        invoiceId: 'inv-019',
        invoiceNumber: 'SHRKS/Inv/26-27/019',
        amount: 200000.00,
        mode: 'bank',
        reference: 'HDFC-NEFT-992104',
        notes: 'Advance part payment received.'
      },
      {
        id: 'pay-002',
        paymentNumber: 'PAY-000002',
        date: '2026-10-15',
        customerId: 'cust-2',
        invoiceId: 'inv-020',
        invoiceNumber: 'SHRKS/Inv/26-27/020',
        amount: 208598.00,
        mode: 'bank',
        reference: 'KKBK2610150912',
        notes: 'Full payment received against Tax Invoice SHRKS/Inv/26-27/020.'
      }
    ],
    expenses: [
      {
        id: 'exp-1',
        date: '2026-10-02',
        category: 'Travel',
        amount: 4500.00,
        vendor: 'KSRTC Airavat & Local Taxi',
        notes: 'Technician travel for Manipal Speciality Chemicals onsite installation',
        billable: true,
        customerId: 'cust-1',
        status: 'unbilled'
      }
    ],
    projects: [
      {
        id: 'proj-1',
        name: 'Manipal Lab HPLC Method Development',
        customerId: 'cust-1',
        billingMethod: 'hourly',
        ratePerHour: 3500.00,
        status: 'active',
        tasks: [
          { id: 'task-1', name: 'Column Validation', budgetHours: 20 }
        ]
      }
    ],
    timesheets: [],
    activities: [
      { id: 'act-1', text: 'Tax Invoice SHRKS/Inv/26-27/022 issued to Serum Institute of India Pvt Ltd', time: '2026-10-18 16:00', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-2', text: 'Full payment of ₹ 2,08,598.00 reconciled for Tax Invoice SHRKS/Inv/26-27/020 (Sun Pharma)', time: '2026-10-15 14:10', user: 'Demo Customer', role: 'customer' },
      { id: 'act-3', text: 'Overdue audit escalation dispatched for Tax Invoice SHRKS/Inv/26-27/021 (Biocon)', time: '2026-10-15 16:30', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-4', text: 'E-Way Bill 241920194812 verified for Tax Invoice SHRKS/Inv/26-27/020 dispatch', time: '2026-10-12 09:30', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-5', text: 'Tax Invoice SHRKS/Inv/26-27/020 issued to Sun Pharma (Inter-State IGST 18%)', time: '2026-10-10 11:00', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-6', text: 'Debit Note SHRKS/DN/26-27/002 approved for ₹ 36,630.00 (Thermo Fisher)', time: '2026-10-08 14:15', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-7', text: 'Part payment of ₹ 2,00,000.00 received for Tax Invoice SHRKS/Inv/26-27/019 (Manipal)', time: '2026-10-05 16:45', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-8', text: 'Tax Invoice SHRKS/Inv/26-27/019 issued with Bill To & Ship To to Manipal Speciality Chemicals', time: '2026-10-04 10:15', user: 'Shreeraksha Admin', role: 'admin' },
      { id: 'act-9', text: 'Quotation SHRKS/Qtn/26-27/019 accepted by Manipal Speciality Chemicals', time: '2026-10-03 10:30', user: 'Demo Customer', role: 'customer' },
      { id: 'act-10', text: 'Vendor PO SHRKS/PO/26-27/005 issued to Thermo Fisher Scientific', time: '2026-10-02 11:00', user: 'Shreeraksha Admin', role: 'admin' }
    ]
  };

  class Store {
    constructor() {
      this.listeners = {};
      this.syncTimeout = null;
      this.load();
    }

    load() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          this.data = JSON.parse(stored);
          for (const key in DEFAULT_DATA) {
            if (!this.data[key] || (Array.isArray(DEFAULT_DATA[key]) && DEFAULT_DATA[key].length > 0 && Array.isArray(this.data[key]) && this.data[key].length === 0)) {
              this.data[key] = JSON.parse(JSON.stringify(DEFAULT_DATA[key]));
            }
          }
          // Safeguard critical collections from test corruption or empty arrays
          if (!this.data.estimates || this.data.estimates.length === 0) {
            this.data.estimates = JSON.parse(JSON.stringify(DEFAULT_DATA.estimates));
          }
          if (!this.data.invoices || this.data.invoices.length === 0 || (this.data.invoices.length === 1 && this.data.invoices[0].id === 'inv-1')) {
            this.data.invoices = JSON.parse(JSON.stringify(DEFAULT_DATA.invoices));
          } else {
            if (!this.data.invoices.some(i => i.invoiceType === 'delivery_note' || (i.number && i.number.includes('/DC/')))) {
              const sampleDC = DEFAULT_DATA.invoices.find(i => i.id === 'dc-001');
              if (sampleDC) this.data.invoices.push(JSON.parse(JSON.stringify(sampleDC)));
            }
            if (!this.data.invoices.some(i => i.invoiceType === 'proforma' || (i.number && i.number.includes('/PI/')))) {
              const samplePI = DEFAULT_DATA.invoices.find(i => i.id === 'pi-001');
              if (samplePI) this.data.invoices.push(JSON.parse(JSON.stringify(samplePI)));
            }
          }
        } else {
          this.data = JSON.parse(JSON.stringify(DEFAULT_DATA));
          this.save();
        }
      } catch (err) {
        console.error('Error loading store, falling back to default:', err);
        this.data = JSON.parse(JSON.stringify(DEFAULT_DATA));
      }

      // Synchronize with SQLite backend database
      this.syncFromBackend();
    }

    async syncFromBackend() {
      try {
        const res = await fetch('/api/db/data');
        if (!res.ok) return;
        const result = await res.json();
        if (result.success && result.data && Object.keys(result.data).length > 0) {
          const backendData = result.data;
          // Guard against truncated data missing quotes or invoices
          if (!backendData.estimates || backendData.estimates.length === 0) {
            backendData.estimates = JSON.parse(JSON.stringify(DEFAULT_DATA.estimates));
          }
          if (!backendData.invoices || backendData.invoices.length === 0 || (backendData.invoices.length === 1 && backendData.invoices[0].id === 'inv-1')) {
            backendData.invoices = JSON.parse(JSON.stringify(DEFAULT_DATA.invoices));
          }
          if (!backendData.customers || backendData.customers.length === 0) {
            backendData.customers = JSON.parse(JSON.stringify(DEFAULT_DATA.customers));
          } else {
            const existingCustIds = new Set(backendData.customers.map(c => c.id));
            (DEFAULT_DATA.customers || []).forEach(dc => {
              if (!existingCustIds.has(dc.id)) {
                backendData.customers.push(JSON.parse(JSON.stringify(dc)));
              }
            });
          }
          if (backendData.organization) {
            if (!backendData.organization.bankName || backendData.organization.bankName === 'HDFC Bank') {
              backendData.organization.bankName = 'State Bank of India';
              backendData.organization.accountName = 'SHREERAKSHA SOLUTIONS';
              backendData.organization.accountNumber = '45666081503';
              backendData.organization.branch = 'PARKALA';
              backendData.organization.ifscCode = 'SBIN0016869';
            }
          }
          if (!backendData.debitCreditNotes || backendData.debitCreditNotes.length === 0) {
            backendData.debitCreditNotes = JSON.parse(JSON.stringify(DEFAULT_DATA.debitCreditNotes));
          }
          if (!backendData.items || backendData.items.length === 0) {
            backendData.items = JSON.parse(JSON.stringify(DEFAULT_DATA.items));
          }
          this.data = backendData;
          try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
          } catch (e) {}
          this.emit('change', { collection: 'all', type: 'backend_sync' });
          console.log('[Store] Synchronized with SQLite database successfully.');
        } else {
          // Database is newly initialized; seed initial data to SQLite backend
          this.syncToBackend();
        }
      } catch (err) {
        console.warn('[Store] Operating in local cached mode:', err.message);
      }
    }

    save() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
      } catch (err) {
        console.error('Failed to save to localStorage:', err);
      }

      // Immediate real-time persistence to SQLite backend database
      clearTimeout(this.syncTimeout);
      this.syncTimeout = setTimeout(() => {
        this.syncToBackend();
      }, 50);
    }

    async syncToBackend() {
      try {
        await fetch('/api/db/sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key: 'main_data', data: this.data })
        });
      } catch (err) {
        console.warn('[Store] Could not persist to server DB:', err.message);
      }
    }

    on(event, callback) {
      if (!this.listeners[event]) this.listeners[event] = [];
      this.listeners[event].push(callback);
    }

    emit(event, payload) {
      if (this.listeners[event]) {
        this.listeners[event].forEach(fn => fn(payload));
      }
      if (this.listeners['*']) {
        this.listeners['*'].forEach(fn => fn(event, payload));
      }
    }

    getAll(collection) {
      return this.data[collection] || [];
    }

    getById(collection, id) {
      const list = this.getAll(collection);
      return list.find(item => item.id === id) || null;
    }

    add(collection, item) {
      if (!this.data[collection]) this.data[collection] = [];
      if (!item.id) {
        item.id = collection.slice(0, 4) + '-' + Date.now();
      }
      this.data[collection].unshift(item);
      this.save();
      this.logActivity(`Created ${collection.slice(0, -1)}: ${item.number || item.name || item.id}`);
      this.emit(`${collection}:change`, { type: 'add', item });
      this.emit('change', { collection, type: 'add', item });
      return item;
    }

    update(collection, id, updates) {
      const list = this.getAll(collection);
      const index = list.findIndex(item => item.id === id);
      if (index !== -1) {
        list[index] = { ...list[index], ...updates };
        this.save();
        this.emit(`${collection}:change`, { type: 'update', item: list[index] });
        this.emit('change', { collection, type: 'update', item: list[index] });
        return list[index];
      }
      return null;
    }

    delete(collection, id) {
      if (!this.data[collection]) return false;
      const initialLen = this.data[collection].length;
      this.data[collection] = this.data[collection].filter(item => item.id !== id);
      if (this.data[collection].length !== initialLen) {
        this.save();
        this.emit(`${collection}:change`, { type: 'delete', id });
        this.emit('change', { collection, type: 'delete', id });
        return true;
      }
      return false;
    }

    getOrg() {
      return this.data.organization;
    }

    updateOrg(updates) {
      this.data.organization = { ...this.data.organization, ...updates };
      this.save();
      this.emit('org:change', this.data.organization);
      this.emit('change', { collection: 'organization', item: this.data.organization });
      return this.data.organization;
    }

    logActivity(text) {
      const now = new Date();
      const timeStr = now.toISOString().replace('T', ' ').substring(0, 16);
      const act = {
        id: 'act-' + Date.now(),
        text,
        time: timeStr
      };
      if (!this.data.activities) this.data.activities = [];
      this.data.activities.unshift(act);
      if (this.data.activities.length > 50) this.data.activities.pop();
      this.save();
      this.emit('activity:new', act);
    }

    getActivities() {
      return this.data.activities || [];
    }

    exportJSON() {
      return JSON.stringify(this.data, null, 2);
    }

    importJSON(jsonString) {
      try {
        const parsed = JSON.parse(jsonString);
        if (parsed.organization) {
          this.data = parsed;
          this.save();
          this.emit('change', { collection: 'all', type: 'import' });
          return true;
        }
        return false;
      } catch (err) {
        console.error('Invalid JSON import:', err);
        return false;
      }
    }

    resetToDemo() {
      this.data = JSON.parse(JSON.stringify(DEFAULT_DATA));
      this.save();
      fetch('/api/db/reset', { method: 'POST' }).catch(() => {});
      this.emit('change', { collection: 'all', type: 'reset' });
    }

    getNextNumber(type) {
      const org = this.getOrg();
      if (type === 'invoice') {
        const count = this.getAll('invoices').filter(i => i.invoiceType !== 'proforma' && i.invoiceType !== 'delivery_note' && (!i.number || (!i.number.includes('/PI/') && !i.number.includes('/DC/')))).length + 20;
        return `${org.invoicePrefix || 'SHRKS/Inv/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'proforma') {
        const count = this.getAll('invoices').filter(i => i.invoiceType === 'proforma' || (i.number && i.number.includes('/PI/'))).length + 1;
        return `${org.proformaPrefix || 'SHRKS/PI/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'delivery_note' || type === 'dc' || type === 'delivery_challan') {
        const count = this.getAll('invoices').filter(i => i.invoiceType === 'delivery_note' || (i.number && i.number.includes('/DC/'))).length + 1;
        return `${org.dcPrefix || 'SHRKS/DC/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'estimate') {
        const count = this.getAll('estimates').length + 21;
        return `${org.estimatePrefix || 'SHRKS/Qtn/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'po') {
        const count = this.getAll('purchaseOrders').length + 6;
        return `${org.poPrefix || 'SHRKS/PO/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'creditNote') {
        const count = this.getAll('debitCreditNotes').filter(n => n.docType === 'CREDIT NOTE').length + 2;
        return `${org.creditNotePrefix || 'SHRKS/CN/26-27/'}${String(count).padStart(3, '0')}`;
      } else if (type === 'debitNote') {
        const count = this.getAll('debitCreditNotes').filter(n => n.docType === 'DEBIT NOTE').length + 3;
        return `${org.debitNotePrefix || 'SHRKS/DN/26-27/'}${String(count).padStart(3, '0')}`;
      }
      return 'DOC-' + Date.now();
    }

    syncLineMaterials(lineItems) {
      if (!Array.isArray(lineItems)) return;
      const allItems = this.getAll('items') || [];

      lineItems.forEach(item => {
        if (!item.name || !item.name.trim()) return;
        const cleanName = item.name.trim();

        const existing = (item.itemId && this.getById('items', item.itemId)) ||
          allItems.find(it => it.name && it.name.trim().toLowerCase() === cleanName.toLowerCase());

        const itemType = item.itemType || 'product';
        const isService = itemType === 'service';
        const hsnVal = isService ? '' : (item.hsnCode || '90279090');
        const sacVal = isService ? (item.sacCode || '998313') : '';
        const codeVal = isService ? sacVal : hsnVal;

        const payload = {
          name: cleanName,
          itemType: itemType,
          type: itemType,
          hsnCode: hsnVal,
          sacCode: sacVal,
          hsnSac: codeVal,
          rate: parseFloat(item.rate) || 0,
          unit: item.unit || 'nos',
          taxRate: parseFloat(item.taxRate) || 18,
          description: item.description || ''
        };

        if (existing) {
          this.update('items', existing.id, payload);
          item.itemId = existing.id;
        } else {
          const created = this.add('items', payload);
          item.itemId = created.id;
          allItems.push(created);
        }
      });
    }
  }

  window.AppStore = new Store();

})(window);
